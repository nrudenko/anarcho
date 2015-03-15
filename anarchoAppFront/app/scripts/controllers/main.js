'use strict';
var MainCtrl = function ($scope, $cookieStore, $timeout, AUTH_EVENTS, Session, AuthService) {

    $scope.isLoading = false;

    $scope.showLoader = function () {
        $scope.progressTimeout = $timeout(function () {
            $scope.showProgress = true;
        }, 2000);
    };

    $scope.hideLoader = function () {
        $scope.showProgress = false;
        $timeout.cancel($scope.progressTimeout);
    };

    $scope.isMobile = {
        Android: function () {
            return /Android/i.test(navigator.userAgent);
        },
        BlackBerry: function () {
            return /BlackBerry/i.test(navigator.userAgent);
        },
        iOS: function () {
            return /iPhone|iPad|iPod/i.test(navigator.userAgent);
        },
        Windows: function () {
            return /IEMobile/i.test(navigator.userAgent);
        },
        any: function () {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Windows());
        }
    };

    $scope.loadUser = function () {
        if (Session.isAuthorized()) {
            AuthService.getUser().then(function (user) {
                $scope.currentUser = user;
            }).finally(function () {
                $scope.hideLoader();
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
    '$scope',
    '$cookieStore',
    '$timeout',
    'AUTH_EVENTS',
    'Session',
    'AuthService',
    MainCtrl]);


