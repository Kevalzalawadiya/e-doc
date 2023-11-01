from django.contrib import admin
from .models import AdminUser   
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        required=True, widget=forms.PasswordInput(
            render_value=True,
            attrs={'autocomplete': 'off'}
        )
    )

    def _init_(self, *args, **kwargs):
        super(UserCreationForm, self)._init_(*args, **kwargs) # type: ignore
       
        if kwargs.get('instance'):
            self.existing_user = kwargs.get('instance')
        self.fields['is_active'].help_text = 'Keep this blank if new user' + \
            ' otherwise user won\'t receive invite. '

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if self.cleaned_data.get("password") and not self.cleaned_data.get(
            "password"
        ).startswith('pbkdf2_sha256'):
            user.set_password(self.cleaned_data["password"])
            print("Not set")

        user.save()
        return user


class MainAdmin(admin.ModelAdmin):
    form = UserCreationForm
    list_display = (
        'username','first_name', 'email', 'mobile_number', 'address'
    )
    fields = ('password', 'username', 'first_name', 'last_name', 'email', 'mobile_number', 'address','forget_password_token')
    exclude = ['user_permissions', 'groups',
               'last_login',
               'date_joined', 'activation_token', 'activation_timestamp',
               'password_reset_token', 'password_reset_expire_timestamp',
               'password_reset_timestamp']
    def get_form(self, request, obj=None, **kwargs):
        form = super(MainAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form
    
    
admin.site.register(AdminUser, MainAdmin)