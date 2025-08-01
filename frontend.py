import streamlit as st
import requests
from networksecurity.constants.training_pipeline import BACKEND_URL
import pandas as pd
import os
 


st.set_page_config(
    page_title="Network Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


with st.sidebar:
    st.image("assets/Logo/Bastion.png", width=150)
    st.title("🛡️ Network Security App")
    st.info("This application selects the best machine learning model trained on various parameters related to a website to detect for phishing behaviour.")
    
    page = st.radio(
        "Choose a page:",
        ("Predict Intrusions", "Train Model"),
        key="navigation"
    )
    
    st.markdown("---")
    st.markdown(
        """
        **About:**
        - **Backend:** FastAPI
        - **Frontend:** Streamlit
        - **Model:** Scikit-learn based classifier for network data.
        """
    )


# Content
if page == "Train Model":
    st.title("🧠 Model Training Pipeline")
    st.markdown("---")
    st.warning("Training can take a significant amount of time and resources. Please proceed with caution.", icon="⚠️")

    # The button to trigger the training pipeline
    if st.button("Start New Training", type="primary", use_container_width=True):
        
        # Display a spinner while waiting for the backend
        with st.spinner("Training in progress... This may take several minutes."):
            try:
                # Make a GET request to the /train endpoint
                response = requests.get(f"{BACKEND_URL}/train", timeout=600) # Increased timeout for training
                
                # Check the response from the backend
                if response.status_code == 200:
                    st.success("✅ Training completed successfully!")
                    st.balloons()
                    st.info(f"Response from server: {response.text}")
                else:
                    st.error(f"❌ An error occurred during training.")
                    st.json({"status_code": response.status_code, "detail": response.text})
            
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not connect to the backend: {e}")
                st.info(f"Please ensure the FastAPI server is running at `{BACKEND_URL}`.")

elif page == "Predict Intrusions":
    st.title("🔍 Predict Network Intrusions")
    st.markdown("---")
    st.info("Upload a CSV file with one or more rows of data to predict if the URLs are malicious.", icon="📄")
    
    # --- Example Data Format Section ---
    st.write("#### 📄 Required CSV Format")
    st.info(
        "Your uploaded CSV file must contain the following columns. The values typically represent categories: "
        "`1` (feature is present), `0` (neutral), `-1` (feature is not present)."
    )
    example_data = {
        "having_IP_Address": 1, "URL_Length": -1, "Shortining_Service": 1, "having_At_Symbol": 1,
        "double_slash_redirecting": 1, "Prefix_Suffix": -1, "having_Sub_Domain": 1, "SSLfinal_State": 1,
        "Domain_registeration_length": 1, "Favicon": 1, "port": 1, "HTTPS_token": -1, "Request_URL": -1,
        "URL_of_Anchor": 1, "Links_in_tags": 1, "SFH": 0, "Submitting_to_email": 1, "Abnormal_URL": 1,
        "Redirect": 0, "on_mouseover": 1, "RightClick": 1, "popUpWidnow": 1, "Iframe": 1,
        "age_of_domain": 1, "DNSRecord": 1, "web_traffic": -1, "Page_Rank": -1, "Google_Index": 1,
        "Links_pointing_to_page": 1, "Statistical_report": 1
    }
    example_df = pd.DataFrame([example_data])
    st.dataframe(example_df)
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Choose a CSV file for prediction",
        type=["csv"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        st.markdown("---")
        st.write("### Uploaded Data Preview:")
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.dataframe(df_preview.head())
            
            num_rows = len(df_preview)

            uploaded_file.seek(0) 

            if st.button("Run Prediction", type="primary", use_container_width=True):
                with st.spinner("Predicting..."):
                    try:
                        files = {'file': (uploaded_file.name, uploaded_file, 'text/csv')}
                        response = requests.post(f"{BACKEND_URL}/predict", files=files, timeout=120)

                        if response.status_code == 200:
                            st.success("✅ Prediction successful!")
                            
                            if num_rows == 1:
                                try:
                                    result_df_list = pd.read_html(response.text)
                                    if result_df_list:
                                        result_df = result_df_list[0]
                                        prediction_value = result_df['predicted_column'].iloc[0]

                                        if prediction_value == 1:
                                            st.error("🚨 This URL is predicted to be MALICIOUS.", icon="🚨")
                                        else:
                                            st.success("✅ This URL is predicted to be SAFE.", icon="✅")
                                    else:
                                        st.warning("Could not find a table in the response from the server.")

                                except Exception as e:
                                    st.error(f"Failed to parse the prediction result: {e}")

                            else:
                                # If more than one row, display the full styled table as before.
                                st.markdown("<h3 style='color: #fafafa;'>Prediction Results:</h3>", unsafe_allow_html=True)
                                
                                table_styler_css = """
                                <style>
                                    .table {
                                        width: 100%; border-collapse: collapse; color: #e1e1e1; background-color: #0e1117;
                                    }
                                    .table th, .table td {
                                        border: 1px solid #3a3a3a; text-align: left; padding: 12px;
                                    }
                                    .table thead th {
                                        background-color: #262730; color: #fafafa; font-weight: bold;
                                    }
                                    .table-striped tbody tr:nth-of-type(odd) {
                                        background-color: #1a1c24;
                                    }
                                    .table-striped tbody tr:nth-of-type(even) {
                                        background-color: #0e1117;
                                    }
                                </style>
                                """
                                
                                backend_html = response.text
                                styled_html = table_styler_css + backend_html
                                st.components.v1.html(styled_html, height=600, scrolling=True)
                            
                        else:
                            st.error("❌ An error occurred during prediction.")
                            st.json({"status_code": response.status_code, "detail": response.text})

                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Could not connect to the backend: {e}")
                        st.info(f"Please ensure the FastAPI server is running at `{BACKEND_URL}`.")

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")