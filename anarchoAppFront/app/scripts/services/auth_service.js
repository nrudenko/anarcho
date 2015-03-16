var AuthService = function (Api) {
    var authService = {};

    authService.login = function (credentials) {
        return Api.post('login', credentials);
    };

    authService.register = function (reg_data) {
        return Api.post('register', reg_data)
    };

    authService.getUser = function () {
        return Api.get('user');
    };

    return authService;
};
app.factory('AuthService', ['Api', AuthService]);
