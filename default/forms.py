from django import forms
from base_user.models import MyUser
from .models import Meals, Ordering, CommentPost
from image_cropping import ImageCropWidget


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Şifrə", widget=forms.PasswordInput())
    password_confirm = forms.CharField(label="Şifrə2", widget=forms.PasswordInput())

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return password_confirm
    class Meta:
        model = MyUser
        fields=['username','email']


class CookerRegisterForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone']

    password = forms.CharField(label="Şifrə", widget=forms.PasswordInput())
    password_confirm = forms.CharField(label="Şifrə2", widget=forms.PasswordInput())

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return password_confirm
    def clean_phone(self):
        if self.cleaned_data['phone'].startswith('55') or self.cleaned_data['phone'].startswith('70') or self.cleaned_data['phone'].startswith('77') or self.cleaned_data['phone'].startswith('51') or self.cleaned_data['phone'].startswith('50'):
            return self.cleaned_data['phone']
        else:
            raise forms.ValidationError('Nomre duzgun yigilmayib')


class AddFood(forms.ModelForm):
    class Meta:
        model=Meals
        fields = ["name", "category","delivery_type","price","quantity"]




class OrderingForm(forms.ModelForm):
    class Meta:
        model = Ordering
        fields=['location','phone_number','quantity','delivery_type']

class CommentForm(forms.ModelForm):
    class Meta:
        model=CommentPost
        fields=["comment"]


class ProfilePhotouser(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=['profile_photo']

class SocialUser(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=['instagram','facebook','twitter']



class ChangePassword(forms.Form):
    password = forms.CharField(label="Yeni Şifrə", widget=forms.PasswordInput())
    password_confirm = forms.CharField(label="Təkrar Şifrə", widget=forms.PasswordInput())

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return password_confirm


