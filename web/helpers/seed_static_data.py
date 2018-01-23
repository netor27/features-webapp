from datetime import date

users = { "user": "Pa$$word55!", "user2": "Password1!" }
areas = ['Policies', 'Billing', 'Claims', 'Reports']
clients = ['Client A', 'Client B', 'Client C' ]
features = [
    {   
        "title": "Add sorting/filtering options to carriers client list", 
        "description": "Currently, the client list offered in our solution only supports sorting and filtering by client name, add: By Client Category, By Client Size, By Client Country", 
        "client_priority": 10,
        "target_date": date(2018, 9, 15),
        "area": "Reports",
        "client": "Client A"
    },
    {   
        "title": "Add American Express payment method", 
        "description": "Currently, the billing platform only supports Visa and MasterCard. Add the support to pay with American Express", 
        "client_priority": 1,
        "target_date": date(2018, 7, 1),
        "area": "Billing",
        "client": "Client A"
    },
    {   
        "title": "Add a read-only role that can only view certain Account details", 
        "description": "This new read-only role is for the use of the Accountant Jr. so he/she could be able to view the following fields of in the Account Detail screen: Account Name, Account Total Balance, Total Deposits, Total Withdrawals. He should not be able to see the client details associated with the account", 
        "client_priority": 4,
        "target_date": date(2018, 5, 25),
        "area": "Policies",
        "client": "Client B"
    },
    {   
        "title": "Review past claims", 
        "description": "The user wants to be able to review past claims even if they are closed or cancelled", 
        "client_priority": 7,
        "target_date": date(2018, 11, 15),
        "area": "Claims",
        "client": "Client B"
    },
    {   
        "title": "Client relationship report", 
        "description": "Add a report that gives the relationship between clients no matter what carrier/company they have their insurance with", 
        "client_priority": 1,
        "target_date": date(2018, 6, 15),
        "area": "Reports",
        "client": "Client C"
    },
    {   
        "title": "Client Hazard report", 
        "description": "Obtain a report that, based on our data and analysis, sets one of the following categories for the clients: -Really Safe -Safe -Normal -Dangerous -Really Dangerous", 
        "client_priority": 2,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client C"
    }]
