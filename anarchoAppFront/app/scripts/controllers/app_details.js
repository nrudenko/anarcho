'use strict';
var appDetailsCtrl = function ($rootScope, $scope, $modal, $timeout, $routeParams, AppsService, $location, PermissionService) {

    PermissionService.extend($scope);

    $scope.app = {};
    $scope.builds = [];

    $scope.appKey = $routeParams.app_key;

    $scope.progress = -1;

    $scope.buildsList = function (appKey) {
        AppsService.getBuilds(appKey).then(function (res) {
            $scope.builds = res.data.list;
        })
    };

    $scope.getApp = function (appKey) {
        AppsService.get(appKey).then(function (res) {
            $scope.app = res.data;
            $scope.buildsList($scope.appKey);
            $rootScope.hideLoader();
        });
    };

    $scope.onFileSelect = function ($files) {
        var file = $files[0];

        $scope.upload = AppsService.uploadBuild(
            $scope.appKey,
            file,
            function (progress) {
                $scope.progress = progress;
            },
            function (data) {
                $scope.builds.push(data);
                $timeout(function () {
                    $scope.progress = -1;
                }, 1000);
            });

        //.error(...)
        //.then(success, error, progress);
        // access or attach event listeners to the underlying XMLHttpRequest.
        //.xhr(function(xhr){xhr.upload.addEventListener(...)})
    };

    $scope.showBuildInfo = function (build) {
        $location.path('/apps/' + $scope.app.app_key + '/' + build.id);
    };

    $scope.ids = [];
    $scope.remove = function () {
        AppsService.removeBuilds($scope.appKey, $scope.ids).then(function (res) {
            $scope.ids = [];
            $scope.init()
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


    $rootScope.showLoader();
    $scope.getApp($scope.appKey);
};

app.controller("AppDetailsCtrl", ['$rootScope', '$scope', '$modal', '$timeout', '$routeParams', 'AppsService',
    '$location', 'PermissionService', appDetailsCtrl]);


