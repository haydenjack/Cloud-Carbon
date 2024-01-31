"Functions required for efficient operation of dashboard."

from os import environ
from dotenv import load_dotenv
import requests
import json
import streamlit as st


load_dotenv()


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
          "average_vcpu_utilization": vcpu_utilization}


def read_metadata(filepath: str) -> dict:
    "Reads in the calculation metadata."
    with open(filepath, "r") as f:
        metadata = json.load(f)
    return metadata


def convert_provider_name(provider: str) -> str:
    "Converts provider name to provider id and vice versa."
    if provider == "Amazon Web Services":
        return "aws"
    if provider == "Microsoft Azure":
        return "azure"
    if provider == "Google Cloud Platform":
        return "gcp"
    if provider == "aws":
        return "Amazon Web Services"
    if provider == "azure":
        return "Microsoft Azure"
    if provider == "gcp":
        return "Google Cloud Platform"
    raise ValueError("Invalid provider named.")


def reset_batches() -> None:
    "Clears all calculation entries."
    st.session_state["aws_batch"] = []
    st.session_state["azure_batch"] = []
    st.session_state["gcp_batch"] = []


def send_batch_request(provider: str, body_array: list):
    "Makes a batch request for multiple vm instances."
    if provider not in ("aws","azure","gcp"):
            raise ValueError("Provider must be one of aws, azure, gcp.")
        
    batch_url = f"https://beta4.api.climatiq.io/compute/{provider}/instance/batch"
    
    response = requests.post(url=batch_url,
                             headers={"Authorization": f"Bearer {environ['API_KEY']}"},
                             json=body_array)
    return response.json()


def format_batch_response(response: dict) -> float:
    "Extracts important information from calculation response."
    overall_co2e = 0
    result_set = response.get("results")
    if result_set:
        for item in result_set:
            overall_co2e += item.get("total_co2e")
    return overall_co2e


def calculate() -> int:
    "Performs full calculation for each cloud service."
    aws_batch = st.session_state["aws_batch"]
    azure_batch = st.session_state["azure_batch"]
    gcp_batch = st.session_state["gcp_batch"]
    complete_co2e = 0
    if aws_batch:
        aws_response = send_batch_request("aws", aws_batch)
        complete_co2e += format_batch_response(aws_response)
    if azure_batch:
        azure_response = send_batch_request("azure", azure_batch)
        complete_co2e += format_batch_response(azure_response)
    if gcp_batch:
        gcp_response = send_batch_request("gcp", gcp_batch)
        complete_co2e += format_batch_response(gcp_response)
    return complete_co2e
