"Exploring the functionality of the Climatiq API Cloud Computing endpoint."

import requests


def calculate_vm_instance(provider: str, region: str, instance: str, duration: int) -> int:
    "This function calculates the emissions of one virtual machine."
    if provider not in ("aws","azure","gcp"):
        raise ValueError("Provider must be one of aws, azure, gcp.")
    
    full_url = f"https://beta4.api.climatiq.io/compute/{provider}/instance"

    body={"region": region,
          "instance": instance,
          "duration": duration}
    
    response = requests.post(url=full_url,
                             headers={"Authorization": "Bearer HWJG9AHYSB4NV3MJ8GKCD78WT84H"},
                             json=body)
    return response.json()


def generate_vm_request_body(region: str, instance: str, duration: int) -> dict:
    "Creates a valid body object for batch requests."
    if not isinstance(duration, int):
        raise ValueError("Duration must be an integer.")
    if not isinstance(region, str) or not isinstance(instance, str):
        raise ValueError("Region and instance must be a string.")

    return {"region": region,
          "instance": instance,
          "duration": duration}


if __name__ == "__main__":

    calculation = calculate_vm_instance("aws", "eu_west_2", "a1.medium", 24)

    print(calculation["total_co2e"])

    batch_url = "https://beta4.api.climatiq.io/compute/aws/instance/batch"

    body_array = [{"region": "eu_west_2",
                   "instance": "a1.medium",
                   "duration": 24},
                   {"region": "eu_west_1",
                   "instance": "c5.24xlarge",
                   "duration": 15}]
    
    response = requests.post(url=batch_url,
                             headers={"Authorization": "Bearer HWJG9AHYSB4NV3MJ8GKCD78WT84H"},
                             json=body_array)
    
    print(response.json())
