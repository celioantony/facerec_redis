window.addEventListener('load', function () {

    const controls = document.querySelector('.controls');
    const cameraOptions = document.querySelector('.video-options>select');
    const video = document.querySelector('video');
    const canvas = document.querySelector('canvas');
    const screenshotImage = document.querySelector('#screenshot-image');
    const screenshotPreview = document.querySelector('.screenshot-preview');
    const animationPhoto = document.querySelector('#display-cover-overlay');
    const buttons = [...controls.querySelectorAll('button')];
    let streamStarted = false;

    const [play, pause, screenshot] = buttons;

    const constraints = {
        video: {
            width: {
                min: 1280,
                ideal: 1920,
                max: 2560,
            },
            height: {
                min: 720,
                ideal: 1080,
                max: 1440
            },
        }
    };

    cameraOptions.onchange = () => {
        const updatedConstraints = {
            ...constraints,
            deviceId: {
                exact: cameraOptions.value
            }
        };

        startStream(updatedConstraints);
    };

    play.onclick = () => {

        if (streamStarted) {
            video.play();
            play.classList.add('d-none');
            pause.classList.remove('d-none');
            return;
        }
        if ('mediaDevices' in navigator && navigator.mediaDevices.getUserMedia) {
            const updatedConstraints = {
                ...constraints,
                deviceId: {
                    exact: cameraOptions.value
                }
            };
            startStream(updatedConstraints);
            animationPhoto.classList.remove('d-none');
            screenshotPreview.classList.add('d-none');
            $(".preview-name").html("");
        }

    };

    const pauseStream = () => {
        video.pause();
        play.classList.remove('d-none');
        pause.classList.add('d-none');
        animationPhoto.classList.add('d-none');
    };

    const base64ToBlob = (dataURI) => {
        var bytesString = atob(dataURI.split(',')[1]);
        var mime = dataURI.split(',')[0].split(':')[1].split(';')[0];
        var arrayBuffer = new ArrayBuffer(bytesString.length);
        var uint8Array = new Uint8Array(arrayBuffer);

        for (var i = 0; i < bytesString.length; i++) {
            uint8Array[i] = bytesString.charCodeAt(i);
        }

        var blob = new Blob([arrayBuffer], { type: mime });

        return blob;
    }

    const doRecognition = () => {
        const blob = base64ToBlob(screenshotImage.src);

        var formData = new FormData();
        formData.append('file', blob);

        $.ajax({
            type: 'POST',
            url: 'http://localhost:8000/cart/facerecognition',
            data: formData,
            async: false,
            contentType: false,
            processData: false,
            success: function (response) {
                displayMessages(response.messages);
                if (response.recognized_names.length > 0) {
                    $(".preview-name").html("Olá, <br>" + response.recognized_names[0]);
                }
            },
            error: function (error) {
                console.log(error);
            }
        })
    }

    const doScreenshot = () => {

        canvas.width = 200;
        canvas.height = 300;
        const sx = Math.round((video.videoWidth / 2) - ((video.videoWidth / 2) * 0.3))
        const sy = (video.videoHeight * 0.05);
        const sw = (video.videoWidth / 2) * 0.6;
        const sh = video.videoHeight * 0.9;
        const dx = 0;
        const dy = 0;

        
        canvas.getContext('2d').drawImage(video, sx, sy, sw, sh, dx, dy, 200, 300);
        screenshotImage.src = canvas.toDataURL('image/png');
        screenshotImage.classList.remove('d-none');
        // recognition.classList.remove('d-none');
        screenshotPreview.classList.remove('d-none');

        setTimeout(() => {
            doRecognition();
        }, 1000);

        // pauseStream
        pauseStream();
    };

    pause.onclick = pauseStream;
    screenshot.onclick = doScreenshot;
    // recognition.onclick = doRecognition;

    const startStream = async (constraints) => {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleStream(stream);
    };


    const handleStream = (stream) => {
        video.srcObject = stream;
        play.classList.add('d-none');
        pause.classList.remove('d-none');
        screenshot.classList.remove('d-none');

    };


    const getCameraSelection = async () => {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        const options = videoDevices.map(videoDevice => {
            return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
        });
        cameraOptions.innerHTML = options.join('');
    };

    getCameraSelection();
});