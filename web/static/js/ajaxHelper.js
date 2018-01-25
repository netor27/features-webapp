function AjaxHelper(username, password) {
    self = this;
    self.username = username;
    self.password = password;

    self.get = function (url, data, onSuccess, onError) {
        client(url, data, "GET", onSuccess, onError);
    };

    self.post = function (url, data, onSuccess, onError) {
        client(url, data, "POST", onSuccess, onError);
    };

    self.patch = function (url, data, onSuccess, onError) {
        client(url, data, "PATCH", onSuccess, onError);
    };

    function client(url, data, type, onSuccess, onError) {
        $.ajax
            ({
                type: type,
                url: url,
                contentType: "application/json",
                accepts: "application/json",
                cache: false,
                dataType: 'json',
                async: true,
                data: data,
                success: onSuccess,
                error: onError,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization',
                    "Basic " + btoa(self.username + ":" + self.password));
                },
            });
    }
}




