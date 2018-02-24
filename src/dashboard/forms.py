from django import forms

from account.models import UserDetails, User


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'profile_image']


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['password']

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError("The Password Does Not Match")
        return old_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password Doesn't Match")
        return confirm_password

    def save(self, commit=False):
        user = super(ChangePasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user

