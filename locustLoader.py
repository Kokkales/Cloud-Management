from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        self.client.post("/login", {
            "username": "test_user",
            "password": ""
        })

    @task
    def get_endpoint(self):
        self.client.get("/get")

    @task
    def post_endpoint(self):
        self.client.post("/post", json={"data": "some_data"})

    @task
    def delete_endpoint(self):
        self.client.delete("/delete")

    @task
    def put_endpoint(self):
        self.client.put("/put", json={"data": "some_data"})
