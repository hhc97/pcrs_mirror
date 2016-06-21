function PythonSubmissionWrapper(name) {
    SubmissionWrapper.call(this, name);
    this.language = "python";
    this.language_version = 3;
}
PythonSubmissionWrapper.prototype = Object.create(SubmissionWrapper.prototype);
PythonSubmissionWrapper.prototype.constructor = PythonSubmissionWrapper;

/**
 * @override
 */
PythonSubmissionWrapper.prototype._showEditorTraceDialog = function(code) {
    var code = this.getAllCode();
    $('#waitingModal').modal('show');
    getVisualizerComponents(code, '', 9999999);
    $('#visualizerModal').modal('show');
    setTimeout(PythonSubmissionWrapper._waitVis, 100);
}

// TODO At some point, this should be a callback. Polling is bad!
PythonSubmissionWrapper._waitVis = function() {
    if (visPostComplete) {
        $('#waitingModal').modal('hide');
        if (pythonVisError) {
            $('#visualizerModal').modal('hide');
        }
    } else {
        setTimeout(PythonSubmissionWrapper._waitVis, 100);
    }
}

/**
 * @override
 */
PythonSubmissionWrapper.prototype._createTestCaseRow = function(testcase) {
    var $newRow = SubmissionWrapper.prototype._createTestCaseRow.apply(
        this, arguments);

    if ('exception' in testcase) {
        return $newRow;
    }

    $newRow.append('<td class="description">' + testcase.test_desc + '</td>');

    if (testcase.test_input != null) {
        $newRow.append('<td class="expression"><div class="expression_div">' +
                testcase.test_input + '</div></td>');
    } else {
        $newRow.append('<td class="expression">' +
                "Hidden Test" +'</td>');
    }

    var expTestValDiv = $('<div class="ExecutionVisualizer"></div>');
    var testResultDiv = $('<div class="ExecutionVisualizer"></div>');

    $newRow.append($('<td class="expected"></td>')
        .append($('<div class="ptd"></div>')
            .append(expTestValDiv)));
    $newRow.append($('<td class="result"></td>')
        .append($('<div class="ptd"></div>')
            .append(testResultDiv)));

    renderData_ignoreID(testcase.test_val, testResultDiv);
    renderData_ignoreID(testcase.expected_output, expTestValDiv);

    this._addFaceColumnToTestRow($newRow, testcase.passed_test);
    this._addA11yToTestRow($newRow, this._createOutput(testcase.test_val),
        testcase.passed_test, testcase.expected_output);
    this._addDebugColumnToTestRow($newRow, testcase.debug);

    return $newRow;
}

/**
 * @override
 */
PythonSubmissionWrapper.prototype._prepareVisualizer = function(row) {
    var testcaseCode = row.find(".expression_div").text();
    var newCode = myCodeMirrors[this.wrapperDivId].getValue() +
        "\n" + testcaseCode;
    getVisualizerComponents(newCode, testcaseCode, this.problemId);
}

/**
 * @override
 */
PythonSubmissionWrapper.prototype._formatTestCaseObject = function(testcase) {
    testcase = SubmissionWrapper.prototype._formatTestCaseObject.apply(
        this, arguments);
    testcase.expected_output = testcase.expected_output
        ? this._createOutput(testcase.expected_output)
        : null;
    return testcase;
}

/**
 * Convert the given "input" in to a string representing the
 * students python solution.
 */
PythonSubmissionWrapper.prototype._createOutput = function(input) {
    var brakets_o = {"list":"[","tuple":"(","dict":"{"};
    var brakets_c = {"list":"]","tuple":")","dict":"}"};

    if (input.length == 2) {
        return this._createOutput(input[0]) + ":" + this._createOutput(input[1]);
    } else if (input[0] == "list" || input[0] == "tuple" || input[0] == "dict") {
        var output = brakets_o[input[0]];
        for (var o_index = 2; o_index < input.length; o_index++) {
            output += this._createOutput(input[o_index]);
            if (o_index != input.length - 1) {
                output += ", ";
            }
        }
        output += brakets_c[input[0]];
        return output
    } else if (input[0] == "string") {
        return "'" + input[2] + "'";
    } else if(input[0] == "float") {
        if (String(input[2]).indexOf(".") > -1) {
            return input[2];
        } else {
            return input[2] + ".0"
        }
    } else {
        return input[2]
    }
}

