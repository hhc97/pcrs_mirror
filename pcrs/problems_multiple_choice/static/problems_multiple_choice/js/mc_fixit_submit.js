
function submit_mc(submission, problem_pk, div_id) {
    /**
     * Submits the students solution to a MC problem
     */

    var postParams = { csrftoken: csrftoken, submission : submission  };
    $.post(root+'/problems/multiple_choice/'+problem_pk+'/fixit',
            postParams,
            function(data) {
                var display_element = $('#multiple_choice-'+problem_pk)
                    .find('#alert');

                var score = data['score'];
                var max_score = data['max_score'];

                var is_correct = score >= max_score;
                $(display_element)
                    .toggleClass('red-alert', !is_correct);
                $(display_element)
                    .toggleClass('green-alert', is_correct);
                $(display_element)
                    .children('icon')
                    .toggleClass('remove-icon', !is_correct);
                $(display_element)
                    .children('icon')
                    .toggleClass('ok-icon', is_correct);
                if (is_correct){
                    $(display_element)
                        .children('span')
                        .text('Your solution is complete.');
                    $('#'+div_id).find('.screen-reader-text').prop('title', 'Your solution is complete.');
                }
                else{
                    var alert_msg = 'Your solution is either incorrect or incomplete!';
                    if (data['error_msg']){
                        alert_msg = data['error_msg'];
                    }
                    $(display_element).children('span').text(alert_msg);
                    $('#'+div_id).find('.screen-reader-text').prop('title', alert_msg);
                }

                mc_options = $('#'+div_id).find('[id^="id_options_"]');

                options_list = []

                for (var opt = 0; opt < mc_options.length; opt++){
                    options_list.push({
                        'selected': $(mc_options[opt]).is(':checked'),
                        'option': $(mc_options[opt]).parents('.checkbox').text()
                    });
                }

                returnable = {
                    'sub_time': new Date(),
                    'score': score,
                    'out_of': max_score,
                    'best': data['best'],
                    'past_dead_line': false,
                    'problem_pk': problem_pk,
                    'sub_pk': data['sub_pk'],
                    'options': options_list
                }
                if (data['best'] && !data['past_dead_line']){
                    update_marks(div_id, score, max_score);
                }

                var flag = ($('#'+div_id).find('#history_accordion').children().length != 0);
                add_mc_history_entry(returnable, div_id, flag)
            },
        "json")
     .fail(function(jqXHR, textStatus, errorThrown) { console.log(textStatus); });
}
