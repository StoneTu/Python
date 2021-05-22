const express = require("express");
const app = express();
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(express.static(__dirname+"/public"));
app.set("views", __dirname+"/views");
app.set("view engine", "ejs");
// run python with pythonshell
let { PythonShell } = require('python-shell')

// run python with spawn
const { spawn } = require('child_process');
const readline = require('readline');

app.get("/", function(req, res) {
    res.render("webPage", {});
});

/// following code using spawn to run python
// var num = 0;
var numRes;
// const child = spawn('python3', ['./python/opencv_in_img.py']);
// const child = spawn('python3', ['./python/test.py']);

app.post("/getImage", function(req, res) {
    var nodeTime = new Date().getTime();
    var num = req.body.num;
    var webTime = req.body.time;
    // timeList = JSON.parse(timeList);
    console.log("[POST] IN "+num+" web time: "+webTime)
    var imageString = req.body.imageString;
    const child = spawn('python3', ['./python/opencv_in_img_once.py']); // move to outside post
    child.stdin.write(num+","+imageString+"\n");
    child.stdin.end(); // This will only work once.
    num += 1;
    const rl = readline.createInterface({ input: child.stdout });
    rl.on('line', data => {
        // console.log('out a image', typeof data); // string
        var imageString = data.toString('base64');
        var splitL = imageString.split(",");
        numRes = splitL[0]
        imageString = splitL[1]
        pythonTime = new Date().getTime();
        // res.send({imageString:imageString});
        console.log("[POST] OUT");
        res.send({result: `${numRes}`,imageString:imageString, time: [webTime, nodeTime, pythonTime]});
    });
    child.on('exit', (code) => {
        console.log(`Child process exited with code ${code}, num:${numRes}`);
    });
    child.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
});

// app.post("/getImage", function(req, res) {
//     var imageString = req.body.imageString;
//     var pyshell = new PythonShell('./python/opencv_in_img.py');
//     pyshell.send(imageString);
//     pyshell.on('message', data => {
//         // console.log('out a image', typeof data); // string
//         var imageString = data.toString('base64');
//         res.send({imageString:imageString});
//     });
//     pyshell.end(function (err) {
//         if (err){
//             throw err;
//         };
//         console.log('finished');
//     });

// });

app.listen(3000, function() {
    console.log("Starting server...")
});