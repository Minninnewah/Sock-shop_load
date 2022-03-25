import base64

from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    user_json = {
        "email": "user@user.com",
        "firstName": "user",
        "lastName": "user",
        "password": "password",
        "username": ""
    }

    card_json = {
        "longNum": "1111222233334444",
        "expires": "01/25",
        "ccv": "756"
    }

    address_json = {
        "street": "Baumallee",
        "number": "5",
        "country": "Schweiz",
        "city": "Hogsmeade",
        "postcode": "0000"
    }

    user_counter = 0

    def on_start(self):
        self.user_counter = self.environment.runner.user_count
        self.user_json['username'] = "user" + str(self.user_counter)

        print("***********************************************************************************", flush=True)
        customers = self.client.get('/customers').json()['_embedded']['customer']

        for customer in customers:
            if customer['username'] == self.user_json['username']:
                self.client.delete('/customers/' + customer['id'])
                print("User deleted")

        resp = self.client.post('/register', json=self.user_json)

        customer_id = resp.json()['id']
        self.client.get("/login", auth=(self.user_json['username'], self.user_json['password']))

        self.client.post('/addresses', json=self.address_json)
        self.client.post('/cards', json=self.card_json)
        print("User " + self.user_json['username'] + " with id " + customer_id + " created", flush=True)

    @task(4)
    def frontend(self):
        self.client.get("/")

    @task(1)
    def login(self):
        self.client.get("/login", auth=("user" + str(self.user_counter), self.user_json['password']))

    @task(6)
    def catalogue(self):
        self.client.get("/category.html")

    @task(1)
    def carts(self):
        self.client.get("/cart")

    @task(1)
    def orders(self):
        self.client.get("/orders")

    @task(1)
    def basket(self):
        self.client.get("/basket.html")

    @task(1)
    def add_order(self):
        catalogue = self.client.get("/catalogue").json()
        category_item = catalogue[1]
        item_id = category_item["id"]
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.post("/cart", json={"id": item_id, "quantity": 1})

        self.client.post("/orders")
        self.client.delete("/cart")
