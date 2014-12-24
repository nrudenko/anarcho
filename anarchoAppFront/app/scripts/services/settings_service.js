var SettingsService = function (Api) {
    var settingsService = {};

    settingsService.add = function (user_app) {
        return Api.post('permission', user_app);
    };

    settingsService.update = function (user_app) {
        return Api.patch('permission', user_app);
    };

    settingsService.revoke = function (user_app) {
        return Api.delete("permission", user_app);
    };

    settingsService.list = function (app_key) {
        return Api.get("permission/" + app_key);
    };
    return settingsService;
};

app.factory('SettingsService', ['Api', SettingsService]);
