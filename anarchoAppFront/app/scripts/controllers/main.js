'use strict';
var MainCtrl = function ($rootScope, $scope, $cookieStore, $timeout, AUTH_EVENTS, Session, AuthService) {

    $rootScope.showLoader = function () {
        $scope.progressTimeout = $timeout(function () {
            $scope.showProgress = true;
        }, 1000);
    };

    $rootScope.hideLoader = function () {
        $scope.showProgress = false;
        $timeout.cancel($scope.progressTimeout);
    };

    $rootScope.isLoading = function () {
        return $scope.showProgress;
    };

    $scope.loadUser = function () {
        if (Session.isAuthorized()) {
            AuthService.getUser().then(function (user) {
                $scope.currentUser = user;
                $rootScope.hideLoader();
            }).catch(function () {
                $rootScope.hideLoader();
            });
        }
    };

    $scope.$on(AUTH_EVENTS.loginSuccess, function () {
        $scope.loadUser();
    });

    $scope.$on(AUTH_EVENTS.logoutSuccess, function () {
        $scope.currentUser = null;
    });

    $scope.loadUser();
};

app.controller('MainCtrl', [
    '$rootScope',
    '$scope',
    '$cookieStore',
    '$timeout',
    'AUTH_EVENTS',
    'Session',
    'AuthService',
    MainCtrl]);


