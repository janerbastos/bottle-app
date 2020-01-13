from core.forms.validate.form import Form
class LoginForm(Form):
    fields = ['first_name', 'last_name', 'username', 'email', 'password']