const express = require('express');
const axios = require('axios');
const cors = require('cors')

const PORT = 5100;
const chat = 'http://chat:5200'
const app = express();

// Demonstraion tag list
const taglist = ["events","excursions" , "news" ,
                "weather", "music" ,
                "gifts", "food" , "today_dinner",
                "locations" , "what_to_do",
                "make_coffee", "whattosee",
                "virus_todo" , "whats new" ,
                "whattolisten" , "walk"];
app.use(cors({
    origin: ['http://localhost:3000', 'http://localhost:8080', 'http://localhost:4200']
}))
app.use(express.json());

app.post('/test', async (req, res) =>
{
    res.status(200).json({message: "Всё работает"});
});

app.post('/message/bot', async (req, res) =>
{
    axios.post(`${chat}/bot`, {message: req.body.message})
        .then((rest) =>
        {
            // Check returned tag
            point = false;
            for(i = 0; i < taglist.length; i++)
                if(rest.data.ints == taglist[i])
                    point = true;

        if(point)
        {
            // Get recommendation
            axios.post(`${chat}/tag`, {message: req.body.message})
                .then((restag) =>
                {
                    res.status(200).json({message: rest.data.message,
                        audio: rest.data.audio,
                        tags: restag.data.tags });
                })
                .catch((err) =>
                {
                    console.log("err tag");
                });
        }
        else
        {
            res.status(200).json({message: rest.data.message,
                audio: rest.data.audio,
                tags: ['Nan'] });
        }
        }).catch((err) =>
        {
            console.log(err)
            res.status(200).json({message: "Ошибка подключения к боту"});
         });
});

app.listen(PORT, error=>{
    error? console.log(error): console.log(`Listening port ${PORT}`)
});

