function displayMessages(htmlMessages) {
    const elMessages = $("#ajaxmessages");
    elMessages.html(htmlMessages).delay(2000).fadeOut(500, function () {
        $("#ajaxmessages").html("");
        $("#ajaxmessages").removeAttr("style");
    });
}

function message(msg, type) {
    $divMsg = $('<div id="id_messages" class="messages"></div>');
    $divAlert = $(`<div class="alert alert-${type} animate__animated animate__fadeInUp" role="alert"></div>`);

    $divAlert.html(msg)
    $divMsg.html($divAlert);

    displayMessages($divMsg)
}

// declare all characters
const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function generateString(length) {
    let result = ' ';
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}

function base64ToBlobFn(dataURI) {
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

function lettersOnly(event) {
    var charCode = event.keyCode;

    if ((charCode > 64 && charCode < 91) || (charCode > 96 && charCode < 123) || charCode == 8)
        return true;
    else
        return false;
}