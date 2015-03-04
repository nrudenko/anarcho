var buildDetailsCtrl = function ($rootScope, $scope, $routeParams, AppsService, ngToast, PermissionService, app_config) {
    PermissionService.extend($scope);
    console.log(app_config);
    $scope.certLink = app_config.API_URL + 'cert';
    $scope.app = {};
    $scope.buildId = $routeParams.build_id;
    $scope.appKey = $routeParams.app_key;
    $scope.editNotesDisabled = true;

    $scope.getBuild = function () {
        AppsService.getBuild($scope.appKey, $scope.buildId).then(function (res) {
            $scope.build = res.data;
            $rootScope.hideLoader();
        });
    };

    $scope.editNotes = function () {
        $scope.editNotesDisabled = false;
    };

    $scope.linkCopied = function () {
        ngToast.create('Link ' + $scope.build.build_url + ' copied');
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
    AppsService.get($scope.appKey).then(function (res) {
            $scope.app = res.data;
            if ($scope.app.app_type === 'ios') {
                $scope.iosApp = true;
            } else {
                $scope.iosApp = false;
            }
            $scope.getBuild();
        }
    );

};

app.controller("BuildDetailsCtrl", ['$rootScope', '$scope', '$routeParams', 'AppsService', 'ngToast',
    'PermissionService', 'app_config', buildDetailsCtrl]);