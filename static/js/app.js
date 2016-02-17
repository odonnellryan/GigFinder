(function () {
    'use strict';

    var module = angular.module('gigFinder', []);

    module.service('gigService', function ($http) {
        this.updateGigs = function () {
            return $http({
                method: 'GET',
                url: '/gigs/'
            });
        }
    });

    module.service('gigSearch', function ($http) {
        this.search = function (searchTerm) {
            return $http({
                method: 'GET',
                url: '/search/' + searchTerm
            });
        }
    });

    module.controller('gigController',
        function ($scope, gigService, gigSearch) {
            $scope.search = function () {
                gigSearch.search($scope.searchText).then(function (response) {
                    $scope.gigs = response.data;
                });
            };
            $scope.gigs = "Gigs not updated";
            gigService.updateGigs().then(function (response) {
                $scope.gigs = response.data;
            });
        });

}());