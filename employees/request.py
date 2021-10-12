EMPLOYEES = [
    {
        "id": 1,
        "name": "Jessica Younker",
        "address": "123 Street St.",
        "locationId": 2
    },
    {
        "id": 2,
        "name": "Zoe LeBlanc",
        "email": "123 Street Rd.",
        "locationId": 1
    },
    {
        "name": "Hannah Hall",
        "email": "123 Avenue St.",
        "id": 3,
        "locationId": 2
    },
    {
        "name": "Jenna Solis",
        "email": "123 Street Ave.",
        "id": 4,
        "locationId": 1
    },
    {
        "id": 5,
        "name": "Ryan Tanay",
        "email": "123 Road St.",
        "locationId": 2
    }
]

def get_all_employees():
    return EMPLOYEES

# Function with a single parameter
def get_single_employee(id):
    # Variable to hold the found animal, if it exists
    requested_employee = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for employee in EMPLOYEES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if employee["id"] == id:
            requested_employee = employee

    return requested_employee
    
