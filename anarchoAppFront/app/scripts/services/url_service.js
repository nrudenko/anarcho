var UrlService = function (configuration) {
    var urlService = {};
    urlService.getBuildUrl = function (app_key, build) {
        if (build.id != null)
            return configuration.API_URL + "apps/" + app_key + "/" + build.id;
    };

    urlService.getUploadUrl = function (app_key) {
        return configuration.API_URL + "apps/" + app_key;
    };

    return urlService;
};
app.factory('UrlService', ['configuration', UrlService]);

