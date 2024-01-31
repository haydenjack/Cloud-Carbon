"Main dashboard for the Cloud Carbon platform."

import streamlit as st

from dash_functions import (convert_provider_name,
                            read_metadata,
                            reset_batches,
                            calculate,
                            generate_vm_request_body)


TIME_UNIITS = ["h","ms","s","m","day","year"]


if __name__ == "__main__":

    st.markdown("# ☁️ Cloud Carbon")
    st.markdown("#### Calculate the emissions of your cloud resources")

    metadata = read_metadata("metadata.json")


    if "aws_batch" not in st.session_state:
        st.session_state["aws_batch"] = []
    if "azure_batch" not in st.session_state:
        st.session_state["azure_batch"] = []
    if "gcp_batch" not in st.session_state:
        st.session_state["gcp_batch"] = []

    col1, col2 = st.columns(2)

    with col1:
        provider = st.selectbox("Provider",
                                options=["Amazon Web Services","Microsoft Azure","Google Cloud Platform"])
        provider = convert_provider_name(provider)

    with col2:
        valid_regions = metadata["cloud_providers"][provider]["regions"]
        region = st.selectbox("Region",
                            options=valid_regions)

    valid_instances = metadata["cloud_providers"][provider]["virtual_machine_instances"]

    with st.form("my_form"):
        fcol1, fcol2, fcol3, fcol4 = st.columns([2,1,1,2])

        with fcol1:
            instance_type = st.selectbox("Instance Type", options=valid_instances)
        with fcol2:
            duration = st.number_input("🕗 Duration", min_value=1, step=1, help="The time the virtual machine has been running.")
        with fcol3:
            unit = st.selectbox("Unit", options=TIME_UNIITS)
        with fcol4:
            vcpu_utilization = st.slider("Avg. vCPU Utilisation",
                      min_value=0.1, max_value=1.0,
                      value=0.5,
                      help="Default is 0.5 if unknown")

        form_output = st.form_submit_button("Add to Calculation")
        if form_output:
            vm_body = generate_vm_request_body(region, instance_type, duration, unit, vcpu_utilization)
            st.session_state[f"{provider}_batch"].append(vm_body)

    col3, col4 = st.columns(2)
    with col3:
        calculate_bool = st.button("Calculate")
        if calculate_bool:
            calculation_result = round(calculate(),5)
            st.metric(label="Total CO2 emissions",value=f"{str(calculation_result)}kg")
    with col4:
        st.button("Reset Calculation", on_click=reset_batches)


    for item in st.session_state.items():
        if item[0] in ("gcp_batch","aws_batch","azure_batch") and item[1]:
            provider_name = item[0].split("_")[0]
            provider_name = convert_provider_name(provider_name)
            with st.expander(f"{provider_name} - {len(item[1])}"):
                item[1]
