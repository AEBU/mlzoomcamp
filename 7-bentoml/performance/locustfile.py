from random import sample
import numpy as np
from locust import task
from locust import between 
from locust import HttpUser

sample = {
  "seniority": 12,
  "home": "owner",
  "time": 1,
  "age": 0,
  "marital": "string",
  "records": "string",
  "job": "string",
  "expenses": 0,
  "income": 0,
  "assets": 0,
  "debt": 0,
  "amount": 0,
  "price": 0.1
}


class CreditRiskTestUser(HttpUser):
    """
    Usage: 
        Start locust load testing cliente with 
        locust -H http://localhost:3000
        Open browser at http://0.0.0.0:8089 
    """
    @task
    def classify(self):
        self.client.post("/classify_vector_validate",json=sample)
    
    # RPS Request per second, para cada solicitud que hace el cliente
    wait_time = between(0.01,2) # Random time entre 0.01-2s