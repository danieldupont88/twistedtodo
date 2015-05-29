/**
 * Created by dn3 on 28/05/2015.
 */

angular
    .module('twistedToDo', ['ngResource']);

angular.module('twistedToDo')
    .controller('todoCtrl', todoCtrl);

        todoCtrl.$inject = ['$scope', '$http', '$rootScope'];

        function todoCtrl($scope, $http, $rootScope) {
            $scope.makeLogin = function () {
                console.log('makelogin');
                if (!$scope.user || !$scope.password) {

                    return false;

                }

                $http.post('http://dn3lenovo\:8090/login/', {username: $scope.user, password: $scope.password}).
                    success(function (data, status, headers, config) {
                        console.log('logado');
                        $scope.loggedUser = data.username;
                        $("#loginContainer").hide("slow");
                        $scope.todos = $scope.queryTodos();

                    }).
                    error(function (data, status, headers, config) {
                        console.log('erro');
                        $scope.loginError = "Houve um erro ao tentar logar!";

                    });
            };

            $scope.dismissError = function () {
                console.log('dismiss error');
                delete $scope.loginError;
            };

            $scope.checkTodo = function (todo) {
                console.log(todo);
                todo.status = !todo.status;
                var req = {
                    method: 'PUT',
                    url: 'http://dn3lenovo\:8090/todos/' + todo.id ,
                    headers: {'user': $scope.loggedUser},
                    data: todo
                };

                $http(req).success(
                    function (data, status, headers, config) {
                        console.log('sucesso');
                    })
                    .error(
                    function (data, status, headers, config) {
                        console.log('erro');
                    });

            };

            $scope.updateTodo = function (todo) {
                console.log(todo);
                var req = {
                    method: 'PUT',
                    url: 'http://dn3lenovo\:8090/todos/' + todo.id ,
                    headers: {'user': $scope.loggedUser},
                    data: todo
                };

                $http(req).success(
                    function (data, status, headers, config) {
                        console.log('sucesso');
                    })
                    .error(
                    function (data, status, headers, config) {
                        console.log('erro');
                    });

            };

            $scope.queryTodos = function () {
                var req = {
                    method: 'GET',
                    url: 'http://dn3lenovo\:8090/todos',
                    headers: {'user': $scope.loggedUser},
                    data: {}
                };

                $http(req).success(
                    function (data, status, headers, config) {
                        $scope.todos = data;
                    })
                    .error(
                    function (data, status, headers, config) {
                        console.log('erro');
                    });
            };

            $scope.createTodo = function() {
                var req = {
                    method: 'POST',
                    url: 'http://dn3lenovo\:8090/todos',
                    headers: {'user': $scope.loggedUser},
                    data: {task : $scope.newTodo, "status": 0, user: $scope.loggedUser  }
                };

                $http(req).success(
                    function (data, status, headers, config) {
                        $scope.newTodo = '';
                        $scope.todos.push(data);
                    })
                    .error(
                    function (data, status, headers, config) {
                        console.log('erro');
                    });
            };

            $scope.deleteTodo = function(todo) {
                var req = {
                    method: 'DELETE',
                    url: 'http://dn3lenovo\:8090/todos/' + todo.id,
                    headers: {'user': $scope.loggedUser},
                    data: { }
                };

                $http(req).success(
                    function (data, status, headers, config) {
                        $("#TodoContainer" + todo.id).hide("slow");
                    })
                    .error(
                    function (data, status, headers, config) {
                        console.log('erro');
                    });
            };



        }
