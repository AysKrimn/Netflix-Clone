from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user_app.models import Movies, NetflixUser

@login_required(login_url="user_login")
def like_movie(request, movieId):
    response = {}

    movie = Movies.objects.filter(id = movieId).first()

    if movie is None:
        response['message'] = "Invalid Movie"
    
    else:
        movie.movie_likes += 1
        movie.save()
        response['message'] = "Movie is liked"


    # JSON yanıt dön
    return JsonResponse(response)


@login_required(login_url="user_login")
def addMyList(request, movieId):
    response = {}

    movie = Movies.objects.filter(id = movieId).first()

    if movie is None:
        response['message'] = "Invalid Movie"

    else:
        request.selectedProfile.list.add(movie)
        response['message'] = "Added to my list"
    
    return JsonResponse(response)



@login_required(login_url="user_login")
def removeMyList(request, movieId):
    response = {}

    movie = Movies.objects.filter(id = movieId).first()

    if movie is None:
        response['message'] = "Invalid Movie"

    else:
        request.selectedProfile.list.remove(movie)
        response['message'] = "Removed from my list"
    
    return JsonResponse(response)


@login_required(login_url="user_login")
def kidProtect(request):
    response = {}

    user = NetflixUser.objects.filter(id = request.user.id).first()

    if user is None:
        response['data'] = { "status": "Not Found", "message": "Invalid User"}
    else:
        
        if user.kidProtect == False:
            user.kidProtect = True
            response['data'] = { "status": "active", "message": "Ebeveyn koruması aktif hale getirildi"}
        else:
            user.kidProtect = False
            response['data'] = { "status": "deactive", "message": "Ebeveyn koruması deaktif hale getirildi"}
        # db'e kaydet
        user.save()

    # json dön
    return JsonResponse(response)


@login_required(login_url="user_login")
def canceloractiveSub(request):
    response = {}

    if request.user.is_premiumUser:

        request.user.is_premiumUser = False
        response['message'] = "deactived"
    else:

        request.user.is_premiumUser = True
        response["message"] = "actived"

    
    request.user.save()
    return JsonResponse(response)

