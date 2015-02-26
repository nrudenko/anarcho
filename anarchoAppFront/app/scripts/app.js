'use strict';

/**
 * @ngdoc overview
 * @name anarchoApp
 * @description
 * # anarchoApp
 *
 * Main module of the application.
 */


angular
    .module('anarchoApp', [
        'ngCookies',
        'ngRoute',
        'ui.bootstrap',
        'angularFileUpload',
        'ja.qr',
        'ngClipboard',
        'monospaced.elastic',
        'ngToast'
    ]);
var app = angular.module('anarchoApp');

app.config(['ngClipProvider', function (ngClipProvider) {
    ngClipProvider.setPath("bower_components/zeroclipboard/dist/ZeroClipboard.swf");
    ngClipProvider.setConfig({
        forceHandCursor: false
    });

}]);

app.filter('addEllipsis', function () {
    return function (input, scope) {
        var maxCol = scope;
        if (isNaN(parseFloat(maxCol)) && !isFinite(maxCol)) {
            throw "addEllipsis wrong attribute to evaluate. Usage: {{ data | addEllipsis : 50}} ";
        }
        if (input) {
            if (input.length > maxCol) {
                return input.substring(0, maxCol).trim() + '...';
            }
            else {
                return input;
            }
        }
    }
});

app.constant('AUTH_EVENTS', {
    loginSuccess: 'auth-login-success',
    loginFailed: 'auth-login-failed',
    logoutSuccess: 'auth-logout-success',
    sessionTimeout: 'auth-session-timeout',
    notAuthenticated: 'auth-not-authenticated',
    notAuthorized: 'auth-not-authorized'
});