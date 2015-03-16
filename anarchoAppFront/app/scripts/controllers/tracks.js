'use strict';
app.controller("TracksCtrl", ['$scope', 'TracksService', function ($scope, TracksService) {
    $scope.tracks = [];
//    $scope.getTracks = function () {
//        TracksService.fetch().then(function (resp) {
//
//            $scope.tracks = resp.data;
//        });
//    };
    TracksService.fetch()
        .success(function (data) {
            $scope.tracks = data.data;
        });
}]);
