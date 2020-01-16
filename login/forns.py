from core.forms.validate.form import Form
from login.models.auth import User
class LoginForm(Form):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'password']


class ChangePasswordForm(Form):
    fields = ['new_password', 'confirma_password']