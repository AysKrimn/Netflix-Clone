from django.shortcuts import render
from django.http import JsonResponse
# Movie Modelini çek
from userApp.models import Movie
# listeme ekle bölümü (api)
def movie_set(request, movieId, userId):
    context = {}
    if request.user.is_authenticated:
           
            
            movieId = int(movieId)
            userId = int(userId)

            print("Payload:", movieId, "userId:", userId)

            # filmi çek
            movie = Movie.objects.filter(id=movieId).first()

            print("film adı:", movie.movie_name)

            if movie is None:
                context["serverResponse"] = 404
            else:
                # eğer movie varsa
                request.user.movie_list.add(movie)
                context['serverResponse'] = 200

            
            return JsonResponse(context)
    else:
         context['serverResponse'] = 403
         return JsonResponse(context)