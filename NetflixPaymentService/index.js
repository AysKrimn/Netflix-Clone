const express = require('express')
const app = express()
const port = 8080


// middleware
app.use(express.urlencoded({ extended: true}))
app.use(express.json())


app.get('/', (req, res) => {
  res.send('Hello World!')
})



const cards = [

    {
        id: 13211,
        cardNo: "1221123123",
        cardName: "Ömer Ocak",
        valid: "05/23",
        cvv: 123,
        amount: 65
    },

    {
        id: 13211342,
        cardNo: "1221124124",
        cardName: "Burak Işık",
        valid: "02/23",
        cvv: 341,
        amount: 12
    }
]

app.get('/api/cards', (request, response) => {


    response.json(cards)

})


app.post('/api/cards', (request, response) => {

        console.log("body:", request.body)
        const { cardNo, price } = request.body


        const data = cards.find(card => card.cardNo === cardNo)

        console.log("gelen veri:", data)

        
        if (data) {
            // parayı çek
            data.amount -= price;
            if (data.amount >= price) { response.json(data); console.log("user:", data) }
        

            else {

                return response.json({ error: "Bakiye yetersiz"})
            }

        } else {

            const data = {
                error: "Böyle bir kart numarası mevcut değil"
            }

            response.json(data)
        }




})


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})