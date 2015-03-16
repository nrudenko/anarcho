'use strict';
var AppSettingsCtrl = function ($scope, $routeParams, AppsService, $controller) {
    $controller('AppBaseCtrl', {$scope: $scope});

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
                if ($scope.app.app_type === 'andr') {
                    includePage = "views/settings_plugin_config_android.html";
                } else {
                    includePage = "views/settings_plugin_config_bash.html";
                }

                break;
        }

        return includePage;
    };

    $scope.loadApp();
    $scope.action = "team";
};
app.controller("AppSettingsCtrl", ['$scope', '$routeParams', 'AppsService', '$controller', AppSettingsCtrl]);
