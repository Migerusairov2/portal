from django.shortcuts import redirect


class RequirePasswordSetupMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        if request.user.is_authenticated:

            needs_password = not request.user.has_usable_password()

            allowed_paths = [
            "/account/set-password/",
            "/accounts/logout/",
            "/",
            ]

            if (
                needs_password
                and request.path not in allowed_paths
            ):
                return redirect("set_password")


        return self.get_response(request)