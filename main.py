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


def generate_vm_request_body(region: str, instance: str, duration: int, duration_unit: str="h", vcpu_utilization: float=0.5) -> dict:
    "Creates a valid body object for batch requests."
    if not isinstance(duration, int):
        raise ValueError("Duration must be an integer.")
    if not isinstance(region, str) or not isinstance(instance, str):
        raise ValueError("Region and instance must be a string.")
    if duration_unit not in ("ms","s","m","h","day","year"):
        raise ValueError("Duration unit must be one of ms, s, m, h, day or year.")
    if not isinstance(vcpu_utilization, float):
        raise ValueError("vCPU utilization must be a float.")
    if vcpu_utilization > 1 or vcpu_utilization < 0:
        raise ValueError("vCPU utilization must be between 0 and 1.")

    return {"region": region,
          "instance": instance,
          "duration": duration,
          "duration_unit": duration_unit,
          "average_vcpu_utilization:": vcpu_utilization}


if __name__ == "__main__":

    # calculation = calculate_vm_instance("aws", "eu_west_2", "a1.medium", 24)

    # print(calculation["total_co2e"])

    # batch_url = "https://beta4.api.climatiq.io/compute/aws/instance/batch"

    # body_array = [{"region": "eu_west_2",
    #                "instance": "a1.medium",
    #                "duration": 24},
    #                {"region": "eu_west_1",
    #                "instance": "c5.24xlarge",
    #                "duration": 15}]
    
    # response = requests.post(url=batch_url,
    #                          headers={"Authorization": "Bearer HWJG9AHYSB4NV3MJ8GKCD78WT84H"},
    #                          json=body_array)
    
    # print(response.json())

    print(generate_vm_request_body("eu_west_2", "a1.medium", 24))