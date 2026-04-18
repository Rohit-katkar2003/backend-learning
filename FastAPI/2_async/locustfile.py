from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    host = "http://127.0.0.1:8000"   # 👈 FIX HERE
    wait_time = between(0.001, 0.01)

    @task
    def test_root(self):
        self.client.get("/")

    @task
    def test_multi(self):
        self.client.get("/multi")