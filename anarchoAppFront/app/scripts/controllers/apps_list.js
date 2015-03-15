'use strict';
var AppsListCtrl = function ($scope, $modal, AppsService) {
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
    $scope.showLoader();
    AppsService.list().success(function (data) {
        $scope.apps = data.list;
        $scope.hideLoader();
    });

    $scope.addApp = function (app) {
        AppsService.add(app).then(function (response) {
            $scope.apps.push(response.data);
        });
    };

};

app.controller("AppsCtrl", ['$scope', '$modal', 'AppsService', AppsListCtrl]);
