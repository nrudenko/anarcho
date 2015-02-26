var buildDetailsCtrl = function ($rootScope, $scope, $routeParams, AppsService, UrlService, ngToast, PermissionService) {
    PermissionService.extend($scope);

    $scope.app = {}
    $scope.buildId = $routeParams.build_id;
    $scope.appKey = $routeParams.app_key;

    $scope.editNotesDisabled = true;

    $scope.getBuild = function () {
        AppsService.getBuild($scope.appKey, $scope.buildId).then(function (res) {
            $scope.build = res.data;
            if ($scope.build) {
                $scope.buildUrl = UrlService.getBuildUrl($scope.appKey, $scope.build);
            }
            $rootScope.hideLoader();
        });
    };

    $scope.getApp = function () {
        AppsService.get($scope.appKey).then(function (res) {
            $scope.app = res.data;
        });
    };


    $scope.editNotes = function () {
        $scope.editNotesDisabled = false;
    };

    $scope.linkCopied = function () {
        ngToast.create('Link ' + $scope.buildUrl + ' copied');
    };

    $scope.saveNotes = function () {
        AppsService.postNotes($scope.appKey, $scope.buildId, $scope.build.release_notes).then(function () {
            $scope.editNotesDisabled = true;
        }, function () {
            ngToast.create({
                content: 'Can\'t update release notes',
                className: 'danger'
            });
            console.log();
        });
    };

    $rootScope.showLoader();
    $scope.getBuild();
    $scope.getApp();
};

app.controller("BuildDetailsCtrl", ['$rootScope', '$scope', '$routeParams', 'AppsService', 'UrlService', 'ngToast',
    'PermissionService', buildDetailsCtrl]);