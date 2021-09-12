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
    var location = window.location.href.split('#')[0];
    $.post(location + "/activetime",
        {csrftoken: csrftoken, elapsed_time: elapsed_time})
     .fail(function(response) {
        console.log("Error: Cannot log elapsed time")});         // Likely lost authentication, so we'll lose that data.
}
