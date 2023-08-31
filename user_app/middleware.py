from .models import NetflixProfile

def current_profile(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        cookie_id = request.COOKIES.get('selected_profile')

        if request.user.is_authenticated and cookie_id:

            profile = NetflixProfile.objects.filter(id = cookie_id).first()
            request.selectedProfile = profile
        
        
        response = get_response(request)

        return response

    return middleware