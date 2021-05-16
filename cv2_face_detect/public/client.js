console.log("this is client");
function runCam() {
      console.log("run Camera");
      $.post('/runcam', {}, function(data) {
            console.log("response:", data);
            const socket = io();
            socket.on('second', function (second) {
                $('#second').text(second.second);
            });
            socket.on("ferret", (name, fn) => { // fn work for returning data to server.
                  console.log("client:", name);
                  fn("woot");  
            });
            socket.on('image', (image) => {
                  console.log('ready to get image:');
                  const imageElement = document.getElementById('image');
                  // console.log(imageElement);
                  imageElement.src = `data:image/jpeg;base64,${image}`;
            
            });
      });
}