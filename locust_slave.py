import base64

import requests
from locust import HttpUser, task, between, events
from random import choice

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    username = "user2"
    password = "password"

    @events.test_start.add_listener
    def setup(environment, **kwargs):

        user_json = {
            "email": "user@user.com",
            "firstName": "user2",
            "lastName": "user",
            "password": "password",
            "username": "user2"
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

        print("***********************************************************************************", flush=True)
        customers = requests.get(environment.host + '/customers').json()['_embedded']['customer']

        for customer in customers:
            if customer['username'] == user_json['username']:
                requests.delete(environment.host + '/customers/' + customer['id'])
                print("User deleted")

        resp = requests.post(environment.host + '/register', json=user_json)

        customer_id = resp.json()['id']
        print(customer_id)

        session = requests.session()
        session.get(environment.host + "/login", auth=(user_json['username'], user_json['password']))

        resp = session.post(environment.host + '/addresses', json=address_json)
        session.post(environment.host + '/cards', json=card_json)
        print("User with id " + customer_id + " created", flush=True)

    def on_start(self):
        self.client.get("/login", auth=(self.username, self.password))

    @task(4)
    def frontend(self):
        self.client.get("/")

    @task(6)
    def catalogue(self):
        self.client.get("/category.html")

    @task(1)
    def carts(self):
        self.client.get("/cart")

    #@task(1)
    #def user(self):
    #    #string = ('%s:%s' % ('user', 'password')).replace('\n', '')
    #    #base64string = base64.encodebytes(bytes(string, "UTF-8"))
    #    #self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})
    #    #self.client.get("/login", {"username":"useername", "password":"password"})
    #    self.client.get("/login", auth=(self.username, self.password))
#
    @task(1)
    def orders(self):
        self.client.get("/login", auth=(self.username, self.password))
        resp = self.client.get("/orders")
        #print(resp.status_code, flush=True)

    @task(1)
    def basket(self):
        self.client.get("/basket.html")

    @task(1)
    def add_order(self):
        #self.client.get("/login", auth=(self.username, self.password))

        catalogue = self.client.get("/catalogue").json()
        #category_item = choice(catalogue)
        category_item = catalogue[1]
        item_id = category_item["id"]
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.post("/cart", json={"id": item_id, "quantity": 1})

        resp = self.client.post("/orders")
        #if resp.json().get('id') is not None:
            #print(resp.json().get('id'), flush=True)
            #I can request the detail information as a webpage
            #resp = self.client.get("/detail.html?id={}".format(resp.json().get('id')))
            #print(resp.status_code)
            #print(resp.json())
        self.client.delete("/cart")
