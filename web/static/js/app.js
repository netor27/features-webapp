toastr.options.closeButton = true;
toastr.options.closeDuration = 150;

var ahClient = null;

function NavViewModel() {
    var self = this;
    self.loginFormUsername = ko.observable();
    self.loginFormPassword = ko.observable();
    self.username = ko.observable();
    self.currentPage = ko.observable();

    self.login = function () {
        username = self.loginFormUsername();
        password = self.loginFormPassword();
        ahClient = new AjaxHelper(username, password);
        ahClient.get("api/users/" + username, {},
            function (data, status) {
                self.username(username);
                toastr.success(username, 'Welcome!');
                location.hash = "Home";
            },
            function (error) {
                toastr.error("Incorrect username or password");
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
    self.features = ko.observable();
    self.page = ko.observable(0);
    self.pageSize = 5;

    self.show = ko.computed(function () {
        return navViewModel.currentPage() == "features";
    });
    self.pages = ko.computed(function () {
        if (self.features() == null)
            return 0 ; 
        count = self.features().count;
        n = Math.ceil(count / self.pageSize);
        result = []
        for (var i = 0; i < n; i++)
            result.push(i+1);
        return result;
    });



    self.init = function () {
        getFeatures();
    }

    function getFeatures() {
        ahClient.get("api/features/", { "page":self.page(), "size":self.pageSize},
            function (data, status) {
                self.features(data);
            },
            function (error) {
                toastr.error("Error");
            });
    };
};

function AreasViewModel() {
    var self = this;
    self.show = ko.computed(function () {
        return navViewModel.currentPage() == "areas";
    });

    self.areas = ko.observable();

    self.init = function () {
        getAreas();
    }

    function getAreas() {
        ahClient.get("api/areas/", {},
            function (data, status) {
                self.areas(data);
            },
            function (error) {
                toastr.error("Error");
            });


    };
};

function ClientsViewModel() {
    var self = this;
    self.show = ko.computed(function () {
        return navViewModel.currentPage() == "clients";
    });

    self.clients = ko.observable();

    self.init = function () {
        getClients();
    }

    function getClients() {
        ahClient.get("api/clients/", {},
            function (data, status) {
                self.clients(data);
            },
            function (error) {
                toastr.error("Error");
            });
    };
};

// declare view models
var navViewModel = new NavViewModel();
var homeViewModel = new HomeViewModel();
var featuresViewModel = new FeaturesViewModel();
var areasViewModel = new AreasViewModel();
var clientsViewModel = new ClientsViewModel();

// apply bindings
ko.applyBindings(navViewModel, $('#NavViewModel')[0]);
ko.applyBindings(homeViewModel, $('#HomeViewModel')[0]);
ko.applyBindings(featuresViewModel, $('#FeaturesViewModel')[0]);
ko.applyBindings(areasViewModel, $('#AreasViewModel')[0]);
ko.applyBindings(clientsViewModel, $('#ClientsViewModel')[0]);

