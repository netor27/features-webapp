function User(data){
    this.name = ko.observable(data.name);
    this.password = ko.observable(data.password);
}

function FeaturesViewModel() {
    toastr.options.closeButton = true;
    toastr.options.closeDuration = 150;
    
    // Data
    var self = this;
    self.client = AjaxHelper();
    self.user = ko.observable();
    self.currentPage = ko.observable();
    self.userLoginForm = new User({name:"", password:""});

    // Behaviors
    self.logout = function(){
        self.user(null);     
        location.hash = "Home";
    };

    self.showContainer = function(page){
        return page == self.currentPage();
    }

    
    self.login = function(){
        name = self.userLoginForm.name();
        password = self.userLoginForm.password();
        self.client.get("api/users/"+name, {}, name, password, 
        function(data, status)
        {
            self.user({name:name, password:password});
            self.userLoginForm = new User({name:"", password:""});        
            toastr.success(name, 'Welcome!');
        },
        function(error){
            toastr.error("Incorrect username or password");     
        });        
    };
    

    // Client-side routes    
    Sammy(function () {

        this.get('#:page', function(){
            currentPage = this.params.page;
            self.currentPage(currentPage);
            if(currentPage != "home" && !self.user()){
                this.app.runRoute('get', '#home')
            }

            switch (currentPage) {
                case "features":
                    
                    break;
            
                default:
                    break;
            }
        });

        this.get('', function () { 
            this.app.runRoute('get', '#home')
        });
    }).run();
};

ko.applyBindings(new FeaturesViewModel());