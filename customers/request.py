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
    

def create_customer(customer):
    max_id = CUSTOMERS[-1]["id"]

    new_id = max_id + 1

    customer["id"] = new_id

    CUSTOMERS.append(customer)

    return customer


#from ch5
def delete_customer(id):
    customer_index = -1

    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index = index

    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)