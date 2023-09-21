function handleModal(movieId) {

    const movieSource = document.getElementById(`track-${movieId}`)
    movieSource.muted = false
    // sesia yarla
    movieSource.volume = 0.5
    movieSource.play()


    // kapanma talimatını ver
    const modal = document.getElementById(`exampleModal-${movieId}`)

    modal.addEventListener('hidden.bs.modal', function() {
        // videoyu durdur
        movieSource.pause()
    })


  }