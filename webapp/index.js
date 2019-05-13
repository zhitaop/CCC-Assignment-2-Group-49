const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const session = require('express-session');
const request = require('request');
const fs = require('fs')

const app = express();
const portNum = process.env.PORT || 3000;

let dbname = 'twitter_data'
let processed_dbname = 'twitter_processed'

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.use(express.static(path.join(__dirname, 'web')));

// {rows: [{name: 'city', count: num}, ...]}  {rows: [{coordinates: [x,y]}, ...]}
app.get('/s',function(req, res){
    
    res.sendFile(path.join(__dirname, '/web/index.html'));
});
app.get('/get',function(req, resp){
    request('http://localhost:5984/twitter_processed/_design/wrath/_view/wrath_tweets?group=true', (err, res, body)=>{
        if (err) {console.log(err);}

        request('http://localhost:5984/twitter_processed/_design/wrath/_view/wrath_tweets?reduce=false', (err, res, body)=>{
            
            body = JSON.parse(body)
            let coords = [];
            for (let row of body.rows) {
                coords.push(row.value);
            }
            //console.log('Wrath sum1:', body.total_rows);
            //console.log(coords)    
    })


        data = JSON.parse(body)
        let sum = 0
        for (let row of data.rows) {
            sum += row.value
        }
        data.total_count = sum;
        console.log('Wrath sum~~~~:', sum);

        fs.writeFileSync('web/wrathTweets.json', JSON.stringify(data))

        //rese.json(data)

        request('http://localhost:5984/twitter_processed/_design/negative/_view/negative_score?group=true', (err, res, body)=>{
            if (err) {console.log(err);}
    
            data = JSON.parse(body)
            let sum = 0
            for (let row of data.rows) {
                sum += row.value
            }
            console.log('negative sum~~~~:', sum);
            data.total_count = sum;
    
            fs.writeFileSync('web/negative_Tweets.json', JSON.stringify(data))
    
            request('http://localhost:5984/twitter_data', (err, res, body) => {
                if (err) console.log(err)

                //console.log(res)
                console.log(JSON.parse(body).doc_count);

                request('http://localhost:5984/twitter_processed', (err, res, body) => {
                    if (err) console.log(err)
    
                    //console.log(res)
                    console.log(JSON.parse(body).doc_count);

                    resp.sendFile(path.join(__dirname, '/web/index.html'));

                });
            });
    
        });

    });

});


app.get('/getview',function(req, resp){
    request('http://localhost:5984/'+processed_dbname+'/_design/wrath/_view/wrath_tweets?group=true', (err, res, body)=>{
        if (err) {console.log(err);}
        
        fs.writeFileSync('web/wrath_tweets.json', body)

        request('http://localhost:5984/'+processed_dbname+'/_design/wrath/_view/wrath_tweets?reduce=false', (err, res, body)=>{
            
            fs.writeFileSync('web/wrath_tweets_coords.json', body)
            let wrathCount = JSON.parse(body).total_rows;    
            console.log('Wrath sum~~~~:', wrathCount);

            request('http://localhost:5984/'+processed_dbname+'/_design/sentiment/_view/sentiment?group=true', (err, res, body)=>{

                fs.writeFileSync('web/sentiment.json', body)
                console.log(body)
                })

            request('http://localhost:5984/'+processed_dbname+'/_design/negative/_view/negative_score?reduce=false', (err, res, body)=>{
                if (err) {console.log(err);}
        
                data = JSON.parse(body)
                console.log('negative sum~~~~:', data.rows.length);
                let negativeCount = data.rows.length;
        
                //fs.writeFileSync('web/negative_Tweets.json', JSON.stringify(data))
        
                request('http://localhost:5984/'+dbname, (err, res, body) => {
                    if (err) console.log(err)
    
                    //console.log(res)
                    let totalCount = JSON.parse(body).doc_count;
                    console.log(JSON.parse(body).doc_count);
    
                    request('http://localhost:5984/'+processed_dbname, (err, res, body) => {
                        if (err) console.log(err)
        
                        //console.log(res)
                        let vicCount = JSON.parse(body).doc_count;
                        console.log(JSON.parse(body).doc_count);
    
                        resp.render('index', {
                            totalCount: totalCount,
                            vicCount: vicCount,
                            wrathCount: wrathCount,
                            negativeCount: negativeCount
                        });    
                    });
                });        
            });
        });
    });
});


app.listen(portNum, function(){
    console.log('Server started on port '+portNum);
});