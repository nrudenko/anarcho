var AppRemoveCtrl = function ($scope, AppsService, $location, ngToast) {

    $scope.removeApp = function () {
        AppsService.removeApp($scope.appKey)
            .success(function (data) {
                $location.path("#/apps")
            }).error(function (data) {
                var errorCode = data.error;
                var errorMsg = "You can't remove <b>" + $scope.app.name + "</b>.  <br> ";
                if (errorCode === 'not_enough_permission') {
                    errorMsg = errorMsg + "Not enough permission!";
                }
                if (errorCode === 'app_not_found') {
                    errorMsg = errorMsg + "Application not found!";
                }
                ngToast.create({
                    content: errorMsg,
                    className: 'danger'
                });
            });
    };
};

app.controller("AppRemoveCtrl", ['$scope', 'AppsService', '$location', 'ngToast', AppRemoveCtrl]);
