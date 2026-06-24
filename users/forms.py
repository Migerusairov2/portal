from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget.attrs.update({
            "placeholder": "Current password"
        })

        self.fields["new_password1"].widget.attrs.update({
            "placeholder": "New password"
        })

        self.fields["new_password2"].widget.attrs.update({
            "placeholder": "Confirm new password"
        })