"use strict";angular.module("anarchoApp",["ngCookies","ngRoute","ui.bootstrap","angularFileUpload","ja.qr"]);var app=angular.module("anarchoApp");app.constant("AUTH_EVENTS",{loginSuccess:"auth-login-success",loginFailed:"auth-login-failed",logoutSuccess:"auth-logout-success",sessionTimeout:"auth-session-timeout",notAuthenticated:"auth-not-authenticated",notAuthorized:"auth-not-authorized"}),app.config(["$routeProvider",function(a){a.when("/apps",{templateUrl:"views/apps_list.html"}).when("/apps/:app_key",{templateUrl:"views/app_detail.html"}).when("/settings/:app_key/",{templateUrl:"views/app_settings.html"}).otherwise({redirectTo:"/apps"})}]),app.constant("configuration",{API_URL:"api/"});var AuthCtrl=function(a,b,c,d,e){a.login=function(f){d.login(f).then(function(a){e.create(a.authToken),b.$broadcast(c.loginSuccess)}).catch(function(d){a.error=d.error,b.$broadcast(c.loginFailed)})},a.register=function(f){d.register(f).then(function(a){e.create(a.authToken),b.$broadcast(c.loginSuccess)}).catch(function(d){console.log(d.error),a.error=d.error,b.$broadcast(c.loginFailed)})},a.logout=function(){e.destroy(),b.$broadcast(c.logoutSuccess)}};app.controller("AuthCtrl",["$scope","$rootScope","AUTH_EVENTS","AuthService","Session",AuthCtrl]),app.controller("TracksCtrl",["$scope","TracksService",function(a,b){a.tracks=[],b.fetch().success(function(b){a.tracks=b.data})}]);var appCtrl=function(a,b,c,d){b.apps=[];var e=function(a,b){a.modalAddApp=function(a){b.close(a)},a.cancel=function(){b.dismiss()}};e.$inject=["$scope","$modalInstance"],b.showNewApp=function(){c.open({templateUrl:"views/new_app_modal.html",size:"sm",controller:e}).result.then(function(a){b.addApp(a)})},a.showLoader(),d.list().success(function(c){b.apps=c.list,a.hideLoader()}),b.addApp=function(a){d.add(a).then(function(a){b.apps.push(a.data)})}};app.controller("AppsCtrl",["$rootScope","$scope","$modal","AppsService",appCtrl]);var appDetailsCtrl=function(a,b,c,d,e,f){b.app={},b.builds=[],b.appKey=e.app_key,b.canWrite=function(){return b.hasPermission("w")},b.hasPermission=function(a){return b.app.permission?-1!=b.app.permission.indexOf(a):!1},b.progress=-1,b.init=function(){a.showLoader(),b.getApp(b.appKey)},b.buildsList=function(a){f.getBuilds(a).then(function(a){console.log(a.data),b.builds=a.data.list,console.log(b.builds)})},b.addBuild=function(){f.addBuild(b.appKey).then(function(a){b.builds.push(a.data)})},b.getApp=function(c){f.get(c).then(function(c){b.app=c.data,b.buildsList(b.appKey),a.hideLoader()})},b.onFileSelect=function(a){var c=a[0];b.upload=f.uploadBuild(b.appKey,c,function(a){b.progress=a},function(a){b.builds.push(a),d(function(){b.progress=-1},1e3)})},b.init();var g=function(a,b,c,d){a.build=d,a.getBuildUrl=function(){return c.getBuildUrl(d)}};g.$inject=["$scope","$modalInstance","UrlService","build"],b.showBuildInfo=function(a){c.open({templateUrl:"views/build_details_modal.html",size:"sm",controller:g,resolve:{build:function(){return a}}})},b.ids=[],b.remove=function(){f.removeBuilds(b.appKey,b.ids).then(function(){b.ids=[],b.init()})},b.toggleBuild=function(a){var c=b.ids.indexOf(a);c>-1?b.ids.splice(c,1):b.ids.push(a)}};app.controller("AppDetailsCtrl",["$rootScope","$scope","$modal","$timeout","$routeParams","AppsService",appDetailsCtrl]);var AppSettingsCtrl=function(a,b,c){a.app={},a.appKey=b.app_key,a.canWrite=function(){return a.hasPermission("w")},a.hasPermission=function(b){return a.app.permission?-1!=a.app.permission.indexOf(b):!1},a.getInclude=function(){var b="";switch(a.action){case"team":b="views/settings_team.html";break;case"remove":b="views/settings_remove_app.html"}return b},a.getApp=function(b){c.get(b).then(function(b){a.app=b.data,a.canWrite()&&(a.action="team")})},a.init=function(){a.getApp(a.appKey)},a.init()};app.controller("AppSettingsCtrl",["$scope","$routeParams","AppsService",AppSettingsCtrl]);var AppRemoveCtrl=function(){console.log("AppRemoveCtrl"+(new Date).getTime())};app.controller("AppRemoveCtrl",["$scope","AppsService",AppRemoveCtrl]);var AppTeamCtrl=function(a,b){a.permissions=[],a.usersList=function(c){b.list(c).success(function(b){a.permissions=b.list})},a.addUser=function(c){c.app_key=a.app.app_key,b.add(c).success(function(b){a.permissions.push(b)})},a.updateUser=function(c){c.app_key=a.app.app_key,b.update(c).success(function(){})},a.revokeUser=function(c){c.app_key=a.app.app_key,b.revoke(c).success(function(b){for(var c=0;c<a.permissions.length;c++)if(a.permissions[c].email===b.email){a.permissions.splice(c,1);break}})},a.usersList(a.app.app_key),a.all_permissions=[{id:"w",name:"Write"},{id:"r",name:"Read"}]};app.controller("AppTeamCtrl",["$scope","TeamService",AppTeamCtrl]);var MainCtrl=function(a,b,c,d,e,f,g){a.showLoader=function(){b.progressTimeout=d(function(){b.showProgress=!0},1e3)},a.hideLoader=function(){b.showProgress=!1,d.cancel(b.progressTimeout)},a.isLoading=function(){return b.showProgress},b.loadUser=function(){f.isAuthorized()&&g.getUser().then(function(c){b.currentUser=c,a.hideLoader()}).catch(function(){a.hideLoader()})},b.$on(e.loginSuccess,function(){b.loadUser()}),b.$on(e.logoutSuccess,function(){b.currentUser=null}),b.loadUser()};app.controller("MainCtrl",["$rootScope","$scope","$cookieStore","$timeout","AUTH_EVENTS","Session","AuthService",MainCtrl]);var api=function(a,b,c,d){var e={};return e.getBaseConfig=function(a){var b={url:c.API_URL+a,headers:{}},e=d.authToken;return null!=e&&(b.headers["x-auth-token"]=e),b},e.delete=function(b,c){var d=e.getBaseConfig(b);return d.headers["Content-Type"]="application/json;charset=utf-8",d.method="DELETE",d.data=c,a(d)},e.post=function(b,c){var d=e.getBaseConfig(b);return d.headers["Content-Type"]="application/json;charset=utf-8",d.method="POST",d.data=c,a(d)},e.patch=function(b,c){var d=e.getBaseConfig(b);return d.method="PATCH",d.data=c,a(d)},e.get=function(b){var c=e.getBaseConfig(b);return c.method="GET",a(c)},e.uploadBuild=function(a,c,d,f){var g=e.getBaseConfig(a);return b.upload({url:g.url,method:"POST",headers:g.headers,file:c}).progress(function(a){d(parseInt(100*a.loaded/a.total))}).success(function(a){f(a)})},e};app.factory("Api",["$http","$upload","configuration","Session",api]);var AuthService=function(a){var b={};return b.login=function(b){return a.post("login",b).then(function(a){return a.data},function(a){throw a.data})},b.register=function(b){return a.post("register",b).then(function(a){return a.data},function(a){throw a.data})},b.parseUser=function(a){var b={};return b.name=a.data.name,b.id=a.data.id,b},b.getUser=function(){return a.get("user").then(function(a){return b.parseUser(a)},function(a){throw a})},b};app.factory("AuthService",["Api",AuthService]);var SessionService=function(a){return this.authToken=a.get("auth_token"),this.isAuthorized=function(){return null==this.authToken?!1:!0},this.create=function(b){this.authToken=b,a.put("auth_token",this.authToken)},this.destroy=function(){a.remove("auth_token"),this.authToken=null},this};app.service("Session",["$cookieStore",SessionService]);var AppsService=function(a){var b={};return b.list=function(){return a.get("apps")},b.add=function(b){return a.post("apps",b)},b.get=function(b){return a.get("apps/"+b)},b.getBuilds=function(b){return a.get("apps/"+b+"/builds")},b.uploadBuild=function(b,c,d,e){a.uploadBuild("apps/"+b,c,d,e)},b.removeBuilds=function(b,c){return a.delete("apps/"+b+"/builds",{ids:c})},b};app.factory("AppsService",["Api",AppsService]);var TrackService=function(a,b,c){return{fetch:function(){var d={headers:{"x-auth-token":c.authToken}};return a.get(b.API_URL+"track/list",d)}}};app.factory("TracksService",["$http","configuration","Session",TrackService]);var TeamService=function(a){var b={};return b.add=function(b){return a.post("permission",b)},b.update=function(b){return a.patch("permission",b)},b.revoke=function(b){return a.delete("permission",b)},b.list=function(b){return a.get("permission/"+b)},b};app.factory("TeamService",["Api",TeamService]);var UrlService=function(a){var b={};return b.getBuildUrl=function(b){return null!=b.id?a.API_URL+"apps/"+b.app_key+"/"+b.id:void 0},b};app.factory("UrlService",["configuration",UrlService]);var IconSrc=function(){var a={};return a.link=function(a,b,c){a.$watch(function(){return c.iconSrc?b.attr("src",c.iconSrc):b.attr("src","images/./logo.6db6798c.png"),c.iconSrc},function(a){a||b.attr("src","images/./logo.6db6798c.png")}),b.bind("error",function(){b.attr("src","images/./logo.6db6798c.png")})},a};app.directive("iconSrc",IconSrc);