(function () {
    'use strict';

    var module = angular.module('gigFinder', []);

    module.service('gigService', function ($http) {
        this.update_gigs = function () {
            return $http({
                method: 'GET',
                url: '/gigs/'
            });
        }
    });

    module.controller('gigController', ['$scope', 'gigService', function ($scope, gigService) {
        $scope.gigs = "Gigs not updated";
        gigService.update_gigs().then(function (response) {
            $scope.gigs = response.data;
        });
    }]);

}());