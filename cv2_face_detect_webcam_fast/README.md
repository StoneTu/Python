## 使用opencv 內建人臉辨識模型進行辨識
## 網頁開啟webcam版本 優化回應速度
建立日期05/15/2021<br>
實作例子，由網頁開啟鏡頭，將影像傳輸到後端進行辨識，將辨識後的圖像顯示於網頁，改善回應速度過慢的問題
<br>需要預先安裝好opencv，目前使用版本為4.5.2，
node 版本為v14.15.5<br>
1. 
    建立python script ，請參考前一例子說明<br>

2. 
    建立node server與前端網頁，請參考前一例子說明<br>
3. 
    優化速度：
    之前程式為每次呼叫都重新開一次python程式，這裏改為只有第一次開啟python程式，之後的影像資料由stdin傳送．改寫如下．
```
var numRes;
const child = spawn('python3', ['./faceView/nodeDriverDetect.py']);
app.post("/getImage", function(req, res) {
    var nodeTime = new Date().getTime();
    var num = req.body.num;
    var webTime = req.body.time;
    // timeList = JSON.parse(timeList);
    console.log("[POST] IN "+num+" web time: "+webTime)
    var imageString = req.body.imageString;
    // const child = spawn('python3', ['./python/opencv_in_img.py']); // move to outside post
    child.stdin.write(num+","+imageString+"\n");
    // child.stdin.end(); // This will only work once.
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
        rl.close(); // make readline stop, this's very important step.
        rl.removeAllListeners(); // make readline stop, this's very important step.
        res.send({result: `${numRes}`,imageString:imageString, time: [webTime, nodeTime, pythonTime]});
    });
    child.on('exit', (code) => {
        console.log(`Child process exited with code ${code}, num:${numRes}`);
    });
    child.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
});
```
首先將child process移到外圍，於server啟動時就開啟，並等待stdin<br>
將child.stdin.end();拿掉，
在每次python script回傳時，加入下面程式，應該兩種擇一即可，移除readline的listener，避免下一次的回傳有兩個listener回應．
rl.close();
rl.removeAllListeners();
3.
    啟動網頁來看看成果，可以觀察到優化時間差的版本時間差由0.6秒降到到0.1以下<br>
    <video controls="controls" width="300"
                    name="Video Name" src="./cv2_face_detect_webcam_fast.mov"></video>