SubmissionWrapper.prototype._getTestcasesCallback = function(data) {
    // use_simpleui is global... gur.
    if (use_simpleui == 'False' && this._shouldUseGradeTable()) {
        this.wrapperDiv.find("#grade-code").show();
    }

    var score = data['score'];
    var max_score = data['max_score'];

    if ( ! this.isEditor) {
        var $alertBox = this.wrapperDiv.find('#alert');
        $alertBox.show();
        var decider = score == max_score;

        $alertBox.toggleClass("red-alert", ! decider);
        $alertBox.toggleClass("green-alert", decider);
        $alertBox.children('icon').toggleClass("remove-icon", ! decider);
        $alertBox.children('icon').toggleClass("ok-icon", decider);

        if (decider) {
            $alertBox.children('span').text("Your submission is correct!");

            this.wrapperDiv
                .find('.screen-reader-text')
                .prop('title', 'Your solution is correct!');
        } else {
            var resultText = "Your solution passed " +
                score + " out of " + max_score + " cases!";

            $alertBox.children('span').text(resultText);
            this.wrapperDiv.find('.screen-reader-text').prop(resultText);
        }
    }

    this.prepareGradingTable({
        'testcases': data['results'][0],
        'best_score': data['best'],
        'max_score': max_score,
        'past_dead_line': data['past_dead_line'],
        'sub_pk': data['sub_pk'],
        'error_msg': data['results'][1] || null,
    });
}      

SubmissionWrapper.prototype.getTestcases = function(code) {
    var call_path = root + '/problems/' + this.language + '/' + this.wrapperDivId.split("-")[1]+ '/fixit';
    var postParams = { csrftoken: csrftoken, submission: code };

    // Activate loading pop-up
    $('#waitingModal').modal('show');

    var that = this;
    $.post(call_path,
            postParams,
            function(data) {
                that._getTestcasesCallback(data);
                // Deactivate loading pop-up
                $('#waitingModal').modal('hide');
            },
        "json")
     .fail(
        function(jqXHR, textStatus, errorThrown) {
            // Deactivate loading pop-up
            $('#waitingModal').modal('hide');
        });
}
