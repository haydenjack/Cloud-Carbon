# Cloud-Carbon Dashboard
Cloud-Carbon is an intuitive dashboard designed to help users assess the carbon footprint of their cloud resources, promoting sustainable practices in cloud computing.

## Features
- **Carbon Footprint Estimation**: Calculate the carbon footprint of cloud resources using the Climatiq API.
- **Intuitive Interface**: The project furnishes an easy-to-navigate dashboard built with Streamlit.
- **Metadata Analysis**: Analyze provider, region, and instance metadata to enrich the footprint calculation.

## Getting Started
Before you begin, ensure you have Python installed on your system. This project is compatible with Python 3.

### Prerequisites
- Obtain an API key from [Climatiq](https://www.climatiq.io/docs/api-reference).
- Install necessary Python libraries with:
  `pip3 install -r requirements.txt`
- Create a metadata.json file by making a GET request to the compute endpoint of the Climatiq API.

### Installation
1. Clone this repository or download the ZIP file.
2. Navigate to the directory and install the required Python libraries: 
3. Ensure you have a valid API key from Climatiq and a metadata.json file in your project directory.

### Running the Dashboard
Launch the Streamlit dashboard with:
bash
streamlit run dashboard.py
Access the dashboard through your web browser at: <http://localhost:8502>.

## Project Structure
Here's a brief overview of the key scripts in the Cloud-Carbon project:
- dashboard.py: This is the core script that initializes and renders the Streamlit dashboard, serving as the entry point for users to interact with the carbon footprint calculation features.
- dash_functions.py: Contains utility functions crucial for the dashboard's operations, such as constructing request payloads, invoking API calls, and handling responses.

## Contributing
We welcome contributions! If you're interested in improving Cloud-Carbon or have suggestions, please feel free to fork the repository, make your changes, and submit a pull request.