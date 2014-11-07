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
        'ja.qr'
    ]);
var app = angular.module('anarchoApp');

app.constant('AUTH_EVENTS', {
    loginSuccess: 'auth-login-success',
    loginFailed: 'auth-login-failed',
    logoutSuccess: 'auth-logout-success',
    sessionTimeout: 'auth-session-timeout',
    notAuthenticated: 'auth-not-authenticated',
    notAuthorized: 'auth-not-authorized'
});