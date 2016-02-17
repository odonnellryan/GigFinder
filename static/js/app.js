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
        this.performSearch = function ($scope, searchTerm) {
            apiSearch(searchTerm).then(function success(response) {
                $scope.gigs = response.data;
            }, function failure(){
                $scope.gigs = {
                    "error": "Problem with search results"
                }
            });
        };
        var apiSearch = function (searchTerm) {
            return $http({
                method: 'GET',
                url: '/search/' + searchTerm
            });
        }
    });

    module.controller('gigController',
        function ($scope, gigService, gigSearch) {
            $scope.search = function () {
                if ($scope.searchText) {
                    gigSearch.performSearch($scope, $scope.searchText)
                } else {
                    updateGigs();
                }
            };
            $scope.gigs = "Loading gigs...";
            var updateGigs = function() {
                gigService.updateGigs().then(function (response) {
                    $scope.gigs = response.data;
                });
            };
            updateGigs();
        });

}());