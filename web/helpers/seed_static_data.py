from datetime import date

users = { "DemoUser": "Pa$$word55!", "DemoUser2": "Password1!" }
areas = ['Policies', 'Billing', 'Claims', 'Reports']
clients = ['Client A', 'Client B', 'Client C','Client D', 'Client E', 'Client F', 'Client G' ]
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
    },
    {   
        "title": "New Feature 1", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 1,
        "target_date": date(2018, 8, 15),
        "area": "Claims",
        "client": "Client D"
    },
    {   
        "title": "New Feature 2", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 2,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client F"
    },
    {   
        "title": "New Feature 3", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 3,
        "target_date": date(2018, 8, 15),
        "area": "Claims",
        "client": "Client G"
    },
    {   
        "title": "New Feature 4", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 4,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client D"
    },
    {   
        "title": "New Feature 5", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 5,
        "target_date": date(2018, 8, 15),
        "area": "Billing",
        "client": "Client F"
    },
    {   
        "title": "New Feature 6", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 6,
        "target_date": date(2018, 8, 15),
        "area": "Claims",
        "client": "Client G"
    },
    {   
        "title": "New Feature 7", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 7,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client E"
    },
    {   
        "title": "New Feature 8", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 8,
        "target_date": date(2018, 8, 15),
        "area": "Billing",
        "client": "Client F"
    },
    {   
        "title": "New Feature 9", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 9,
        "target_date": date(2018, 8, 15),
        "area": "Claims",
        "client": "Client G"
    },
    {   
        "title": "New Feature 10", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 10,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client D"
    },
    {   
        "title": "New Feature 11", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 11,
        "target_date": date(2018, 8, 15),
        "area": "Billing",
        "client": "Client F"
    },
    {   
        "title": "New Feature 12", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 12,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client G"
    },
    {   
        "title": "New Feature 13", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 13,
        "target_date": date(2018, 8, 15),
        "area": "Claims",
        "client": "Client D"
    },
    {   
        "title": "New Feature 14", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 14,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client F"
    },
    {   
        "title": "New Feature 15", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 15,
        "target_date": date(2018, 8, 15),
        "area": "Billing",
        "client": "Client G"
    },
    {   
        "title": "New Feature 16", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 16,
        "target_date": date(2018, 8, 15),
        "area": "Claims",
        "client": "Client D"
    },
    {   
        "title": "New Feature 17", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 17,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client F"
    },
    {   
        "title": "New Feature 18", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 18,
        "target_date": date(2018, 8, 15),
        "area": "Billing",
        "client": "Client D"
    },
    {   
        "title": "New Feature 19", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 19,
        "target_date": date(2018, 8, 15),
        "area": "Billing",
        "client": "Client E"
    },
    {   
        "title": "New Feature 20", 
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", 
        "client_priority": 20,
        "target_date": date(2018, 8, 15),
        "area": "Reports",
        "client": "Client E"
    }
]