$(document).ready(function() {
    $("form").submit(function(e) {
        e.preventDefault();
        $("input[type='submit']").prop('disabled', true);
        if ($("#output").length) {
            $("#output").html("Running your code<span class='dots'><i>.</i><i>.</i><i>.</i></span>");
        }
        var a = $(this);
        $.post($(this).attr('action'), $(this).serialize(), function(data) {
            if (data.redirect) {
                window.location.href = data.redirect;
            }
            if (data.clippy) {
                $("#clippy span").html(data.clippy);
                $("#clippy").fadeIn();
            }
            if (data.error) {
                a.find('.alert').html(data.error).addClass('alert-danger').show();
            }
            if (data.output) {
                $('#output').html(data.output);
            }
        }, 'json').always(function() {
            $("input[type='submit']").prop('disabled', false);
        }).fail(function() {
            a.find('.alert').html('Unknown error!').addClass('alert-danger').show();
        });
    });
});
