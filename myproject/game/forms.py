from game.models import Comment
from django import forms


class MessageForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
    #  super to klasa wyzej
    #  def is_valid(self):
    #     super(MessageForm, self).is_valid()

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['sent_by'].widget = forms.HiddenInput()

class EmailForm(forms.ModelForm):
    subject = forms.CharField()
    text = forms.Textarea()
    from_who = forms.EmailField()
    to_who = forms.EmailField()