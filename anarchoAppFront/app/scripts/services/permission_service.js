var PermissionService = function () {
    var _this = {};

    _this.hasPermission = function (app, key) {
        if (app.permission) {
            return app.permission.indexOf(key) != -1;
        } else {
            return false;
        }
    };

    _this.canWrite = function (app) {
        return _this.hasPermission(app, "w");
    };


    _this.extend = function ($scope) {
        $scope.canWrite = function () {
            return _this.canWrite($scope.app);
        }
    };

    return _this;
};
app.factory('PermissionService', [PermissionService]);

