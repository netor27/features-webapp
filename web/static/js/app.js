$(function () {

    toastr.options.closeButton = true;
    toastr.options.closeDuration = 150;

    var ahClient = null;

    // TODO: move this viewmodels to separate files :/

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
                console.log(currentPage);
                switch (currentPage) {
                    case "feature":
                        featureDetailViewModel.init(null);
                        break;
                    case "area":
                        areaDetailViewModel.init(null);
                        break;
                    case "client":
                        clientDetailViewModel.init(null);
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
                    case "area":
                        areaDetailViewModel.init(id);
                        break;
                    case "client":
                        clientDetailViewModel.init(id);
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
        self.pageSize = 10;
        self.viewIsReady = ko.observable(false);
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
            self.pendingDelete = item;
            $('#featureDeleteModal').modal('show');
        };

        self.deleteFeature = function () {
            self.viewIsReady(false);
            $('#featureDeleteModal').modal('hide');
            ahClient.delete(self.pendingDelete.url, {},
                function (data, status) {
                    toastr.success('Feature deleted');
                    getFeatures();
                },
                function (error) {
                    toastr.error("An error occurred when deleting the feature.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function getFeatures() {
            self.viewIsReady(false);
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
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the features.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };
    };

    function AreasViewModel() {
        var self = this;
        self.pageSize = 5;
        self.viewIsReady = ko.observable(false);
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
            self.viewIsReady(false);
            $('#areaDeleteModal').modal('hide');
            ahClient.delete(self.pendingDelete.url, {},
                function (data, status) {
                    toastr.success('Area deleted');
                    getAreas();
                },
                function (error) {
                    toastr.error("An error occurred when deleting the area.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function getAreas() {
            self.viewIsReady(false);
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
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the areas.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };
    };

    function ClientsViewModel() {
        var self = this;
        self.pageSize = 5;
        self.viewIsReady = ko.observable(false);
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
            self.viewIsReady(false);
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
                    self.viewIsReady(true);
                });
        };

        function getClients() {
            self.viewIsReady(false);
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
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };
    };

    function FeatureDetailViewModel() {
        var self = this;
        self.id = null;
        self.isUpdate = null;
        self.viewIsReady = ko.observable(true);
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

            if (id != null) {
                self.buttonText("Update Feature Request");
                self.id = id;
                self.isUpdate = true;
            } else {
                self.buttonText("Add Feature Request");
                self.isUpdate = false;
                self.id = null;
                self.title("");
                self.description("");
                self.client("");
                self.area("");
                self.targetDate("");
                self.clientPriority("");
            }

            $('.datepicker').datepicker({ format: 'yyyy-mm-dd', todayHighlight: true });
            getClients();
        }

        self.submitForm = function () {
            self.viewIsReady(false);
            if (self.isUpdate) {
                updateFeature();
            } else {
                addFeature();
            }
        };

        function getClients(callback) {
            self.viewIsReady(false);
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
                    self.viewIsReady(true);
                });
        };

        function getAreas() {
            self.viewIsReady(false);
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
                    self.viewIsReady(true);
                });
        };

        function getFeature() {
            if (self.id == null) {
                self.viewIsReady(true);
                return;
            }

            self.viewIsReady(false);
            ahClient.get("api/features/" + self.id, {},
                function (data, status) {
                    self.title(data.title);
                    self.description(data.description);
                    self.client(data.client.name);
                    self.area(data.area.name);
                    self.targetDate(data.target_date);
                    self.clientPriority(data.client_priority);
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function updateFeature() {
            if (self.id == null) {
                return;
            }

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
                    toastr.success("Feature Request updated!");
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when updating the feature.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function addFeature() {
            ahClient.post("api/features/",
                JSON.stringify({
                    title: self.title(),
                    client: self.client(),
                    description: self.description(),
                    client_priority: self.clientPriority(),
                    target_date: self.targetDate(),
                    area: self.area()
                }),
                function (data, status) {
                    toastr.success("Feature Request created! With Id: " + data.id);
                    self.init(null);
                },
                function (error) {
                    toastr.error("An error occurred when creating the feature request.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };
    };

    function AreaDetailViewModel() {
        var self = this;
        self.id = null;
        self.isUpdate = null;
        self.viewIsReady = ko.observable(true);
        self.buttonText = ko.observable();
        self.name = ko.observable();

        self.show = ko.computed(function () {
            return navViewModel.currentPage() == "area";
        });

        self.init = function (id) {

            if (id != null) {
                self.buttonText("Update Area Request");
                self.id = id;
                self.isUpdate = true;
            } else {
                self.buttonText("Add Area Request");
                self.isUpdate = false;
                self.id = null;
                self.name("");
                self.viewIsReady(true);
            }

            getArea();
        }

        self.submitForm = function () {
            if (self.isUpdate) {
                updateArea();
            } else {
                addArea();
            }
        };

        function getArea() {
            if (self.id == null) {
                return;
            }

            self.viewIsReady(false);
            ahClient.get("api/areas/" + self.id, {},
                function (data, status) {
                    self.name(data.name);
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function updateArea() {
            if (self.id == null) {
                return;
            }
            self.viewIsReady(false);
            ahClient.patch("api/areas/" + self.id,
                JSON.stringify({
                    name: self.name(),
                }),
                function (data, status) {
                    toastr.success("Area Request updated!");
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when updating the area.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function addArea() {
            self.viewIsReady(false);
            ahClient.post("api/areas/",
                JSON.stringify({
                    name: self.name(),
                }),
                function (data, status) {
                    toastr.success("Area Request created! With Id: " + data.id);
                    self.init(null);
                },
                function (error) {
                    toastr.error("An error occurred when creating the area request.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };
    };

    function ClientDetailViewModel() {
        var self = this;
        self.id = null;
        self.isUpdate = null;
        self.viewIsReady = ko.observable(true);
        self.buttonText = ko.observable();
        self.name = ko.observable();

        self.show = ko.computed(function () {
            return navViewModel.currentPage() == "client";
        });

        self.init = function (id) {

            if (id != null) {
                self.buttonText("Update Client Request");
                self.id = id;
                self.isUpdate = true;
            } else {
                self.buttonText("Add Client Request");
                self.isUpdate = false;
                self.id = null;
                self.name("");
                self.viewIsReady(true);
            }

            getClient();
        }

        self.submitForm = function () {
            if (self.isUpdate) {
                updateClient();
            } else {
                addClient();
            }
        };

        function getClient() {
            if (self.id == null) {
                return;
            }

            self.viewIsReady(false);
            ahClient.get("api/clients/" + self.id, {},
                function (data, status) {
                    self.name(data.name);
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when retrieving the clients.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function updateClient() {
            if (self.id == null) {
                return;
            }
            self.viewIsReady(false);
            ahClient.patch("api/clients/" + self.id,
                JSON.stringify({
                    name: self.name(),
                }),
                function (data, status) {
                    toastr.success("Client Request updated!");
                    self.viewIsReady(true);
                },
                function (error) {
                    toastr.error("An error occurred when updating the client.");
                    console.error(error);
                    self.viewIsReady(true);
                });
        };

        function addClient() {
            self.viewIsReady(false);
            ahClient.post("api/clients/",
                JSON.stringify({
                    name: self.name(),
                }),
                function (data, status) {
                    toastr.success("Client Request created! With Id: " + data.id);
                    self.init(null);
                },
                function (error) {
                    toastr.error("An error occurred when creating the client request.");
                    console.error(error);
                    self.viewIsReady(true);
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
    var areaDetailViewModel = new AreaDetailViewModel();
    var clientDetailViewModel = new ClientDetailViewModel();


    // apply bindings
    ko.applyBindings(navViewModel, $('#NavViewModel')[0]);
    ko.applyBindings(homeViewModel, $('#HomeViewModel')[0]);
    ko.applyBindings(featuresViewModel, $('#FeaturesViewModel')[0]);
    ko.applyBindings(areasViewModel, $('#AreasViewModel')[0]);
    ko.applyBindings(clientsViewModel, $('#ClientsViewModel')[0]);
    ko.applyBindings(featureDetailViewModel, $('#FeatureDetailViewModel')[0]);
    ko.applyBindings(areaDetailViewModel, $('#AreaDetailViewModel')[0]);
    ko.applyBindings(clientDetailViewModel, $('#ClientDetailViewModel')[0]);

    


});


