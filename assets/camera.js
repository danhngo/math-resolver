window.onload = function () {
    let cameraButton = document.getElementById('camera-button');
    if (cameraButton) {
        cameraButton.addEventListener('click', function () {
            let video = document.createElement('video');
            let canvas = document.createElement('canvas');
            let context = canvas.getContext('2d');
            
            navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
                video.srcObject = stream;
                video.play();

                video.addEventListener('loadeddata', () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    let image_data = canvas.toDataURL('image/png');
                    
                    // Update the hidden input with the base64 image data
                    let inputElement = document.getElementById('input-on-submit');
                    if (inputElement) {
                        inputElement.value = image_data;
                        inputElement.dispatchEvent(new Event('change'));
                    }
                    
                    // Stop the video stream
                    stream.getTracks().forEach(track => track.stop());
                });
            }).catch(err => console.log('An error occurred: ' + err));
        });
    } else {
        console.log('Camera button not found');
    }
};
