var AuthService = function (Api) {
    var authService = {};

    authService.login = function (credentials) {
        return Api.post('authorize', credentials);
    };

    authService.register = function (reg_data) {
        return Api.put('users', reg_data)
    };

    authService.getUser = function () {
        return Api.get('users/me');
    };

    return authService;
};
app.factory('AuthService', ['Api', AuthService]);
