'use strict';
var AppTeamCtrl = function ($scope, TeamService) {
    $scope.all_permissions = [
        {id: "w", name: "Write"},
        {id: "r", name: "Read"}
    ];

    $scope.permissions = [];
    $scope.usersList = function (app_key) {
        TeamService.list(app_key)
            .success(function (data) {
                $scope.permissions = data.list;
            });
    };

    $scope.addUser = function (permission) {
        permission.app_key = $scope.appKey;
        TeamService.add(permission)
            .success(function (data) {
                $scope.permissions.push(data);
                $scope.error = null;
            }).error(function (data) {
                $scope.error = data.error;
            });
    };

    $scope.updateUser = function (user_app) {
        user_app.app_key = $scope.appKey;
        TeamService.update(user_app)
            .success(function (data) {
                //TODO implement
            });
    };

    $scope.revokeUser = function (user_app) {
        user_app.app_key = $scope.appKey;
        TeamService.revoke(user_app)
            .success(function (data) {
                for (var i = 0; i < $scope.permissions.length; i++) {
                    if ($scope.permissions[i].email === data.email) {
                        $scope.permissions.splice(i, 1);
                        break;
                    }
                }
            });
    };

    $scope.usersList($scope.appKey);
};

app.controller("AppTeamCtrl", ['$scope', 'TeamService', AppTeamCtrl]);
