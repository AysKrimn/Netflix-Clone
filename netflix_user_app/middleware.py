from .models import NetflixProfile, MovieTypes

def selected_profile(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request/response after
        # the view is called.
        # film / dizi categorilerini al
        categories = MovieTypes.objects.all()
        request.categories = categories

        # cookielerde selected profile var mı? 
        selected_profile_id = request.COOKIES.get('selected_profile_id')

        if selected_profile_id:
            profileObject = NetflixProfile.objects.filter(id = selected_profile_id).first()


            if profileObject:
                request.profile = profileObject

            print("şuanki profil:", request.profile)


             # Code to be executed for each request before
             # the view (and later middleware) are called.

        response = get_response(request)
        return response

    return middleware