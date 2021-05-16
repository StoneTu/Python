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
    setInterval(() => {
        webCamSnap(num);
        num += 1
    }, 300);
}
function webCamSnap(runNo) {
    var beginTime = new Date().getTime();
    storeNum.push(beginTime);
    Webcam.snap(function (snappedImage) {
        // console.log("snappedImage",snappedImage);
        var imageString = snappedImage.split(",")[1];
        // console.log("imageString",imageString);
        var data = {num:runNo,imageString:imageString};
        $.post("/getImage", data, function(receive) {
            displayImg.src = `data:image/jpeg;base64,${receive.imageString}`;
            var resInt = parseInt(receive.result);
            var deltaTime = new Date().getTime() - storeNum[resInt];
            displayText.innerText ="Send"+receive.result + " delta time: "+(deltaTime/1000)+"sec";
            // sendFrameInterval();
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