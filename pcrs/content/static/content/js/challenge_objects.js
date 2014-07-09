var $uiselected = null;


$(document).ready(function () {

    $(document).on('click', '.item', select);

    $(document).on('click', '#add-page', addPage);
    $(document).on('click', '.delete-page', deletePage);
    $(document).on('click', '.remove_item', deleteItemHelper);

    $(document).on('click', '#add-text', addText);
    $(document).on('click', '#save-text', saveText);

    $(document).on('click', '#save_top', savePages);
    $(document).on('click', '#save_bot', savePages);

    $('.btn-object-visibility').on('click', change_problem_visibility);

    $(".page").sortable({
        connectWith: ".page",
        update: function (event, ui) {
            $('#save_top').prop('disabled', false);
            $('#save_bot').prop('disabled', false);
            resize_problems();
        }
    });

    $(".items").sortable({
        connectWith: ".page"
    });

    // make pages selectable
    $("#challenge").selectable({
        selecting: function (event, ui) {
            // allow only one page to be selected
            if ($(".ui-selected, .ui-selecting").length > 1) {
                $(ui.selecting).removeClass("ui-selecting");
            }
        }});

    // bind deletion of items to d key
    $(document).keypress(
        function (event) {
            if (event.which == 100 && $uiselected != null) {
                deleteItem($($uiselected));
            }
        });

    resize_problems();
});

function resize_problems(){
    $('.available_problems').height($('.ui-selectable').height()-$('.available_problems').find('.nav-tabs').height());
}

function select(event) {
    if ($uiselected != null) {
        $uiselected.toggleClass('uiselected');
    }
    $uiselected = $(event.target).parent('.item');
    $uiselected.toggleClass('uiselected');
}

function addPage() {
    $.post(document.URL + '/page/create', {csrftoken: csrftoken})
        .success(function (data) {
            $new_item = $("<div/>", {
                class: "page well",
                id: "page-" + data['pk']
            });
            $delete = $("<i/>", {
                class: "delete-page glyphicon glyphicon-remove pull-right"
            });
            $new_item.prepend($delete);
            $('#challenge').append($new_item);
            $new_item.sortable({
                connectWith: ".page",
                update: function (event, ui) {
                    $('#save_top').prop('disabled', false);
                    $('#save_bot').prop('disabled', false);
                    resize_problems();
                }
            });
        });
}

function deletePage() {
    if (confirm('Are you sure you would like to delete this page?')) {
        $item = $(this).parent('.page');
        $.post(document.URL + '/' + $item.attr('id') + '/delete')
            .success(function (data) {
                $item.remove();
                resize_problems();
            });
    }
}

function addText() {
    $uiselected = null;
    var $page = $('.ui-selected');
    if ($page.length == 0) {
        alert('Please select the page you would like to add the text to.')
    }
    else {
        $('#text-entry-modal').modal();
        console.log($('#text-entry-modal'));
        resize_problems();
    }
}

function saveText(event) {
    var $page = $('.ui-selected');

    $.post(document.URL + '/' + $page.attr('id') + '/text/create', {
        text: $('#text-entry').val(),
        csrftoken: csrftoken
    })
        .success(function (data) {
            var $new_item = $("<div/>", {
                html: "<p class='ui-selectee'>" + $('#text-entry').val() + "</p>",
                class: "textblock item well ui-selectee",
                id: "textblock-" + data['pk']
            });
            $new_item.prepend($("<button/>",{
                class: "btn btn-object-close btn-xs glyphicon glyphicon-remove remove_item ui-selectee pull-right",
                title: "Delete Item"
            }))
            $page.append($new_item);
            $('#save_top').prop('disabled', false);
            $('#save_bot').prop('disabled', false);
        });
}

function deleteItemHelper(){
    deleteItem($(this).parent());
}

function deleteItem($item) {
    var id = $item.attr('id');
    // if text
    if (id.match('^textblock')) {
        $.post(document.URL + '/' + id + '/delete', {csrftoken: csrftoken})
            .success(function () {
                $item.remove()
            });
    }
    // video or problem: put the item back into the appropriate list
    if (id.match('^video')) {
        $('#videos').append($item.remove());
    }
    // problem
    if (id.match('^problem')) {
        var list_id = id.match('[^-]*'); // match up to the dash
        $('#' + list_id).append($item.remove());
    }
    $item.toggleClass('uiselected');
    $uiselected = null;
    $('#save_top').prop('disabled', false);
    $('#save_bot').prop('disabled', false);
    resize_problems();
}

function savePages() {
    var page_object_list = $.map(
        $('.page'),
        function (el, i) {
            return [$.grep($(el).sortable('toArray'),
                function (e, i) {
                    return e != ''
                })];
        }
    );

    $.post(document.URL + '/pages', {
        page_object_list: JSON.stringify(page_object_list),
        csrftoken: csrftoken
    }).success(function () {
        $('#save_bot').attr('disabled', 'disabled');
        $('#save_top').attr('disabled', 'disabled');
    });
}

function change_problem_visibility(){
    var parent_id = $(this).parent('div').attr('id');
    var current_problem_type = parent_id.split("-")[0];
    var current_problem_pk = parent_id.split("-")[1];
    var this_button = this;
    var send_data = {problem_type:current_problem_type,
                     problem_pk:current_problem_pk,
                     csrftoken: csrftoken};
    $.post(document.URL + '/change_status', send_data)
        .success(function (data) {
            var new_visibility = data['new_visibility'];
            var old_visibility = data['old_visibility'];
            if (old_visibility == 'open'){
                $(this_button).removeClass('visibility-open glyphicon-eye-open');
                $(this_button).addClass('visibility-'+new_visibility+' glyphicon-eye-close');
            }
            else{
                $(this_button).removeClass('visibility-'+old_visibility+' glyphicon-eye-close');
                if (new_visibility == "open"){
                    $(this_button).addClass('visibility-'+new_visibility+' glyphicon-eye-open');
                }
                else{
                    $(this_button).addClass('visibility-'+new_visibility+' glyphicon-eye-close');
                }
            }

            $(this_button).prop('title', "Visibility "+new_visibility);
        });
}