$(document).ready(function() {
    function waitVis() {
        if (visPostComplete) {
            $('#waitingModal').modal('hide');
            if (pythonVisError) {
                $('#visualizerModal').modal('hide');
            }
        }
        else {
            setTimeout(waitVis, 100);
        }
    }

    var code_wrapper = $('.code-mirror-wrapper')[0];
    var code_wrapper_id = code_wrapper.id;

    $(code_wrapper).children('#grade-code').hide();

    checkLanguageFromContainerId(code_wrapper_id);

    if (language == "python"){
        myCodeMirrors[code_wrapper_id] = to_code_mirror(language, 3, $(code_wrapper).find("#div_id_code_box"), '', false);
        $(code_wrapper).find('#submit-id-trace').hide()
        $(code_wrapper).append($('<button id="python_trace_btn" class="debugBtn pull-right" type="button" data-target="#visualizerModal">Trace</button>'));
        $('#python_trace_btn').bind('click', function() {
            var div_id = $(this).parents('.code-mirror-wrapper')[0].id;
            var user_code = myCodeMirrors[div_id].getValue();
            if (user_code == '') {
                alert('There is no code to submit.');
            } else {
                $('#waitingModal').modal('show');
                getVisualizerComponents(user_code, '', 9999999);
                $('#visualizerModal').modal('show');
                setTimeout(waitVis, 100);
            }
        });
    }
    else if (language == "c") {
        myCodeMirrors[code_wrapper_id] = to_code_mirror(language, 'text/x-csrc', $(code_wrapper).find("#div_id_code_box"), '', false);
        myCodeMirrors[code_wrapper_id].getDoc().setValue("#include <stdio.h>\n\nint main() {\n\n    return 0;\n}");

        preventDeleteLastLine(code_wrapper_id);

        $(code_wrapper).find('#submit-id-trace').click(function(event) {
            event.preventDefault();
            var div_id = $(this).parents('.code-mirror-wrapper')[0].id;

            var user_code = myCodeMirrors[div_id].getValue();
            if (user_code == '') {
                alert('There is no code to submit.');
            } else {
                // FIXME this method no longer exists
                getTestcases(div_id);
            }
        });
    }
    else if (language == "ra" || language == "sql") {
        myCodeMirrors[code_wrapper_id] = to_code_mirror(language, 'text/x-sql', $(code_wrapper).find("#div_id_code_box"), '', false);

        if (language == "ra") {
            myCodeMirrors[code_wrapper_id].getDoc().setValue("\\project_{eid} sales;");
        }
        else {
            myCodeMirrors[code_wrapper_id].getDoc().setValue("select eid from sales;");
        }

        $(code_wrapper).find('#submit-id-trace').click(function(event) {
            event.preventDefault();
            var div_id = $(this).parents('.code-mirror-wrapper')[0].id;

            var user_code = myCodeMirrors[div_id].getValue();
            if (user_code == '') {
                alert('There is no code to submit.');
            } else {
                getTestcases(div_id);
            }
        });
    }
});

function start_editor_visualizer(user_code, code_wrapper_id) {
    var postParams = { 'language' : language, 'user_code' : user_code };

    executeGenericVisualizer("gen_execution_trace_params", postParams, '');

    visualizerDetailsTarget = '/visualizer-details-editor';
    $.post(root + '/editor' + visualizerDetailsTarget,
            postParams,
            function(data) {
                executeGenericVisualizer("create_visualizer", data, user_code);
            },
        "json")
     .fail(function(jqXHR, textStatus, errorThrown) { console.log(textStatus); });
}

/**
 * Check the language of a problem container. (the id of the main_div)
 */
function checkLanguageFromContainerId(containerId) {
    if (containerId.indexOf("c") > -1){
        return 'c';
    } else if (containerId.indexOf("python") > -1){
        return 'python';
    } else if (containerId.indexOf("java") > -1){
        return 'java';
    } else if (containerId.indexOf("sql") > -1){
        return 'sql';
    } else if (containerId.indexOf("ra") > -1){
        return 'ra';
    } else {
        throw new Error('Could not detect language of ' + containerId + '!');
    }
}

