var UrlService = function (configuration) {
    var urlService = {};
    urlService.getBuildUrl = function (build) {
        if (build.id != null)
            return configuration.API_URL + "apps/" + build.app_key + "/" + build.id;
    };
    return urlService;
};
app.factory('UrlService', ['configuration', UrlService]);

