'use strict';
var AppBaseCtrl = function ($scope, $routeParams, AppsService) {

    $scope.app = {};
    $scope.appKey = $routeParams.app_key;

    $scope.hasPermission = function (app, key) {
        if (app.permission) {
            return app.permission.indexOf(key) != -1;
        } else {
            return false;
        }
    };

    $scope.canWrite = function () {
        return $scope.hasPermission($scope.app, "w");
    };

    $scope.loadApp = function () {
        AppsService.get($scope.appKey).then(function (res) {
            $scope.app = res.data;
        });
    };
};

app.controller("AppBaseCtrl", ['$scope', '$routeParams', 'AppsService', AppBaseCtrl]);