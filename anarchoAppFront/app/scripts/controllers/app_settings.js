var AppSettingsCtrl = function ($rootScope, $scope, $routeParams, AppsService) {
    $scope.app = {};
    $scope.appKey = $routeParams.app_key;

    $scope.canWrite = function () {
        return $scope.hasPermission("w");
    };

    $scope.hasPermission = function (key) {
        if ($scope.app.permission) {
            return $scope.app.permission.indexOf(key) != -1;
        } else {
            return false;
        }
    };

    $scope.getInclude = function () {
        var includePage = "";
        switch ($scope.action) {
            case "team":
                includePage = "views/settings_team.html";
                break;
            case "remove":
                includePage = "views/settings_remove_app.html";
                break;
            case "plugin":
                if ($scope.app.app_type==='andr') {
                    includePage = "views/settings_plugin_config_android.html";
                } else {
                    includePage = "views/settings_plugin_config_bash.html";
                }

                break;
        }

        return includePage;
    };

    $scope.getApp = function (appKey) {
        AppsService.get(appKey).then(function (res) {
            $scope.app = res.data;
            $scope.action = "team";
        });
    };

    $scope.init = function () {
        $scope.getApp($scope.appKey);
    };

    $scope.init();
};
app.controller("AppSettingsCtrl", ['$rootScope', '$scope', '$routeParams', 'AppsService', AppSettingsCtrl]);
