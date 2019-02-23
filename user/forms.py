from django import forms


from .models import User


class UserForm(forms.ModelForm):
    score = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'score']


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=64, required=True)
    firstname = forms.CharField(label='نام', max_length=64, required=True)
    lastname = forms.CharField(label='نام خانوادگی', max_length=128, required=True)
    email = forms.EmailField(label='ایمیل', required=True)
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "گذرواژه و تکرار گذرواژه‌ای که وارد کرده‌اید، یکسان نیستند"
            )
