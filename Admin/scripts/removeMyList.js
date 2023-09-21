async function removeMyList(event, movieId) {

    const endpoint = `${base_api_url}/myList/${movieId}/remove`
    const request = await fetch(endpoint)
    const response = await request.json()

    if (response.message == "Removed from my list") {

       const parent = event.target.parentElement.parentElement.parentElement
       parent.remove()
    }

    alert(response.message)
}