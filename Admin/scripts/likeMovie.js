async function handleLike(movieId) {

    const endpoint = `${base_api_url}/movies/${movieId}/like`
    const request = await fetch(endpoint)
    const response = await request.json()

    alert(response.message)
}