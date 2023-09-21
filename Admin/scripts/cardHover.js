const cardBody = document.querySelectorAll('.card-body')

     document.querySelectorAll('.card').forEach(cardDiv => {


        cardDiv.onmouseenter = function(e) {
            console.log("chilD:", e.target.children[1])
            const target = e.target.children[1]
            target.style.opacity = 1
            target.style.visibility = "visible"

            e.target.style.marginLeft = "2rem"
        }


        cardDiv.onmouseleave = function(e) {

            const target = e.target.children[1]
            target.style.opacity = 0
            target.style.visibility = "hidden"

            e.target.style.marginLeft = "0"
        }

})