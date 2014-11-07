app.config(['$routeProvider',
    function ($routeProvider) {

        $routeProvider.
            when('/apps', {
                templateUrl: 'views/apps_list.html'
            }).
            when('/apps/:app_key', {
                templateUrl: 'views/app_detail.html'
            }).
            when('/settings/:app_key/', {
                templateUrl: 'views/app_settings.html'
            }).
            otherwise({
                redirectTo: '/apps'
            });
    }]);