$(function () {

    toastr.options.closeButton = true;
    toastr.options.closeDuration = 150;

    var ahClient = null;

    function NavViewModel() {
        var self = this;
        self.loginFormUsername = ko.observable();
        self.loginFormPassword = ko.observable();
        self.username = ko.observable();
        self.currentPage = ko.observable();
        self.originalHash = null;

        self.login = function () {
            username = self.loginFormUsername();
            password = self.loginFormPassword();
            ahClient = new AjaxHelper(username, password);
            ahClient.get("api/users/" + username, {},
                function (data, status) {
                    self.username(username);
                    toastr.success(username, 'Welcome!');
                    location.hash = self.originalHash;
                },
                function (error) {
                    toastr.error("Incorrect username or password");
                    console.error(error);
                });
        }

        self.logout = function () {
            self.username(null);
            ahClient = null;
            location.hash = "Home";
        };


        // Client-side routes    
        Sammy(function () {

            this.get('#:page', function () {
                currentPage = this.params.page.toLowerCase()
                self.currentPage(currentPage);
                // validate that we can only view the home page if we're not logged in
                if (currentPage != "home" && !self.username()) {
                    self.originalHash = location.hash;
                    location.hash = "home";
                } else {
                    switch (currentPage) {
                        case "home":
                            break;
                        case "features":
                            featuresViewModel.init();
                            break;
                        case "areas":
                            areasViewModel.init();
                            break;
                        case "clients":
                            clientsViewModel.init();
                            break;

                        default:
                            toastr.warning("Sorry, this page doesn't exists!");
                            location.hash = "home";
                            break;
                    }
                }
            });

            this.get('#:page/add', function () {
                if (!self.username()) {
                    self.originalHash = location.hash;
                    location.hash = "home";
                    return;
                }

                currentPage = this.params.page.toLowerCase();
                self.currentPage(currentPage);
                switch (currentPage) {
                    case "feature":
                        featureDetailViewModel.init(null);
                        break;
                    default:
                        toastr.warning("Sorry, this page doesn't exists!");
                        location.hash = "home";
                        break;
                }

            });

            this.get('#:page/:id', function () {
                if (!self.username()) {
                    self.originalHash = location.hash;
                    location.hash = "home";
                    return;
                }

                currentPage = this.params.page.toLowerCase();
                id = this.params.id.toLowerCase();
                self.currentPage(currentPage);
                switch (currentPage) {
                    case "feature":
                        featureDetailViewModel.init(id);
                        break;
                    default:
                        toastr.warning("Sorry, this page doesn't exists!");
                        location.hash = "home";
                        break;
                }

            });

            this.get('', function () {
                this.app.runRoute('get', '#home')
            });
        }).run();

    };

    function HomeViewModel() {
        var self = this;
        self.show = ko.computed(function () {
            return navViewModel.currentPage() == "home";
        });
    };

    function FeaturesViewModel() {
        var self = this;
        self.pageSize = 5;
        self.features = ko.observable();
        self.page = ko.observable(1);
        self.pages = ko.observableArray([]);
        self.pendingDelete = null;

        self.show = ko.computed(function () {
            return navViewModel.currentPage() == "features";
        });

        self.init = function () {
            getFeatures();
        }

        self.changePage = function (item) {
            if (self.page() != item) {
                self.page(item);
                getFeatures();
            }
        };

        self.isActivePage = function (index) {
            return index == self.page();
        };

        self.showModalDelete = function (item) {
            console.log(location.hash);
            self.pendingDelete = item;
            $('#featureDeleteModal').modal('show');
        };

        self.deleteFeature = function () {
            ahClient.delete(self.pendingDelete.url, {},
                function (data, status) {
                    toastr.success('Feature deleted');
                    $('#featureDeleteModal').modal('hide');
                    getFeatures();
                },
                function (error) {
                    toastr.error("An error occurred when deleting the feature.");
                    console.error(error);
                    $('#featureDeleteModal').modal('hide');
                });
        };

        function getFeatures() {
            ahClient.get("api/features/", { "page": self.page(), "size": self.pageSize },
                function (data, status) {
                    self.features(data);
                    self.pages.removeAll();
                    n = Math.ceil(data.count / self.pageSize);
                    for (var i = 1; i <= n; i++) {
                        self.pages.push(i);
                    }
                    if (self.page() > n) {
                        self.changePage(n);
                    }
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the features.");
                    console.error(error);
                });
        };
    };

    function AreasViewModel() {
        var self = this;
        self.pageSize = 5;
        self.areas = ko.observable();
        self.page = ko.observable(1);
        self.pages = ko.observableArray([]);
        self.pendingDelete = null;

        self.show = ko.computed(function () {
            return navViewModel.currentPage() == "areas";
        });

        self.init = function () {
            getAreas();
        }

        self.changePage = function (item) {
            if (self.page() != item) {
                self.page(item);
                getAreas();
            }
        };

        self.isActivePage = function (index) {
            return index == self.page();
        };

        self.showModalDelete = function (item) {
            self.pendingDelete = item;
            $('#areaDeleteModal').modal('show');
        };

        self.deleteArea = function () {
            ahClient.delete(self.pendingDelete.url, {},
                function (data, status) {
                    toastr.success('Area deleted');
                    $('#areaDeleteModal').modal('hide');
                    getAreas();
                },
                function (error) {
                    toastr.error("An error occurred when deleting the area.");
                    console.error(error);
                    $('#areaDeleteModal').modal('hide');
                });
        };

        function getAreas() {
            ahClient.get("api/areas/", { "page": self.page(), "size": self.pageSize },
                function (data, status) {
                    self.areas(data);
                    self.pages.removeAll();
                    n = Math.ceil(data.count / self.pageSize);
                    for (var i = 1; i <= n; i++) {
                        self.pages.push(i);
                    }
                    if (self.page() > n) {
                        self.changePage(n);
                    }
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the areas.");
                    console.error(error);
                });
        };
    };

    function ClientsViewModel() {
        var self = this;
        self.pageSize = 5;
        self.clients = ko.observable();
        self.page = ko.observable(1);
        self.pages = ko.observableArray([]);
        self.pendingDelete = null;

        self.show = ko.computed(function () {
            return navViewModel.currentPage() == "clients";
        });

        self.init = function () {
            getClients();
        }

        self.changePage = function (item) {
            if (self.page() != item) {
                self.page(item);
                getClients();
            }
        };

        self.isActivePage = function (index) {
            return index == self.page();
        };

        self.showModalDelete = function (item) {
            self.pendingDelete = item;
            $('#clientDeleteModal').modal('show');
        };

        self.deleteClient = function () {
            ahClient.delete(self.pendingDelete.url, {},
                function (data, status) {
                    toastr.success('Client deleted');
                    $('#clientDeleteModal').modal('hide');
                    getClients();
                },
                function (error) {
                    toastr.error("An error occurred when deleting the client.");
                    console.error(error);
                    $('#clientDeleteModal').modal('hide');
                });
        };

        function getClients() {
            ahClient.get("api/clients/", { "page": self.page(), "size": self.pageSize },
                function (data, status) {
                    self.clients(data);
                    self.pages.removeAll();
                    n = Math.ceil(data.count / self.pageSize);
                    for (var i = 1; i <= n; i++) {
                        self.pages.push(i);
                    }
                    if (self.page() > n) {
                        self.changePage(n);
                    }
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                });
        };
    };

    function FeatureDetailViewModel() {
        var self = this;
        self.id = null;
        self.isUpdate = null;
        self.buttonText = ko.observable();
        self.title = ko.observable();
        self.description = ko.observable();
        self.client = ko.observable();
        self.area = ko.observable();
        self.targetDate = ko.observable();
        self.clientPriority = ko.observable();
        self.clients = ko.observableArray();
        self.areas = ko.observableArray();

        self.show = ko.computed(function () {
            return navViewModel.currentPage() == "feature";
        });

        self.init = function (id) {
            $('.datepicker').datepicker({ format: 'yyyy-mm-dd', todayHighlight: true });
            getClients();

            if (id != null) {
                self.buttonText("Update Feature Request");
                self.id = id;
                self.isUpdate = true;
            } else {
                self.buttonText("Add Feature Request");
                self.isUpdate = false;
            }
        }

        self.submitForm = function () {
            if (self.isUpdate) {
                updateFeature();
            } else {
                addFeature();
            }
        };

        function getClients(callback) {
            ahClient.get("api/clients/", { "page": 1, "size": 1 },
                function (data, status) {
                    n = data.count;
                    ahClient.get("api/clients/", { "page": 1, "size": n },
                        function (data, status) {
                            self.clients(data.results);
                            getAreas();
                        },
                        function (error) {
                            toastr.error("An error occurred when retrieving the clients.");
                            console.error(error);
                        });
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                });
        };

        function getAreas() {
            ahClient.get("api/areas/", { "page": 1, "size": 1 },
                function (data, status) {
                    n = data.count;
                    ahClient.get("api/areas/", { "page": 1, "size": n },
                        function (data, status) {
                            self.areas(data.results);
                            getFeature();
                        },
                        function (error) {
                            toastr.error("An error occurred when retrieving the areas.");
                            console.error(error);
                        });
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the areas.");
                    console.error(error);
                });
        };

        function getFeature() {
            if (self.id == null) {
                return;
            }

            console.log("calling " + "api/features/" + self.id);
            ahClient.get("api/features/" + self.id, {},
                function (data, status) {
                    console.log(data);
                    self.title(data.title);
                    self.description(data.description);
                    self.client(data.client.name);
                    self.area(data.area.name);
                    self.targetDate(data.target_date);
                    self.clientPriority(data.client_priority);
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                });
        };

        function updateFeature() {
            if (self.id == null) {
                return;
            }

            console.log("calling update" + "api/features/" + self.id);
            console.log(self.description())
            ahClient.patch("api/features/" + self.id,
                JSON.stringify({
                    title: self.title(),
                    client: self.client(),
                    description: self.description(),
                    client_priority: self.clientPriority(),
                    target_date: self.targetDate(),
                    area: self.area()
                }),
                function (data, status) {
                    console.log(data);
                    toastr.success("Feature Request updated!");
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                });
        };


    };


    // declare view models
    var navViewModel = new NavViewModel();
    var homeViewModel = new HomeViewModel();
    var featuresViewModel = new FeaturesViewModel();
    var areasViewModel = new AreasViewModel();
    var clientsViewModel = new ClientsViewModel();
    var featureDetailViewModel = new FeatureDetailViewModel();


    // apply bindings
    ko.applyBindings(navViewModel, $('#NavViewModel')[0]);
    ko.applyBindings(homeViewModel, $('#HomeViewModel')[0]);
    ko.applyBindings(featuresViewModel, $('#FeaturesViewModel')[0]);
    ko.applyBindings(areasViewModel, $('#AreasViewModel')[0]);
    ko.applyBindings(clientsViewModel, $('#ClientsViewModel')[0]);
    ko.applyBindings(featureDetailViewModel, $('#FeatureDetailViewModel')[0]);

});


