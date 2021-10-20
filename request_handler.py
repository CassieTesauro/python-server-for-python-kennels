from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal
from animals import get_animals_by_location, get_animals_by_status
from customers import get_all_customers, get_single_customer, create_customer
from customers import delete_customer, update_customer, get_customers_by_email
from employees import get_all_employees, get_single_employee, create_employee
from employees import delete_employee, update_employee, get_employees_by_location
from locations import get_all_locations, get_single_location, create_location
from locations import delete_location, update_location



class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):  #UPDATED IN CH 10
        """Parses path to access id
        """
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)


    # Here's a class function
    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):   #UPDATED IN CH 10
        """Handles GET requests to the server
        """
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
            
            if key == "location_id" and resource == "employees":
                response = get_employees_by_location(value)

            if key == "location_id" and resource == "animals":
                response = get_animals_by_location(value)

            if key == "status" and resource == "animals":
                response = get_animals_by_status(value)  

        self.wfile.write(response.encode())



    def do_POST(self):
        """Handles POST requests to the server
        """
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None

        if resource == "animals":
            new_animal = create_animal(post_body)

        # Encode the new animal and send in response
            self.wfile.write(f"{new_animal}".encode())  #Note- make sure everything under if is indented or you'll get a 'none' running when you try to do postman

        new_location = None
        if resource == "locations":
            new_location = create_location(post_body)
            self.wfile.write(f"{new_location}".encode())
 
        new_employee = None
        if resource == "employees":
            new_employee = create_employee(post_body)
            self.wfile.write(f"{new_employee}".encode())  

        new_customer = None
        if resource == "customers":
            new_customer = create_customer(post_body)
            self.wfile.write(f"{new_customer}".encode())  


    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            delete_animal(id)

            self.wfile.write("".encode())

        if resource == "locations":
            delete_location(id)

            self.wfile.write("".encode())

        if resource == "employees":
            delete_employee(id)

            self.wfile.write("".encode())

        if resource == "customers":
            delete_customer(id)

            self.wfile.write("".encode())

    def do_PUT(self):
        """Handles PUT requests to the server
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)

        if resource == "customers":
            success = update_customer(id, post_body)

        if resource == "employees":
            success = update_employee(id, post_body)

        if resource == "locations":
            success = update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
