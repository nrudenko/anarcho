var AppsService = function (Api) {
    var appService = {};

    appService.list = function () {
        return Api.get('apps');
    };

    appService.add = function (app) {
        return Api.post('apps', app);
    };

    appService.removeApp = function (appKey) {
        return Api.delete('apps/' + appKey);
    };

    appService.get = function (appKey) {
        return Api.get('apps/' + appKey);
    };

    appService.getBuilds = function (appKey) {
        return Api.get('apps/' + appKey + "/builds");
    };

    appService.uploadBuild = function (appKey, file, progress, success) {
        return Api.uploadBuild('apps/' + appKey, file, progress, success);
    };

    appService.removeBuilds = function (appKey, ids) {
        return Api.delete('apps/' + appKey + "/builds", {ids: ids});
    };

    appService.getPluginConfig = function (appKey) {
        return Api.get('apps/' + appKey + "/plugin");
    };

    appService.getBuild = function (appKey, buildId) {
        return Api.get('apps/' + appKey + "/" + buildId);
    };

    appService.postNotes = function (appKey, buildId, notes) {
        return Api.post('apps/' + appKey + "/" + buildId + "/notes", {release_notes: notes});
    };

    return appService;
};

app.factory('AppsService', ['Api', AppsService]);
