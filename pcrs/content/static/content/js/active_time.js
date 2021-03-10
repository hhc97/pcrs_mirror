window.addEventListener('focus', gotFocus);
window.addEventListener('unload', cpUnloaded);
window.addEventListener('blur', lostFocus);

var start_time = new Date().getTime();
var elapsed_time = 0;

function gotFocus() {
    start_time = new Date().getTime();
}

function lostFocus() {
    var curr_time = new Date().getTime();
    elapsed_time = elapsed_time + (curr_time - start_time);
}

function cpUnloaded() {
    var curr_time = new Date().getTime();
    elapsed_time = elapsed_time + (curr_time - start_time);
    $.post(window.location.href + "/activetime",
        {csrftoken: csrftoken, elapsed_time: elapsed_time});
}