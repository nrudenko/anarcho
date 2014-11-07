'use strict';
var appCtrl = function ($rootScope, $scope, $modal, AppsService) {
    $scope.apps = [];

    var showNewAppCtrl = function ($scope, $modalInstance) {
        $scope.modalAddApp = function (app) {
            $modalInstance.close(app);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss();
        };
    };
    showNewAppCtrl.$inject = ['$scope', '$modalInstance'];
    $scope.showNewApp = function () {
        $modal.open({
                templateUrl: 'views/new_app_modal.html',
                size: "sm",
                controller: showNewAppCtrl
            }
        ).
            result.then(function (app) {
                $scope.addApp(app);
            });
    };
    $rootScope.showLoader();
    AppsService.list().success(function (data) {
        $scope.apps = data.list;
        $rootScope.hideLoader();
    });

    $scope.addApp = function (app) {
        AppsService.add(app).then(function (response) {
            $scope.apps.push(response.data);
        });
    };

};

app.controller("AppsCtrl", ['$rootScope', '$scope', '$modal', 'AppsService', appCtrl]);
