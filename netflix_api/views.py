from django.http import JsonResponse

# modeller
from netflix_user_app.models import *

def likeMovie(request, movieId):
    response = {}

    print("user:", request.user)

    if request.user.is_authenticated:
       

        print("endpointe gelen istek:", movieId)
        # böyle bir film var mı?
        movie = Movies.objects.filter(id = movieId).first()

        if movie:
            movie.movie_likes += 1
            movie.save()
            response['message'] = "Movie is liked"
        else:
            response['message'] = "Movie is not found"


    else:
         response['message'] = "Login required"


    return JsonResponse(response)



def addList(request, profileId, movieId):
     
     print("addlist gelen veriler:", profileId, movieId)
     response = {}

     if request.user.is_authenticated:
         
        profile = NetflixProfile.objects.filter(id = profileId).first()

        if profile is None:
            response['message'] = "Invalid Profile"
            return JsonResponse(response)


        movie = Movies.objects.filter(id = movieId).first()
        

        if movie is None:
            response['message'] = "Invalid Movie"
            return JsonResponse(response)

        # usere bu movieyi ekle
        profile.list.add(movie)

        response['message'] = "Movie added to user list"
        return JsonResponse(response)


# listemden çikar
def removeList(request, profileId, movieId):
     response = {}
     if request.user.is_authenticated:
         
          movie = Movies.objects.filter(id = movieId).first()

          if movie:
              request.profile.list.remove(movie)
              response['message'] = "removed"

        
          else:
              response['message'] = "invalid movie"

          return JsonResponse(response)
     else:
         response['message'] = "login required"
         return JsonResponse(response)