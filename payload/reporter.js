context.reporter = function(context, name, data, callback=null) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", context.options['callback_url'], true);
    xhr.setRequestHeader("Content-type", "application/json");

    xhr.onreadystatechange = function() {
        if (callback != null)
            callback(xhr)
    }
    var to_send = JSON.stringify({
        uid: context.options['uid'],
        name: name,
        data: data
    });
    xhr.send(to_send);
};