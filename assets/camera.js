document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('camera-button').addEventListener('click', function () {
        let video = document.createElement('video');
        let canvas = document.createElement('canvas');
        let context = canvas.getContext('2d');
        
        navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
            video.srcObject = stream;
            video.play();

            setTimeout(() => {
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                let image_data = canvas.toDataURL('image/png');
                let inputElement = document.getElementById('input-on-submit');
                inputElement.value = image_data;
                inputElement.dispatchEvent(new Event('change'));
                stream.getTracks().forEach(track => track.stop());
            }, 2000);  // Adjust the delay as needed
        });
    });
});
