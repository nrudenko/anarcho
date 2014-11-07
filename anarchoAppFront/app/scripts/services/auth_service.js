var AuthService = function (Api) {
    var authService = {};

    authService.login = function (credentials) {
        return Api.post('login', credentials)
            .then(function (res) {
                return res.data;
            }, function (error) {
                throw error.data;
            });
    };

    authService.register = function (reg_data) {
        return Api.post('register', reg_data)
            .then(function (res) {
                return res.data;
            }, function (error) {
                throw error.data;
            });
    };

    authService.parseUser = function (res) {
        var user = {};
        user.name = res.data.name;
        user.id = res.data.id;
        return user;
    };

    authService.getUser = function () {
        return Api.get('user')
            .then(function (res) {
                return authService.parseUser(res);
            }, function (error) {
                throw error;
            });
    };

    return authService;
};
app.factory('AuthService', ['Api', AuthService]);
