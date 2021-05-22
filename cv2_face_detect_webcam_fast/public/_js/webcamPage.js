var storeNum = [];
var num = 0;
$(document).ready(function () {
    startCamBtn.onclick = startCam;
    // okButton.onclick = webCamSnap;
    okButton.onclick = sendFrameInterval;
    // $("#okButton").on("click", webCamSnap );
    
})
function sendFrameInterval() {
    // webCamSnap(num);
    // num+=1;
    // var intervalID = setInterval(() => {
        webCamSnap(num);
        num += 1
        if (num>200) { 
            num = -1; //end python
            // clearInterval(intervalID);
        }
    // }, 50);
}
function webCamSnap(runNo) {
    var beginTime = new Date().getTime();
    storeNum.push(beginTime);
    Webcam.snap(function (snappedImage) {
        // console.log("snappedImage",snappedImage);
        var imageString = snappedImage.split(",")[1];
        // console.log("imageString",imageString);
        var data = {num:runNo,time:beginTime,imageString:imageString};
        $.post("/getImage", data, function(receive) {
            var webTime = receive.time[0];
            var nodeTime = receive.time[1];
            var pyTime = receive.time[2];
            displayImg.src = `data:image/jpeg;base64,${receive.imageString}`;
            var resInt = parseInt(receive.result);
            var webToNodeTime = nodeTime - webTime;
            var nodeToPyTime = pyTime - nodeTime;
            var pyToWebTime = new Date().getTime() - pyTime;
            var outStr = "Send"+receive.result + " web to node time: "+webToNodeTime;
            outStr += ` node to py time: ${nodeToPyTime}`;
            outStr += ` py to web time: ${pyToWebTime}`;
            displayText.innerText = outStr;
            sendFrameInterval();
        });
    });  // End of Webcam.snap
}
function startCam() {
    // WebCam 啟動程式
    Webcam.set({
        // width: 160,
        // height: 120,
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 90
    });
    Webcam.attach('#cameraDiv');
}