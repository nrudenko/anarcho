var AppTeamCtrl = function ($scope, SettingsService) {
    $scope.permissions = [];
    $scope.usersList = function (app_key) {
        SettingsService.list(app_key).success(function (data) {
            $scope.permissions = data.list;
        });
    };

    $scope.addUser = function (permission) {
        permission.app_key = $scope.app.app_key;
        SettingsService.add(permission).then(function (data) {
            $scope.permissions.push(data.data);
            $scope.error = null;
        }, function (error) {
            $scope.error = error.data.error;
        });
    };

    $scope.updateUser = function (user_app) {
        user_app.app_key = $scope.app.app_key;
        SettingsService.update(user_app).success(function (data) {
        });
    };

    $scope.revokeUser = function (user_app) {
        user_app.app_key = $scope.app.app_key;
        SettingsService.revoke(user_app).success(function (data) {
            for (var i = 0; i < $scope.permissions.length; i++) {
                if ($scope.permissions[i].email === data.email) {
                    $scope.permissions.splice(i, 1);
                    break;
                }
            }
        });
    };

    $scope.usersList($scope.app.app_key);

    $scope.all_permissions = [
        {id: "w", name: "Write"},
        {id: "r", name: "Read"}
    ];
};

app.controller("AppTeamCtrl", ['$scope', 'SettingsService', AppTeamCtrl]);
