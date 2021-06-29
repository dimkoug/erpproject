from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    UserCreationForm as BaseUserCreationForm,
    SetPasswordForm as BaseSetPasswordForm,
)

from core.forms import BootstrapForm


class UserCreationForm(BootstrapForm, BaseUserCreationForm):
    pass


class UserAuthenticationForm(BootstrapForm, BaseAuthenticationForm):
    pass


class UserPasswordResetForm(BootstrapForm, BasePasswordResetForm):
    pass


class UserSetPasswordForm(BootstrapForm, BaseSetPasswordForm):
    pass
