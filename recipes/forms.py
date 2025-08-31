from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your name...",
            "class": "co-input",
        }),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "placeholder": "example@domain.com",
            "class": "co-input",
        }),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            "rows": 5,
            "placeholder": "Your thoughts, feedback, or questions type right here...",
            "class": "co-textarea",
        }),
    )
    fun_question = forms.CharField(
        label="What's your favorite retro-inspired dish?",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Optional, but fun!",
            "class": "co-input",
        }),
    )

    # simple honeypot (hidden field that humans won't fill)
    hp = forms.CharField(required=False, widget=forms.HiddenInput())


    def clean_hp(self):
        if self.cleaned_data.get("hp"):
            raise forms.ValidationError("Spam detected.")
        return self.cleaned_data["hp"]
    
