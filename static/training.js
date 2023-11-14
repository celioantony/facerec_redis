window.addEventListener('load', function () {

    // flag if is training
    const isTraining = document.querySelector("#id_training").getAttribute("training") == 'true' || false;

    // tag controls in video
    const controls = document.querySelector('.controls');
    const buttons = [...controls.querySelectorAll('button')];
    const [play, pause, screenshot] = buttons;
    // constrols in video
    const inputControls = document.querySelector('.input-controls');
    // options devices to camera
    const cameraOptions = document.querySelector('.video-options>select');
    const video = document.querySelector('video');
    const canvas = document.querySelector('canvas');
    // screenshot preview
    const screenshotImage = document.querySelector('#screenshot-image');
    const screenshotPreview = document.querySelector('.screenshot-preview');
    const animationPhoto = document.querySelector('#display-cover-overlay');

    const buttonsInput = [...inputControls.querySelectorAll('button')]
    const training = document.querySelector('#send-training');
    const resetTraining = document.querySelector('#reset-training');
    const inputFacename = document.querySelector('#input-facename');
    const trainingPreview = $(".training-preview")
    const TRAINING_LIMIT = 20 // seconds
    let streamStarted = false;
    let trainingImages = [];


    const [save, edit] = buttonsInput;

    // enable animation if is training
    if (isTraining)
        animationPhoto.classList.remove('d-none');

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

        startStreamFn(updatedConstraints);
    };

    play.onclick = () => {

        if (streamStarted) {
            video.play();
            play.classList.add('d-none');
            pause.classList.remove('d-none');
            resetTraining.classList.add('d-none');
            return;
        }

        if ('mediaDevices' in navigator && navigator.mediaDevices.getUserMedia) {
            const updatedConstraints = {
                ...constraints,
                deviceId: {
                    exact: cameraOptions.value
                }
            };

            startStreamFn(updatedConstraints);

            animationPhoto.classList.remove('d-none');
            screenshotPreview.classList.add('d-none');

            $(".preview-name").html("");
        }

    };

    const pauseStreamFn = () => {
        video.pause();
        play.classList.remove('d-none');
        pause.classList.add('d-none');
        animationPhoto.classList.add('d-none');

        pauseStreamTrainingFn();
    };

    const startStreamFn = async (constraints) => {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleStreamFn(stream);
    };


    const handleStreamFn = (stream) => {
        video.srcObject = stream;
        play.classList.add('d-none');
        pause.classList.remove('d-none');
        screenshot.classList.remove('d-none');

        handleStreamTrainingFn();
    };

    // const handleRecognitionFn = () => {
    //     const blob = base64ToBlobFn(screenshotImage.src);

    //     var formData = new FormData();
    //     formData.append('file', blob);

    //     $.ajax({
    //         type: 'POST',
    //         url: 'http://localhost:8000/facerec/facerecognition',
    //         data: formData,
    //         async: false,
    //         contentType: false,
    //         processData: false,
    //         success: function (response) {
    //             displayMessages(response.messages);
    //             if (response.recognized_names.length > 0) {
    //                 $(".preview-name").html("Olá, <br>" + response.recognized_names[0]);
    //             }
    //         },
    //         error: function (error) {
    //             console.log(error);
    //         }
    //     });
    // }

    const handleTrainingFn = () => {

        var facename = inputFacename.value;
        var formData = new FormData();
        formData.append('facename', facename);
        trainingImages.forEach((item, index) => {
            let blob = base64ToBlobFn(item);
            formData.append(`files[]`, blob);
        });

        $.ajax({
            type: 'POST',
            url: '/facerec/uploadtraining',
            data: formData,
            async: false,
            contentType: false,
            processData: false,
            success: function (response) {
                displayMessages(response.messages);
            },
            error: function (error) {
                console.log(error);
            }
        });
    }

    const handleScreenshotFn = () => {

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

        handleScreenshotTrainingFn();

    };


    const getCameraSelectionFn = async () => {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        const options = videoDevices.map(videoDevice => {
            return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
        });
        cameraOptions.innerHTML = options.join('');
    };


    // cron

    let hour = 0;
    let minute = 0;
    let second = 0;
    let millisecond = 0;
    let cron;

    const elHour = document.querySelector('#hour');
    const elMinute = document.querySelector('#minute');
    const elSecond = document.querySelector('#second');
    const elMillisecond = document.querySelector('#millisecond');
    let screenshotInter;

    const formatFn = (value) => {
        return value >= 10 ? value : `0${value}`
    }

    const timerFn = () => {
        if ((millisecond += 10) == 1000) {
            millisecond = 0;
            second++;
        }
        if (second == 60) {
            second = 0;
            minute++;
        }
        if (minute == 60) {
            minute = 0;
            hour++;
        }

        if (second == TRAINING_LIMIT) {
            pauseCronFn();
            clearInterval(screenshotInter);
            pauseStreamFn();
            training.classList.remove('d-none');
        }

        elHour.innerText = formatFn(hour);
        elMinute.innerText = formatFn(minute);
        elSecond.innerText = formatFn(second);
        elMillisecond.innerText = formatFn(millisecond);
    }

    const startCronFn = () => {
        cron = setInterval(() => { timerFn(); }, 10)
        screenshotInter = setInterval(() => {
            handleScreenshotFn();
        }, 2000);
    }

    const pauseCronFn = () => {
        clearInterval(cron);
        resetCronFn();
    }

    const resetCronFn = () => {
        hour = 0;
        minute = 0;
        second = 0;
        millisecond = 0;

        elHour.innerHTML = '00';
        elMinute.innerHTML = '00';
        elSecond.innerHTML = '00';
        elMillisecond.innerHTML = '0000';
    }

    // TRAINING PAGE

    const handleStreamTrainingFn = () => {
        // if page is training
        if (isTraining) {
            screenshot.classList.add('d-none');
            edit.classList.add('d-none');
            trainingImages = [];
            startCronFn();
        }
    }

    const pauseStreamTrainingFn = () => {
        if (isTraining) {
            pauseCronFn();
            clearInterval(screenshotInter);
            play.classList.add('d-none');
            resetTraining.classList.remove('d-none');
        }
    }

    const handleScreenshotTrainingFn = () => {
        // if it's training
        if (isTraining) {
            trainingImages.push(canvas.toDataURL('image/png'));
            previewImages(canvas.toDataURL('image/png')); // preview images
            setTimeout(() => {
                screenshotPreview.classList.add('d-none');
            }, 1200);
        }
    }

    const resetTrainingFacesFn = () => {
        trainingImages = [];
        inputFacename.value = '';
        trainingPreview.html('');
        training.classList.add('d-none');
        inputFacename.removeAttribute('disabled', 'disabled');
        save.classList.remove('d-none');
        resetTraining.classList.add('d-none');
    }

    const previewImages = (base64img) => {
        // image preview
        $div = $('<div class="col animate__animated animate__backInRight"></div>');
        $img = $(`<img width="60" src="${base64img}" class="img-thumbnail">`)
        $a = $(`<a href="${base64img}" data-lightbox="roadtrip" data-title=""></a>`);
        $a.html($img);
        $div.append($a);

        trainingPreview.append($div);
    }

    const facenameSaveFn = () => {

        value = inputFacename.value;

        if (value == '' || value == undefined || value == null) {
            message("Campo é obrigatório.", "warning");
            return;
        }

        if (value.length < 4) {
            message("Campo deve ter no mínimo 4 caracteres.", "warning");
            return;
        }

        play.classList.remove('d-none');
        inputFacename.setAttribute('disabled', 'disabled')
        save.classList.add('d-none');
        edit.classList.remove('d-none');
    }

    const facenameEditFn = () => {
        play.classList.add('d-none');
        inputFacename.removeAttribute('disabled', 'disabled')
        save.classList.remove('d-none');
        edit.classList.add('d-none');
    }

    // call

    getCameraSelectionFn();

    // camera
    pause.onclick = pauseStreamFn;
    screenshot.onclick = handleScreenshotFn;
    training.onclick = handleTrainingFn;

    // face training
    save.onclick = facenameSaveFn;
    edit.onclick = facenameEditFn;
    resetTraining.onclick = resetTrainingFacesFn;

});