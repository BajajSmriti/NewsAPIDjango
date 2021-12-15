from django import forms
from blogsNewsModule.models import Profile

class ProfileForm(forms.ModelForm):
    """Fields to show in the blog formt"""
    class Meta:
        model = Profile
        fields = ['bio','profile_pic','website_url','instagram_url']
        widgets = {
            'bio': forms.Textarea(attrs={'class':'fadeIn second','maxlength':"30000",'style':"height:300px; overflow:auto; resize: none; width:105%"}),
            'website_url': forms.TextInput(attrs={'class':'fadeIn second','maxlength':"300",'style':'width:105%'}),
            'instagram_url':forms.TextInput(attrs={'class':'fadeIn second','maxlength':"300",'style':'width:105%;'}),
        }