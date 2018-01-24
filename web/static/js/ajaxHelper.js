
function make_base_auth(user, password) {
    var tok = user + ':' + password;
    var hash = btoa(tok);
    return "Basic " + hash;
}

function AjaxHelper() {
    
    function get(url, data, username, password,  onSuccess, onError) {
        client(url, data, "GET", username, password, onSuccess, onError);
    };

    function post(url, data, username, password, onSuccess, onError) {
        client(url, data, "POST", username, password, onSuccess, onError);
    };

    function patch(url, data, username, password, onSuccess, onError) {
        client(url, data, "PATCH", username, password, onSuccess, onError);
    };

    function client(url, data, type, username, password, onSuccess, onError) {
        $.ajax
            ({
                type: type,
                url: url,
                dataType: 'json',
                async: true,
                data: data,
                name: username,
                password: password,
                success: onSuccess,
                error: onError,
                beforeSend: function (xhr){ 
                    xhr.setRequestHeader('Authorization', make_base_auth(username, password)); 
                },
            });
    }

    return {
        get: get,
        post:post,
        patch:patch
    };
}




