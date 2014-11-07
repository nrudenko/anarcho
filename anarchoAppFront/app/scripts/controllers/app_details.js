'use strict';
var appDetailsCtrl = function ($rootScope, $scope, $modal, $timeout, $routeParams, AppsService) {
    $scope.app = {};
    $scope.builds = [];

    $scope.appKey = $routeParams.app_key;

    $scope.canWrite = function () {
        return $scope.hasPermission("w");
    };

    $scope.hasPermission = function (key) {
        if ($scope.app.permission) {
            return $scope.app.permission.indexOf(key) != -1;
        } else {
            return false;
        }
    };

    $scope.progress = -1;

    $scope.init = function () {
        $rootScope.showLoader();
        $scope.getApp($scope.appKey);
    };

    $scope.buildsList = function (appKey) {
        AppsService.getBuilds(appKey).then(function (res) {
            console.log(res.data);
            $scope.builds = res.data.list;
            console.log($scope.builds);
        })
    };

    $scope.addBuild = function () {
        AppsService.addBuild($scope.appKey).then(function (res) {
            $scope.builds.push(res.data);
        });
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

    $scope.init();

    //
    var ShowBuildInfoCtrl = function ($scope, $modalInstance, UrlService, build) {
        $scope.build = build;
        $scope.getBuildUrl = function () {
            return UrlService.getBuildUrl(build);
        }
    };

    ShowBuildInfoCtrl.$inject = ['$scope', '$modalInstance', 'UrlService', 'build'];

    $scope.showBuildInfo = function (build) {
        $modal.open({
                templateUrl: 'views/build_details_modal.html',
                size: "sm",
                controller: ShowBuildInfoCtrl,
                resolve: {
                    build: function () {
                        return build;
                    }
                }
            }
        );
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
};

app.controller("AppDetailsCtrl", ['$rootScope', '$scope', '$modal', '$timeout', '$routeParams', 'AppsService', appDetailsCtrl]);


