const Webcam = {
    set : function( object ) {
        self.videoMode = (object.video==undefined) ? { facingMode: "user" }: object.video;
        self.width = (object.width==undefined) ? 640: object.width;
        self.height = (object.height==undefined) ? 480: object.height;
        self.image_format = (object.image_format==undefined) ? 'jpeg': object.image_format;
        self.videoEle = document.createElement("video");
        self.videoEle.id = (object.height==undefined) ? "camVideo": object.id;
    },
    attach: function ( cssString ) {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: self.videoMode })
                // navigator.mediaDevices.getUserMedia({ video: { facingMode: { exact: "environment" } }})
                .then(function (stream) {
                    self.attachNode = $(cssString)[0];
                    var video = self.videoEle;
                    video.setAttribute('autoplay', '');
                    video.setAttribute('muted', '');
                    video.setAttribute('playsinline', '');
                    video.style = `width: ${self.width}px; height: ${self.height}px;`;
                    video.srcObject = stream;
                    $(cssString).html("");
                    $(cssString).append(video);
                    $(cssString).attr('width', `${self.width}`);
                })
                .catch(function (err0r) {
                    console.log("Attach Failed! Error: "+err0r);
                });
        }
    },
    snap: function(callback) {
        var canvas = document.createElement('canvas');
        canvas.width = self.width;
        canvas.height = self.height;
        var ctx = canvas.getContext('2d');
        //draw image to canvas. scale to target dimensions
        ctx.drawImage(self.videoEle, 0, 0, canvas.width, canvas.height);
        //convert to desired file format
        var dataURI = canvas.toDataURL(`image/${self.image_format}`); // can also use 'image/png'
        callback(dataURI);
    },
    stopBothVideoAndAudio: function() {
        stream = self.videoEle.srcObject
        stream.getTracks().forEach(function(track) {
            if (track.readyState == 'live') {
                track.stop();
            }
        });
        self.attachNode.innerHTML = "";
    }
}
