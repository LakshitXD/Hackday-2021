
const http = require('http');
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));
var test =[{
  "id":"1000"}
];
app.use(express.json());
app.use(express.static("express"));
app.use(express.static('public'));
app.get('/data',function(request,response){
  response.status(200).send(test);
})
app.post('/yeye',function(request,response){
test =request.body;
const {spawn}=require('child_process');
const childPython=spawn('python',['compare1.py']);

childPython.stdout.on('data', (data) => {
    console.log(parseFloat(data,16));
});

childPython.stderr.on('data',(data)=>{
    console.error('stderr: +(data)');
});
response.send("success");
})

const server = http.createServer(app);
const port = 3000;
server.listen(port);
console.debug('Server listening on port ' + port);