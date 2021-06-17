const express = require("express");
var db = require('./db')
const app = express();
app.use(express.json({limit: '10mb'})); /// add limit to prevent PayloadTooLargeError: request entity too large
app.use(express.urlencoded({limit: '10mb',extended: false}));
app.use(express.static(__dirname+"/public"));
app.set("views", __dirname+"/views");
app.set("view engine", "ejs");
// run python with pythonshell
// let { PythonShell } = require('python-shell')

// run python with spawn
const { spawn } = require('child_process');
const readline = require('readline');


// app.listen(3000, function() {
//     console.log("Starting server...")
// });

// run express https server
const fs = require("fs");
const https = require("https");
const { parse } = require("path");
var hskey = fs.readFileSync('pillaAuth-key.pem', 'utf8');
var hscert = fs.readFileSync('pillaAuth-cert.pem', 'utf8');
var credentials = {
    key: hskey,
    cert: hscert
}
const server = https.createServer(credentials, app);

// run with socket.io
// const socket = require("socket.io");
// const io = socket(server, {
//     cors: {
//         origin: "wss://localhost:3000",
//         // origin: "https://localhost:3000",
//         methods: ["GET", "POST"],
//         transports: ['websocket', 'polling'],
//         credentials: true
//     },
//     allowEIO3: true
// });

server.listen(3000, function() {
    console.log("Express https server listening on port "+3000);
});

app.get("/", function(req, res) {
    res.render("index", {});
});

/// following code using spawn to run python
// var num = 0;
app.post("/faceLogin", async function(req, res) {
    console.log("[login IN]");
    const child = spawn('python3', ['./python/faceLogin.py']); // move to outside post
    var result = await db.findAsync();
    // result = JSON.parse(result);  // for fs write
    var nameList = [], face_descriptor = [];
    for (var singleData of result) {
        nameList.push(singleData.userName);
        face_descriptor.push(singleData.face_descriptor);
    }
    var imageString = req.body.imageString;
    child.stdin.write(imageString+"\n");
    child.stdin.write(nameList+"\n");
    child.stdin.write(face_descriptor+"\n");
    const rl = readline.createInterface({ input: child.stdout });
    var dataJson = {code:1};
    rl.on('line', data => {
        console.log("[login PY return]");
        var dataString = data.toString('base64');
        dataJson = JSON.parse(dataString);
        console.log(dataJson);
        rl.close(); // make readline stop, this's very important step.
        rl.removeAllListeners(); // make readline stop, this's very important step.
        // var backJSON = {code:200, result: "Welcome back Jack"};
    }); 
    child.on('exit', (code) => {
        dataJson.code = code;
        res.send(dataJson);
        console.log(`Face login Child process exited with code ${code}`);
    });
    child.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
});
app.post("/faceRegister", function(req, res) {
    var imageString = req.body.imageString;
    var userName = req.body.userName;
    const childReg = spawn('python3', ['./python/register.py']); // move to outside post
    childReg.stdin.write(imageString+"\n");
    const rl = readline.createInterface({ input: childReg.stdout });
    rl.on('line', async function(data) {
        var dataString = data.toString('base64');
        var dataJson = JSON.parse(dataString);
        rl.close(); // make readline stop, this's very important step.
        rl.removeAllListeners(); // make readline stop, this's very important step.
        var dbJson = {userName: userName,
            face_descriptor: dataJson[0]};
        // console.log("dbJson:",dbJson);
        var result = await db.findAsync();
        // var result = JSON.parse(resultStr);  // for fs write
        var nameList = [];
        for (var singleData of result) {
            nameList.push(singleData.userName);
        }
        if (nameList.indexOf(userName)==-1) {
            // dbJson = JSON.stringify(dbJson); // for fs write
            // dbJson = resultStr.slice(0,-1)+","+dbJson+"]"; // for fs write
            var result = await db.insertOneAsync(dbJson);
            var backJSON = {code:200, result:"Regiser ok."};
            // var result = db.insertOne(dbJson)
        } else {
            var backJSON = {code:0, result:'Name existed.'};
        }
        // console.log("findAll:",result, typeof result);
        res.send(backJSON);
    }); 
    childReg.on('exit', (code) => {
        console.log(`Register Child process exited with code ${code}`);
    });
    childReg.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
});
