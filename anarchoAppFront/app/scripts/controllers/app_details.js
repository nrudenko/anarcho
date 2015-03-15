'use strict';
var appDetailsCtrl = function ($scope, $modal, $timeout, $routeParams, AppsService, $location, PermissionService, ngToast) {

    PermissionService.extend($scope);

    $scope.app = {};
    $scope.builds = [];

    $scope.appKey = $routeParams.app_key;

    $scope.progress = -1;

    $scope.buildsList = function (appKey) {
        AppsService.getBuilds(appKey).then(function (res) {
            $scope.builds = res.data.list;
        }).finally(function () {
            $rootScope.showLoader();
        });
    };

    $scope.getApp = function (appKey) {
        AppsService.get(appKey).then(function (res) {
            $scope.app = res.data;
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
        ).then(function (data) {
                $scope.builds.push(data);
                $scope.getApp($scope.appKey);
            }).catch(function (xhr) {
                ngToast.create({
                    content: xhr.data.error,
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
        AppsService.removeBuilds($scope.appKey, $scope.ids).then(function (res) {
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
    $scope.getApp($scope.appKey);
    $scope.buildsList($scope.appKey);
};

app.controller("AppDetailsCtrl", ['$scope', '$modal', '$timeout', '$routeParams', 'AppsService',
    '$location', 'PermissionService', 'ngToast', appDetailsCtrl]);


