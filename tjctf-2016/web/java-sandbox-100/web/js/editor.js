$(document).ready(function() {
    var hasStorage = typeof(Storage) !== "undefined";
    $("#code").hide();
    var editor=ace.edit('editor');
    if (hasStorage) {
        var code = localStorage.getItem("code");
        if (code) {
            editor.getSession().setValue(code);
        }
        else {
            editor.getSession().setValue($("#template").text());
        }
    }
    else {
        editor.getSession().setValue($("#template").text());
    }
    $('#code').val(editor.getSession().getValue());
    editor.setTheme('ace/theme/monokai');
    editor.getSession().setMode('ace/mode/java');
    editor.getSession().on('change', function() {
        $('#code').val(editor.getSession().getValue());
        if (hasStorage) {
            localStorage.setItem("code", $("#code").val());
        }
    });
    var trash;
    $("#reset-code").click(function(e) {
        e.preventDefault();
        trash = editor.getSession().getValue();
        localStorage.setItem("code", "");
        editor.getSession().setValue($("#template").text());
        $("#output").html("Code deleted! Click <a href='#' id='undo-code'>here</a> to undo.");
    });
    $(document).on("click", "#undo-code", function(e) {
        e.preventDefault();
        editor.getSession().setValue(trash);
        $("#output").html("Code undeleted! Press \"Run Code\" to run your code.");
    });
});
