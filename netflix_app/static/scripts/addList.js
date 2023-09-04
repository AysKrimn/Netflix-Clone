async function add_list(profileId, movieId) {

    alert(profileId)
    const request = await fetch(`http://127.0.0.1:8000/v1/api/movies/profiles/${profileId}/item/${movieId}/add`)
    const response = await request.json()
  
    console.log("svden gelen veri:", response)
  
  }