from .models import NetflixProfile

def current_profile(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        cookie_id = request.COOKIES.get('selected_profile')

        if request.user.is_authenticated and cookie_id:
            print("girdim")
            profile =  NetflixProfile.objects.get(id = cookie_id)
            print("çıktım")
            # request'in içine selectedProfiel adında bir key atarız ve profili value olarak göndeririz.
            request.selectedProfile = profile
        
        
        response = get_response(request)

        return response

    return middleware