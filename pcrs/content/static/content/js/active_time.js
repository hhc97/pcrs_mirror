window.addEventListener('focus', gotFocus);
window.addEventListener('unload', lostFocus);
window.addEventListener('blur', lostFocus);

var start_time = new Date().getTime();

function gotFocus() {
    start_time = new Date().getTime();
}

function lostFocus() {
    var curr_time = new Date().getTime();
    var elapsed_time = curr_time - start_time;
    $.post(window.location.href + "/activetime",
        {csrftoken: csrftoken, elapsed_time: elapsed_time});
}
