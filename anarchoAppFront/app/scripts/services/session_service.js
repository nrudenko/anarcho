var SessionService = function ($cookieStore) {
    this.authToken = $cookieStore.get('auth_token');

    this.isAuthorized = function () {
        if (this.authToken == null) {
            return false;
        }
        return true;
    };

    this.create = function (authToken) {
        this.authToken = authToken;
        $cookieStore.put('auth_token', this.authToken);
    };

    this.destroy = function () {
        $cookieStore.remove('auth_token');
        this.authToken = null;
    };

    return this;
};
app.service('Session', ['$cookieStore', SessionService]);