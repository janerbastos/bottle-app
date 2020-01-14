from core.forms.validate.form import Form
from login.models.auth import User
class LoginForm(Form):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'password']