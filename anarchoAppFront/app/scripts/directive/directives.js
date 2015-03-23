var IconSrc = function () {

    var errSrc = {};

    errSrc.link =
        function (scope, element, attrs) {
            scope.$watch(function () {
                if (!attrs['iconSrc']) {
                    element.attr('src', 'images/logo.png');
                } else {
                    element.attr('src', attrs['iconSrc']);
                }
                return attrs['iconSrc'];
            }, function (value) {
                if (!value) {
                    element.attr('src', 'images/logo.png');
                }
            });

            element.bind('error', function () {
                element.attr('src', 'images/logo.png');
            });
        };

    return errSrc;
};

var AppTypeIcon = function () {

    var appLogoSrc = {};

    appLogoSrc.link =
        function (scope, element, attrs) {
            scope.$watch(function () {
                var type = attrs['appTypeIcon'];
                element.css('display', 'initial');
                if (type === 'andr') {
                    element.attr('src', 'images/icon_droid.png');
                } else if (type === 'ios') {
                    element.attr('src', 'images/icon_apple.png');
                } else {
                    element.css('display', 'none');
                }
            });
        };

    return appLogoSrc;
};


var OrderBtn = function () {
    var orderBtn = {};
    orderBtn.restrict = 'E';
    orderBtn.scope = false;

    orderBtn.link = function ($scope, element, attrs) {
        var update = function () {
            var symbol = "&nbsp;";
            if ($scope.order.field === attrs.field) {
                symbol = $scope.order.reverse ? "&#9660;" : "&#9650;";
            }
            element.html("<span>" + attrs.text + symbol + "</span>");
        };

        element.bind("click", function () {
            var reverse = !$scope.order.reverse;
            if (attrs.field != $scope.order.field) {
                reverse = true;
            }
            $scope.$apply(function () {
                $scope.order = {field: attrs.field,
                    reverse: reverse};
            });
        });

        element.hover(function () {
            element.css('cursor', 'hand');
            element.css('cursor', 'pointer');
        });

        $scope.$watch(function () {
            return $scope.order;
        }, function () {
            update();
        });

        if (attrs.reverse != undefined && attrs.reverse != null) {
            $scope.order = {field: attrs.field,
                reverse: attrs.reverse === 'true'};
            update();
        }

    };
    return orderBtn;
};

function FocusOn($timeout) {
    var checkDirectivePrerequisites = function (attrs) {
        if (!attrs.focusOn && attrs.focusOn != "") {
            throw "FocusOnCondition missing attribute to evaluate";
        }
    };

    return {
        restrict: "A",
        link: function (scope, element, attrs, ctrls) {
            checkDirectivePrerequisites(attrs);

            scope.$watch(attrs.focusOn, function (currentValue, lastValue) {
                if (currentValue == true) {
                    $timeout(function () {
                        element.focus();
                    });
                }
            });
        }
    };
}

app.directive('iconSrc', IconSrc);
app.directive('appTypeIcon', AppTypeIcon);
app.directive('orderBtn', OrderBtn);
app.directive('focusOn', ['$timeout', FocusOn]);
