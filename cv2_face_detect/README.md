## 使用opencv 內建人臉辨識模型進行辨識

建立日期04/26/2021<br>
實作例子，建立node.js express server，啟動由python opencv 開啟鏡頭進行辨識，將辨識後的圖像顯示於網頁，需要預先安裝好opencv，目前使用版本為4.5.2，
node 版本為v14.15.5<br> 
socket.io 版本為4.0.1<br>
1. 
    建立python script <br>
內容說明
第一步，載入分類器與從視訊盡頭擷取影片
```
# 載入分類器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
# 從視訊盡頭擷取影片
cap = cv2.VideoCapture(0)
```
第二步，建立一個while迴圈，讀取frame，辨識臉部，辨識眼睛，最後將影像輸出
```
i = 0
while i<10:
    i+=1
    # Read the frame
    _, img = cap.read()
    # 轉成灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 偵測臉部
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # 繪製人臉部份的方框
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        h1=int(float(h/1.5))
        gray_facehalf = gray[y:(y+h1), x:x+w]
        eyes = eye_cascade.detectMultiScale(gray_facehalf, 1.1, 4)
        # 繪製眼睛方框
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(img, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 0, 0), 2)
        # 顯示成果
    ret, jpeg = cv2.imencode('.jpg', img)
    rJpeg = jpeg.tobytes()
    rJpeg = base64.b64encode(rJpeg).decode('utf-8')
    # 將影像轉為字串輸出stdout
    print(rJpeg)
# Release the VideoCapture object
cap.release()
```
此部分的重點為將frame numpy的陣列資料，先轉為jpg格式，接著轉為bytes格式，再轉為base64字串，如此才能夠在網頁顯示出來

2. 
    建立node server與前端網頁，這裡將會使用socket.io作為通訊的方式，這是我目前嘗試最能real time即時顯示影像的方式
```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
...
...
<body>
    <img id="image" width="600px">
</body>
```
在網頁引用jquery與socket.io，並建立img tag用來顯示我們前面python script的輸出

```
$.post('/runcam', {}, function(data) {
    const socket = io();
    socket.on('image', (image) => {
        console.log('ready to get image:');
        const imageElement = document.getElementById('image');
        imageElement.src = `data:image/jpeg;base64,${image}`;
    });
});
```
建立一個java script，或直接寫在html script tag內，發送post並建立socket.io的連線，用來接收image資料，並顯示在img tag
```
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
```
在node server加上上述程式碼，才能使用socket.io通訊

```
let { PythonShell } = require('python-shell')
app.post('/runcam', function(req, res){
    io.on("connection", (socket) => {
        console.log("Made socket connection");
        var pyshell = new PythonShell('./out_opencv_io2.py');
        pyshell.on('message', data => {
            var imageString = data.toString('base64');
            socket.emit('image', imageString);
        });
        pyshell.end(function (err) {
            if (err){
                throw err;
            };
            console.log('finished');
        });
    }); 
    res.send('ok');
});
```
在server端建立接收post的服務，這裏使用PythonShell來啟動前面預先建立好的python script，啟動python script也有其他方法如child process spawn
```
const { spawn } = require('child_process');
const readline = require('readline');
app.post('/runcam', function(req, res){
    io.on("connection", (socket) => {
        console.log("Made socket connection");
        const child = spawn('python3', ['./out_opencv_io2.py']);
        const rl = readline.createInterface({ input: child.stdout });
        rl.on('line', data => {
            var imageString = data.toString('base64');
            socket.emit('image', imageString);
        });
        child.on('exit', (code) => {
            console.log(`Child process exited with code ${code}`);
        });
        child.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
    });
    res.send('ok');
});
```
這裏是使用spawn啟動python script的寫法<br>
3.
    如此便接近成功，啟動網頁來看看成果．
    <video controls="controls" width="300"
                    name="Video Name" src="./cv2_face_detect.mov"></video>