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
    //$.post(location + "/activetime",
    //    {csrftoken: csrftoken, elapsed_time: elapsed_time})
    let data = new FormData();
    data.append('csrftoken', csrftoken);
    data.append('csrfmiddlewaretoken', csrftoken);
    data.append('elapsed_time', elapsed_time);
    navigator.sendBeacon(location + "/activetime", data);

    // header:
    // X-CSRFToken: vDtM0dRbFptcNdQmDiv96cXiYGU3vVXwjfWat9rdJ0bDEPSLHIMHGfaj47gGfG5e
}
