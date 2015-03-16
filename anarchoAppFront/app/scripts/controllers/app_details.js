'use strict';
var AppDetailsCtrl = function ($scope, $modal, $timeout, AppsService, $location, $controller, ngToast) {
    $controller('AppBaseCtrl', {$scope: $scope});

    $scope.builds = [];

    $scope.progress = -1;

    $scope.buildsList = function (appKey) {
        AppsService.getBuilds(appKey)
            .success(function (data) {
                $scope.builds = data.list;
            }).finally(function () {
                $rootScope.hideLoader();
            });
    };

    $scope.onFileSelect = function (files) {
        var file = files[0];

        AppsService.uploadBuild(
            $scope.appKey,
            file,
            function (progress) {
                $scope.progress = progress;
            }
        ).success(function (data) {
                $scope.builds.push(data);
                $scope.getApp($scope.appKey);
            }).error(function (data) {
                ngToast.create({
                    content: data.error,
                    className: 'danger'
                });
            }).finally(function () {
                $timeout(function () {
                    $scope.progress = -1;
                }, 1000);
            });
    };

    $scope.showBuildInfo = function (build) {
        $location.path('/apps/' + $scope.app.app_key + '/' + build.id);
    };

    $scope.ids = [];
    $scope.remove = function () {
        AppsService.removeBuilds($scope.appKey, $scope.ids)
            .success(function (data) {
                $scope.ids = [];
                $scope.buildsList($scope.appKey);
            })
    };

    $scope.toggleBuild = function (id) {
        var idx = $scope.ids.indexOf(id);
        // is currently selected
        if (idx > -1) {
            $scope.ids.splice(idx, 1);
        }
        // is newly selected
        else {
            $scope.ids.push(id);
        }
    };

    $scope.showLoader();
    $scope.loadApp();
    $scope.buildsList($scope.appKey);
};

app.controller("AppDetailsCtrl", ['$scope', '$modal', '$timeout', 'AppsService',
    '$location', '$controller', 'ngToast', AppDetailsCtrl]);


