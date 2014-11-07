var TeamService = function (Api) {
    var teamService = {};

    teamService.add = function (user_app) {
        return Api.post('permission', user_app);
    };

    teamService.update = function (user_app) {
        return Api.patch('permission', user_app);
    };

    teamService.revoke = function (user_app) {
        return Api.delete("permission", user_app);
    };

    teamService.list = function (app_key) {
        return Api.get("permission/" + app_key);
    };
    return teamService;
};

app.factory('TeamService', ['Api', TeamService]);
