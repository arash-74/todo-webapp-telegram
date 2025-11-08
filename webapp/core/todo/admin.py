from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from todo.forms import CreateUserForm, ChangeUserForm
from todo.models import User, Todo


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    def identify(self,obj):
        if obj.username:
            return obj.username
        if obj.chat_id:
            return obj.chat_id
    list_display = ('id', 'identify')
    add_form = CreateUserForm
    form = ChangeUserForm
    fieldsets = (('None', {'fields': ('username', 'chat_id')}),)
    add_fieldsets = (('None', {'fields': ('chat_id',)}),)

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('user__chat_id','title','created_at')