var AppPluginCtrl = function ($scope, UrlService) {
    $scope.uploadUrl = UrlService.getUploadUrl($scope.appKey);
};
app.controller("AppPluginCtrl", ['$scope', 'UrlService', AppPluginCtrl]);
