$(document).ajaxError(function (event, jqXHR, settings, thrownError) {
    switch (jqXHR.status) {
    case 0:
        alert('Error: A network request could not be completed, either because of a local javascript error or because the network is down or very slow. If you are submitting an exercise, copy (and save) the code, so you do not lose work.');
        break;
    case 403:
         alert('Error: Action did not complete: you need to reauthenticate. If you are submitting an exercise, copy (and save) the code, so you do not lose work, then reload the page.')
         break;
    case 500:
        alert('Error: PCRS request failed due to internal server error. Please contact your instructor with the time of the request, so they can investigate. Also, save any code you are submitting so you do not lose your work.');
        break;
    default:
        alert('Error: Action did not complete. Usually, this occurs when authentication expires. Try loading PCRS in another tab to refresh your session, and then try the action again. If you are submitting an exercise, do not forget to copy (and save) the code, in case your page is reloaded.');
    }
});

var csrftoken = getCookie('csrftoken');
var sessionid = getCookie('sessionid');


    jQuery.ajaxSettings.traditional = true;

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
