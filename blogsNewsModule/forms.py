from django import forms
# from tinymce import TinyMCE
from .models import Post


# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False

class PostForm(forms.ModelForm):
    """Fields to show in the blog form"""
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'fadeIn second','maxlength':"300",'style':'width:105%'}),
            'author': forms.TextInput(attrs={'class':'fadeIn second','style':'width:105%;','value':'','id':'updateAuthor','type':'hidden'}),
            'content': forms.Textarea(attrs={'class':'fadeIn second','maxlength':"30000",'style':"height:300px; overflow:auto; resize: none; width:105%"}),
            'likes': forms.MultipleHiddenInput(),

        }