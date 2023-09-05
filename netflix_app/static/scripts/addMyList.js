async function handleAddList(movieId) {

    const endpoint = `${base_api_url}/myList/${movieId}/add`
    const request = await fetch(endpoint)
    const response = await request.json()

    alert(response.message)
}