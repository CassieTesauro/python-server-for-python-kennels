CUSTOMERS = [
    {
        "id": 1,
        "name": "Cassie Tesauro",
        "email": "cassie@tesauro.com",
        "password": "1234"
    },
    {
        "id": 2,
        "name": "Ben Gregory",
        "email": "ben@gregory.com",
        "password": "1234"
    },
    {
        "name": "Myriam Chevalier",
        "email": "myriam@chavalier.com",
        "password": "1234",
        "id": 3
    },
    {
        "name": "Matthew Singler",
        "email": "matthew@singler.com",
        "password": "1234",
        "id": 4
    }
]

def get_all_customers():
    return CUSTOMERS

# Function with a single parameter
def get_single_customer(id):
    # Variable to hold the found animal, if it exists
    requested_customer = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for customer in CUSTOMERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer
    
