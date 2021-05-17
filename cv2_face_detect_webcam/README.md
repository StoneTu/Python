## 使用opencv 內建人臉辨識模型進行辨識
## 網頁開啟webcam版本
建立日期04/27/2021<br>
實作例子，由網頁開啟鏡頭，將影像傳輸到後端進行辨識，將辨識後的圖像顯示於網頁，需要預先安裝好opencv，目前使用版本為4.5.2，
node 版本為v14.15.5<br>
1. 
    建立python script <br>
內容說明:

第一步，載入分類器與從視訊盡頭擷取影片
```
# 載入分類器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
```
第二步，由於影像是網頁提供過來，這裏的輸入需要能接收stdin，轉換為opencv的numpy array
```
lines = sys.stdin.readlines()
lines = [line.rstrip() for line in lines]
lines = ''.join(lines)
lineL = lines.split(",")
num = lineL[0]
lines = lineL[1]
lines = lines.encode('utf-8')
lines = base64.b64decode(lines)
lines = np.frombuffer(lines, dtype="uint8").reshape(-1,1)
img = cv2.imdecode(lines, cv2.IMREAD_UNCHANGED)
```
這裏有個num變數是用來紀錄網頁呼叫的識別用序號，功能為記錄每次呼叫辨識整體需要的時間<br>
第三步，辨識臉部，辨識眼睛，最後將影像輸出
```
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
    # time.sleep(1)
ret, jpeg = cv2.imencode('.jpg', img)
rJpeg = jpeg.tobytes()
rJpeg = base64.b64encode(rJpeg).decode('utf-8')
print(f"{num},{rJpeg}")
```
此部分的重點為將frame numpy的陣列資料，先轉為jpg格式，接著轉為bytes格式，再轉為base64字串，如此才能夠在網頁顯示出來

2. 
    建立node server與前端網頁，這裏會使用網頁開啟使用者鏡頭，會在每次傳送影像時紀錄時間，監測每次整個影像傳輸辨識的過程時間花費
```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="/_js/webcam.min.js"></script>
...
<button id="startCamBtn">Start Camera</button>
<div id="cameraDiv"></div>
<button id="okButton">Send Image</button><hr>
<div>
    <img id="displayImg" src="" alt="">
    <p id="displayText"></p>
</div>
```
在網頁引用webcam.min.js的script，並建立img tag用來顯示我們前面python script的輸出

```
function startCam() {
    // WebCam 啟動程式
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 90
    });
    Webcam.attach('#cameraDiv');
}
```
此處為網頁啟動webcam的啟動程式，可以設定影像的大小，格式，影像品質等
```
function webCamSnap(runNo) {
    var beginTime = new Date().getTime();
    storeNum.push(beginTime);
    Webcam.snap(function (snappedImage) {
        // console.log("snappedImage",snappedImage);
        var imageString = snappedImage.split(",")[1];
        var data = {num:runNo,imageString:imageString};
        $.post("/getImage", data, function(receive) {
            displayImg.src = `data:image/jpeg;base64,${receive.imageString}`;
            var resInt = parseInt(receive.result);
            var deltaTime = new Date().getTime() - storeNum[resInt];
            displayText.innerText ="Send"+receive.result + " delta time: "+(deltaTime/1000)+"sec";
            });
    });  // End of Webcam.snap
}
```
上述程式碼為網頁webcam抓取影像，並且由post方法傳送到server端，由於抓取影像是以字串型態，僅需要去除一小段不需要的標頭部分，並且紀錄時間下來．

接收回傳的影像同時紀錄時間，顯示影像與時間差．
```
app.post("/getImage", function(req, res) {
    var num = req.body.num;
    console.log("[POST] IN "+num)
    var imageString = req.body.imageString;
    const child = spawn('python3', ['./python/opencv_in_img.py']);
    child.stdin.write(num+","+imageString+"\n");
    child.stdin.end();
    num += 1;
    const rl = readline.createInterface({ input: child.stdout });
    rl.on('line', data => {
        var imageString = data.toString('base64');
        var splitL = imageString.split(",");
        numRes = splitL[0]
        imageString = splitL[1]
        res.send({result: `${numRes}`,imageString:imageString});
    });
    child.on('exit', (code) => {
        console.log(`Child process exited with code ${code}, num:${numRes}`);
    });
    child.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
});
```
這裏是使用spawn啟動python script，影像是由stdin輸入字串的方式給python進行人臉辨識，接收stdout的輸出影像字串，回傳給網頁顯示出來<br>
3.
    啟動網頁來看看成果，可以觀察到時間差由0.6秒增加到到1.多看來不是很理想，下次繼續優化時間差的版本<br>
    <video controls="controls" width="300"
                    name="Video Name" src="./cv2_face_detect_webcam.mov"></video>

https://user-images.githubusercontent.com/50975121/118421948-c64ad300-b6f4-11eb-8842-21423fa4ce9f.mov
