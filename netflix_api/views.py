from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user_app.models import Movies

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