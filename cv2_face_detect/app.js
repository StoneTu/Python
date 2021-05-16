const http = require("http");
const express = require('express');
const path = require('path');
const app = express();
const fs = require('fs');
let { PythonShell } = require('python-shell')
const { spawn } = require('child_process');
const readline = require('readline');
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(express.static(__dirname + '/public'));

const socket = require("socket.io");
const server = http.createServer(app);
// const io = socket(server); // This not work.
const io = socket(server, {
    cors: {
        origin: "http://localhost:3001",
        methods: ["GET", "POST"],
        transports: ['websocket', 'polling'],
        credentials: true
    },
    allowEIO3: true
});
server.listen(3001, () => {
    console.log('Express started')
});
app.get('/', function(req, res){
    res.render("realtime",{});
});
app.get('/realtime', function(req, res){
    res.render("realtime",{});
});
app.get('/run', function(req, res) {
    const child = spawn('python3', ['./out_opencv_jpg.py']);
    res.redirect("/img/image.jpg");
});
app.use('/img', express.static(__dirname+'/public/image/'));

app.post('/runcam', function(req, res){
    io.on("connection", (socket) => {
        console.log("Made socket connection");
        var pyshell = new PythonShell('./out_opencv_io2.py');
        pyshell.on('message', data => {
            // console.log('out a image', typeof data); // string
            var imageString = data.toString('base64');
            socket.emit('image', imageString);
        });
        pyshell.end(function (err) {
            if (err){
                throw err;
            };
            console.log('finished');
        });

        // PythonShell.run('./out_opencv_io2.py', {}, (err, data) => {
        //     var imageString = "";
        //     var dataA = data.toString('base64');
        //     socket.emit('image', dataA);
        // });
    }); 
    res.send('ok');
});
app.post('/runcam2', function(req, res){
    io.on("connection", (socket) => {
        console.log("Made socket connection");
        // socket.emit("ferret", "tobi", (data) => {
        //     console.log(data); // data will be "woot"
        // });
        setInterval(function () {
            socket.emit('second', { 'second': new Date().getSeconds() });
        }, 1000);

        // Following code execute python code in node.js
        console.log('[IN] /py');
        const child = spawn('python3', ['./out_opencv_io2.py']);
        var imageString = "";
        const rl = readline.createInterface({ input: child.stdout });
        rl.on('line', data => {
            // console.log('out a image', typeof data); // string
            var dataA = data.toString('base64');
            imageString = dataA;
            socket.emit('image', imageString);
        });
        // child.stdout.on('data', function(data) {
        //     // var decodedImage = new Buffer(data, 'base64').toString('binary');
        //     console.log('out a image', typeof data); // object
        //     // var dataA = Buffer.from(data, 'binary').toString('base64');
        //     var dataA = Buffer.from(data, 'base64');
        //     imageString += dataA;
        //     // console.log("data:", dataA); // string
        //     socket.emit('image', imageString);
        // });
        child.on('exit', (code) => {
            console.log(`Child process exited with code ${code}`);
        });
        child.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
    });
    res.send('ok');
});