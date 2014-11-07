var AppsService = function (Api) {
    var appService = {};

    appService.list = function () {
        return Api.get('apps');
    };

    appService.add = function (app) {
        return Api.post('apps', app);
    };

    appService.get = function (appKey) {
        return Api.get('apps/' + appKey);
    };

    appService.getBuilds = function (appKey) {
        return Api.get('apps/' + appKey + "/builds");
    };

    appService.uploadBuild = function (appKey, file, progress, success) {
        Api.uploadBuild('apps/' + appKey, file, progress, success);
    };

    appService.removeBuilds = function (appKey, ids) {
        return Api.delete('apps/' + appKey + "/builds", {ids: ids});
    };
    return appService;
};

app.factory('AppsService', ['Api', AppsService]);
