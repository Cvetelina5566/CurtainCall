from django.contrib import admin
from .models.hall import Hall
from .models.performance import Performance
from .models.play import Play
# from curtaincall.users import UserType
from .models import Theatre, Order, Ticket

# @admin.register(UserType)
# class UserTypeAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role_type', 'theater')
#     list_filter = ('role_type',)

admin.site.register(Play)
admin.site.register(Hall)
admin.site.register(Performance)
admin.site.register(Ticket)