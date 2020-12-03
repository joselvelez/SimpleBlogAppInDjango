from django import forms
from .models import Comment
from mptt.forms import TreeNodeChoiceField

class NewCommentForm(forms.ModelForm):

    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    # Modify the parent field so that it is not a required field in the form.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide the parent selector from the page
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }