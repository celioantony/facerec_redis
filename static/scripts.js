function displayMessages(htmlMessages) {
    const elMessages = $("#ajaxmessages");
    elMessages.html(htmlMessages).delay(2000).fadeOut(500, function () {
        $("#ajaxmessages").html("");
        $("#ajaxmessages").removeAttr("style");
    });
}