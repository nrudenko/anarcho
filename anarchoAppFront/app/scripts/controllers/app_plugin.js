var AppPluginCtrl = function ($scope, AppsService) {
    AppsService.getPluginConfig($scope.appKey)
        .success(function (data) {
            $scope.appKey = data.app_key;
            $scope.host = data.host;
            $scope.apiToken = data.api_token;
        });
};
app.controller("AppPluginCtrl", ['$scope', 'AppsService', AppPluginCtrl]);
