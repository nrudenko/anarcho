var TrackService = function ($http, configuration, Session) {
    return {
        fetch: function () {
            var config = {
                headers: {'x-auth-token': Session.authToken}
            };

            return $http.get(configuration.API_URL + 'track/list', config);
        }
    }
};
app.factory('TracksService', ['$http', 'configuration', 'Session', TrackService]);
