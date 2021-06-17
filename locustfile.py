import os
from locust import HttpUser, task, constant
import logstream
import time


class LogStreamUser(HttpUser):
    wait_time = constant(1)

    def make_logstream(self):
        source = os.environ["LOG_SOURCE"]
        stream = logstream.LogStream(source)
        return stream

    @task
    def send_requests(self):
        stream = self.make_logstream()
        for route in stream:
            self.client.get(route)
            time.sleep(0.1)
