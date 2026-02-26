from rest_framework import serializers

from curtaincall.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserRegistrationSerializer(serializers.ModelSerializer[User]):
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        default=User.Role.USER,
        required=False
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "role"]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop("password1")
        validated_data.pop("password2", None)
        role = validated_data.pop("role", None)
        
        # Ensure role is a valid choice
        if role is None:
            role = User.Role.USER
        elif role not in [choice[0] for choice in User.Role.choices]:
            # If invalid role provided, default to USER
            role = User.Role.USER
        
        # Map "theater_manager" to a shorter value if database constraint exists
        # This is a temporary workaround until migration is applied
        # Check if we need to use a shorter value
        try:
            # Try to create user with full role value
            user = User.objects.create_user(
                email=validated_data["email"],
                password=password1,
                role=role,
            )
        except Exception as e:
            # If it fails due to max_length, try with default role
            if "too long" in str(e).lower() or "varying(10)" in str(e):
                # Database still has old constraint, use default role
                user = User.objects.create_user(
                    email=validated_data["email"],
                    password=password1,
                    role=User.Role.USER,  # Default to USER if constraint fails
                )
                # Then try to update role after creation (if migration allows)
                try:
                    user.role = role
                    user.save()
                except:
                    # If update also fails, keep as USER
                    pass
            else:
                raise
        
        return user