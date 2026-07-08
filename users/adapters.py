from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        user = request.user

        if (
            user.is_authenticated
            and not user.has_usable_password()
        ):
            return reverse("set_password")

        return reverse("post_list")