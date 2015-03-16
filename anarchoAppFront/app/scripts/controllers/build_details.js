var BuildDetailsCtrl = function ($scope, AppsService, $routeParams, ngToast, $controller, app_config) {
    $controller('AppBaseCtrl', {$scope: $scope});

    $scope.certLink = app_config.API_URL + 'cert';
    $scope.buildId = $routeParams.build_id;
    $scope.editNotesDisabled = true;

    $scope.$watch('app', function () {
        if ($scope.app.app_type === 'ios') {
            $scope.iosApp = true;
        } else {
            $scope.iosApp = false;
        }
    });

    $scope.getBuild = function () {
        AppsService.getBuild($scope.appKey, $scope.buildId).then(function (res) {
            $scope.build = res.data;
        }).finally(function () {
            $rootScope.hideLoader();
        });
    };

    $scope.editNotes = function () {
        $scope.editNotesDisabled = false;
    };

    $scope.saveNotes = function () {
        AppsService.postNotes($scope.appKey, $scope.buildId, $scope.build.release_notes).then(function () {
            $scope.editNotesDisabled = true;
        }, function () {
            ngToast.create({
                content: 'Can\'t update release notes',
                className: 'danger'
            });
        });
    };

    $scope.linkCopied = function () {
        ngToast.create('Link ' + $scope.build.build_url + ' copied');
    };

    $scope.showLoader();
    $scope.loadApp();
    $scope.getBuild();
};

app.controller("BuildDetailsCtrl", ['$scope', 'AppsService', '$routeParams',
    'ngToast', '$controller', 'app_config', BuildDetailsCtrl]);