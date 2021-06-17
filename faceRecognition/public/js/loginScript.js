var working, iconHeight;
$(document).ready(function(){
  working = false;
  iconHeight = document.getElementsByClassName("icon")[0].height;
  console.log("get height", iconHeight);
  if (iconHeight==0) 
    iconHeight = 300;
});
$('#signinForm').on('submit', function(e) {  
  console.log("submit");
  e.preventDefault();
  if (working) return;
  working = true;
  var $this = $(this),
    $state = $this.find('button > .state');
  // console.log("$this", $this);
  // $this.addClass('loading');
  $state.html('Authenticating');
  startCam();
  // This if for checking ok.
  setTimeout(function() {
    $this.addClass('loading');
    faceLoginAction();
    Webcam.stopBothVideoAndAudio();
    $('#webcamDiv').html('<img class="icon" src="./images/faceLoginIcon.png">')
  }, 4000);
});
$('#signupForm').on('submit', function(e) {  
  console.log("sign up");
  e.preventDefault();
  if (working) return;
  working = true;
  var $this = $(this),
    $state = $this.find('button > .state');
  console.log("$this", $this);
  console.log("userName.value:",userName.value)
  if (userName.value.length <3) {
    // $this.addClass('loading');
    $state.html('User Name Invalid');
    working = false;  
  } else {
    startCam2();
    $state.html('Registering');
    setTimeout(function() {
      $this.addClass('loading');
      faceRegisterAction(userName.value);
      Webcam.stopBothVideoAndAudio();
      $('#webcamDiv2').html('<img class="icon" src="./images/faceLoginIcon.png">')
    }, 4000);
  }
});
// faceLogin.onclick = startCam;
// faceSignup.onclick = startCam2;
signupTab.onclick = signupTabShow;
signinTab.onclick = signinTabShow;
function startCam() {
  // WebCam 啟動程式
  Webcam.set({
      // width: 160,
      // height: 120,
      width: 320,
      height: iconHeight,
      image_format: 'jpeg',
      jpeg_quality: 90,
      id: 'videoY'
  });
  Webcam.attach('#webcamDiv');
}
function startCam2() {
  // WebCam 啟動程式
  Webcam.set({
      // width: 160,
      // height: 120,
      width: 320,
      height: 240,
      image_format: 'jpeg',
      jpeg_quality: 90,
      id: 'videoY'
  });
  Webcam.attach('#webcamDiv2');
}
function faceRegisterAction(name) {
  Webcam.snap(function (snappedImage) {
    // console.log("snappedImage", snappedImage);
    var imageString = snappedImage.split(",")[1];
    // console.log("imageString",imageString);
    var data = { userName: name, imageString: imageString };
    $.post("/faceRegister", data, function (receive) {
        console.log('receive', receive);
        if (receive.code==200) {
          $("#signupForm").addClass('ok');
          $("#signupText").html(receive.result);
        } else {
          $("#signupText").html(receive.result);
        }
        working = false;  
        setTimeout(function() {
          $("#signupText").html('Face Sign up');
          $("#signupForm").removeClass('ok loading');
        }, 3000);
    });
});  // End of Webcam.snap
}

function faceLoginAction() {
  Webcam.snap(function (snappedImage) {
    // console.log("snappedImage", snappedImage);
    var imageString = snappedImage.split(",")[1];
    // console.log("imageString",imageString);
    var data = { imageString: imageString };
    $.post("/faceLogin", data, function (receive) {
        console.log('receive', receive);
        if (receive.code==0) {
          $("#signinForm").addClass('ok');
          $("#signinText").html("Welcome back "+receive.result);
        } else {
          $("#signinText").html("Authenticating fail");
        }
        working = false;  
        setTimeout(function() {
          $("#signinText").html('Face Log in');
          $("#signinForm").removeClass('ok loading');
        }, 3000);
    });
});  // End of Webcam.snap
}
function webCamSnap() {
  Webcam.snap(function (snappedImage) {
      // console.log("snappedImage", snappedImage);
      var imageString = snappedImage.split(",")[1];
      // console.log("imageString",imageString);
      return imageString;
  });  // End of Webcam.snap
}
function signupTabShow() {
    signinTab.className = "tablinks";
    signupTab.className = "tablinks active";
    signinForm.className = "tabcontent";
    signupForm.className = "";
}
function signinTabShow() {
  signinTab.className = "tablinks active";
  signupTab.className = "tablinks";
  signinForm.className = "";
  signupForm.className = "tabcontent";
}