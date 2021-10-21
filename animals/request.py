import sqlite3 #ch 9
import json  #ch 9
from models import Animal, Location, Customer 


ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Gypsy",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Admitted"
    }
]


def get_all_animals():  #refactored from just being 'return ANIMALS'
    # Open a connection to the database
    with sqlite3.connect("./kennel.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.customer_id,
            a.status,
            a.location_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # These are creating instances of the classes we made blueprints of in the model, then giving the instance the variable 'animal'
            animal = Animal(row['id'], row['name'], row['breed'], row['customer_id'],
                            row['status'], row['location_id'])

            # Create a Location instance from the current row
            location = Location(row['id'], row['location_name'], row['location_address'])

            customer = Customer(row['id'], row['customer_name'], row['customer_address'])

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__

            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)


    # Use `json` package to properly serialize list as JSON
    return json.dumps(animals)

# Function with a single parameter
def get_single_animal(id):  #refactored in ch 9
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.customer_id,
            a.status,
            a.location_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address
        FROM animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['customer_id'], data['status'],
                            data['location_id'])

        location = Location(data['id'], data['location_name'], data['location_address'])

        customer = Customer(data['id'], data['customer_name'], data['customer_address'])
       
        animal.location = location.__dict__
        animal.customer = customer.__dict__
        
        return json.dumps(animal.__dict__)

    
#from ch15
def create_animal(new_animal):
    with sqlite3.connect("./kennel.db") as conn: #set up path to sql database
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'], new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))

        #lastrowid property on cursor returns PK of last thing added to database
        id = db_cursor.lastrowid 

        new_animal['id'] = id

    return json.dumps(new_animal)





    # # Get the id value of the last animal in the list
    # max_id = ANIMALS[-1]["id"]

    # # Add 1 to whatever that number is
    # new_id = max_id + 1

    # # Add an `id` property to the animal dictionary
    # animal["id"] = new_id

    # # Add the animal dictionary to the list
    # ANIMALS.append(animal)

    # # Return the dictionary with `id` property added
    # return animal

#from ch5
# def delete_animal(id):
#     animal_index = -1

#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             animal_index = index

#     if animal_index >= 0:
#         ANIMALS.pop(animal_index)

#from ch11
def delete_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

# the update_animal function before ch 13 ~~~~~~~~
# def update_animal(id, new_animal):
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Update the value.
#             ANIMALS[index] = new_animal
#             break
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_animals_by_location(location_id):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """, ( location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset: #CH 10 FIRST HAD LOCALID THEN CUSTID BELOW AND RETURNED CUSTID 1 ANIMALS.  SWITCHED THEM AND IT WORKED.
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)

def get_animals_by_status(status):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset: #CH 10 FIRST HAD LOCALID THEN CUSTID BELOW AND RETURNED CUSTID 1 ANIMALS.  SWITCHED THEM AND IT WORKED.
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~