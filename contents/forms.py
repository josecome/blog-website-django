from django import forms  
from .models import (
    Post,
)


class ContentForm(forms.ModelForm):  
    class Meta:  
        model = Post
        fields = ["title", "post_type", "post_content"]
        # fields = "__all__"  