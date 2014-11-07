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

app.directive('iconSrc', IconSrc);