var AuthCtrl = function ($scope, $rootScope, AUTH_EVENTS, AuthService, Session) {

    $scope.login = function (credentials) {
        AuthService.login(credentials)
            .success(function (data) {
                Session.create(data.authToken);
                $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
            }).error(function (data) {
                $scope.error = data.error;
                $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
            });
    };

    $scope.register = function (regData) {
        AuthService.register(regData)
            .success(function (data) {
                Session.create(data.authToken);
                $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
            }).error(function (data) {
                $scope.error = data.error;
                $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
            });
    };

    $scope.logout = function () {
        Session.destroy();
        $rootScope.$broadcast(AUTH_EVENTS.logoutSuccess);
    };

};
app.controller('AuthCtrl', [
    '$scope',
    '$rootScope',
    'AUTH_EVENTS',
    'AuthService',
    'Session',
    AuthCtrl
]);