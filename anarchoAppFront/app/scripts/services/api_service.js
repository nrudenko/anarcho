var api = function ($http, $upload, configuration, Session) {
    var api = {};

    api.getBaseConfig = function (action) {
        var config = {
            url: configuration.API_URL + action,
            headers: {}
        };

        var authToken = Session.authToken;
        if (authToken != null) {
            config.headers['x-auth-token'] = authToken;
        }
        return  config;
    };

    api.delete = function (action, data) {
        var config = api.getBaseConfig(action);
        config.headers['Content-Type']='application/json;charset=utf-8';
        config['method'] = 'DELETE';
        config['data'] = data;
        return $http(config);
    };

    api.post = function (action, data) {
        var config = api.getBaseConfig(action);
        config.headers['Content-Type']='application/json;charset=utf-8';
        config['method'] = 'POST';
        config['data'] = data;
        return $http(config);
    };

    api.patch = function (action, data) {
        var config = api.getBaseConfig(action);
        config['method'] = 'PATCH';
        config['data'] = data;
        return $http(config);
    };

    api.get = function (action) {
        var config = api.getBaseConfig(action);
        config['method'] = 'GET';
        return $http(config);
    };

    api.uploadBuild = function (action, file, progress, success) {
        var config = api.getBaseConfig(action);
        return $upload.upload({
            url: config.url, //upload.php script, node.js route, or servlet url
            method: 'POST',
            headers: config.headers,
            //withCredentials: true,
            //data: {myObj: $scope.myModelObj},
            file: file // or list of files ($files) for html5 only
            //fileName: 'doc.jpg' or ['1.jpg', '2.jpg', ...] // to modify the name of the file(s)
            // customize file formData name ('Content-Desposition'), server side file variable name.
            //fileFormDataName: myFile, //or a list of names for multiple files (html5). Default is 'file'
            // customize how data is added to formData. See #40#issuecomment-28612000 for sample code
            //formDataAppender: function(formData, key, val){}
        }).progress(function (evt) {
            progress(parseInt(100.0 * evt.loaded / evt.total));
        }).success(function (data, status, headers, config) {
            // file is uploaded successfully
            success(data);
        })
    };

    return api;
};

app.factory('Api', ['$http', '$upload', 'configuration', 'Session', api]);
