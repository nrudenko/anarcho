var AppPluginCtrl = function ($scope, AppsService) {
    AppsService.getPluginConfig($scope.appKey).then(function (data) {
        console.log(data);
        $scope.uploadUrl = data.data.uploadUrl;
        $scope.apiToken = data.data.apiToken;
    });
};
app.controller("AppPluginCtrl", ['$scope', 'AppsService', AppPluginCtrl]);
