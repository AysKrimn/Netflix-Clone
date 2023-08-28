    // modaldaki videoları oynat
    function playShortVideo(movieId) {
        // movieId'e göre video tagını çek
        const video = document.getElementById(`movie-${movieId}`)
        // muteyi kaldır
        video.muted = false;
        // sesi 0.5 olarak ayarla
        video.volume = 0.5;
        // video oynat
        video.play()

        // kapanadığı zaman yapılması gerekenleri söyle
        const modal = document.getElementById(`exampleModal-${movieId}`)
        modal.addEventListener('hidden.bs.modal', function() {

          // videoyu durdur
          video.pause()
        })
      }