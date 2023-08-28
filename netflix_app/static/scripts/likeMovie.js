async function like_movie(movieId) {

    const request = await fetch(`http://127.0.0.1:8000/v1/api/movies/${movieId}/like`)
    const response = await request.json()
  
    console.log("svden gelen veri:", response)
    if (response.message === "Movie is liked") {
  
      alert(response.message)
    }
  
  }