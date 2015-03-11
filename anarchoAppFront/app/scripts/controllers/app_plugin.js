var AppPluginCtrl = function ($scope, AppsService) {
    AppsService.getPluginConfig($scope.appKey).then(function (data) {
        $scope.appKey = data.data.app_key;
        $scope.host = data.data.host;
        $scope.apiToken = data.data.api_token;
    });
};
app.controller("AppPluginCtrl", ['$scope', 'AppsService', AppPluginCtrl]);
