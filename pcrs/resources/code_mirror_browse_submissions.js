$(document).ready(function() {
    var code_el = $('div.code');
    for (var index = 0; index < code_el.length; index++){
        language = code_el[index].id.split("_")[0];
        value = code_el[index].innerHTML;
        history_code_mirror (language, language, code_el[index], value, true)
    }
});