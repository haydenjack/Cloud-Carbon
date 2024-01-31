"Functions required for efficient operation of dashboard."

import json

def read_metadata(filepath: str) -> dict:
    "Reads in the calculation metadata."
    with open(filepath, "r") as f:
        metadata = json.load(f)
    return metadata


def convert_provider_name(provider: str) -> str:
    "Converts provider name to provider id."
    if provider == "Amazon Web Services":
        return "aws"
    if provider == "Microsoft Azure":
        return "azure"
    if provider == "Google Cloud Platform":
        return "gcp"
    raise ValueError("Invalid provider named.")


if __name__ == "__main__":

    print(generate_region_list("gcp","metadata.json"))
