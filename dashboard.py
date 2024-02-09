"Main dashboard for the Cloud Carbon platform."

import streamlit as st

from dash_functions import (convert_provider_name,
                            read_metadata,
                            reset_batches,
                            calculate,
                            generate_vm_request_body,
                            generate_storage_request_body,
                            create_piechart)


TIME_UNIITS = ["h","ms","s","m","day","year"]
DATA_UNITS = ["MB","GB","TB"]


if __name__ == "__main__":

    st.markdown("# ☁️ Cloud Carbon")
    st.markdown("#### Calculate the emissions of your cloud resources")

    metadata = read_metadata("metadata.json")

    if "aws_vm_batch" not in st.session_state:
        st.session_state["aws_vm_batch"] = []
    if "azure_vm_batch" not in st.session_state:
        st.session_state["azure_vm_batch"] = []
    if "gcp_vm_batch" not in st.session_state:
        st.session_state["gcp_vm_batch"] = []
    if "aws_store_batch" not in st.session_state:
        st.session_state["aws_store_batch"] = []
    if "azure_store_batch" not in st.session_state:
        st.session_state["azure_store_batch"] = []
    if "gcp_store_batch" not in st.session_state:
        st.session_state["gcp_store_batch"] = []

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
    calculation_type = st.selectbox("Service", options=["Virtual Machine","Storage"], label_visibility="hidden")

    if calculation_type == "Virtual Machine":
        with st.form("vm_form"):

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

            vm_submitted = st.form_submit_button("Add to Calculation")
            if vm_submitted:
                vm_body = generate_vm_request_body(region, instance_type, duration, unit, vcpu_utilization)
                st.session_state[f"{provider}_vm_batch"].append(vm_body)


    if calculation_type == "Storage":
        with st.form("storage_form"):
            fcol5, fcol6, fcol7, fcol8, fcol9 = st.columns([2,1,1,1,1])

            with fcol5:
                storage_type = st.selectbox("Storage Type", options=["Solid-state Drive","Hard Disk Drive"])
            with fcol6:
                duration = st.number_input("🕗 Duration", min_value=1, step=1, help="The time the data is stored for.")
            with fcol7:
                unit = st.selectbox("Unit", options=TIME_UNIITS, label_visibility="hidden")
            with fcol8:
                data_stored = st.number_input("Data", min_value=0.1, step=0.1, help="The amount of data stored.")
            with fcol9:
                data_unit = st.selectbox("Data Unit", options=DATA_UNITS, label_visibility="hidden")
            
            storage_submitted = st.form_submit_button("Add to Calculation")
            if storage_submitted:
                storage_body = generate_storage_request_body(region, storage_type, duration, data_stored, data_unit, unit)
                st.session_state[f"{provider}_store_batch"].append(storage_body)


    col3, col4 = st.columns(2)
    with col3:
        calculate_bool = st.button("Calculate")
    with col4:
        st.button("Reset Calculation", on_click=reset_batches)
    
    if calculate_bool:
        vm_result = calculate("vm")
        store_result = calculate("store")

        result_breakdown = vm_result | store_result

        total_co2e = 0
        store_co2e = 0
        vm_co2e = 0
    
        for key, value in result_breakdown.items():
            total_co2e += value
            c_type = key.split("_")[-1]
            if c_type == "store":
                store_co2e += value
            if c_type == "vm":
                vm_co2e += value
    
        col5, col6 = st.columns(2)
        with col5:
            st.metric("Total CO2 (kg)", value=round(total_co2e, 5))
            if vm_co2e > 0 and store_co2e > 0:
                st.metric("Virtual Machines CO2 (kg)", value=round(vm_co2e, 5))
                st.metric("Storage CO2 (kg)", value=round(store_co2e, 5))
        with col6:
            st.altair_chart(create_piechart(result_breakdown), use_container_width=True)

    for item in st.session_state.items():
        if item[0] in ("gcp_vm_batch","aws_vm_batch","azure_vm_batch") and item[1]:
            provider_name = item[0].split("_")[0]
            provider_name = convert_provider_name(provider_name)
            with st.expander(f"{provider_name} VM - {len(item[1])}"):
                item[1]
        if item[0] in ("gcp_store_batch","aws_store_batch","azure_store_batch") and item[1]:
            provider_name = item[0].split("_")[0]
            provider_name = convert_provider_name(provider_name)
            with st.expander(f"{provider_name} Storage - {len(item[1])}"):
                item[1]
