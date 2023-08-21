import base64

import pandas as pd
import streamlit as st


def empty_function(var=None):
    """
    Placeholder if needed
    """
    pass


def write_features(featurelist):
    """
    Presents selected features from a list in bullet points
    """
    st.code("\n".join(["* {}".format(feature) for feature in featurelist]))


def upload_csv(text):
    """
    Shows an uploader object with as title "Upload a CSV-file"
    Asks the user which protected features to analyze further
    Returns a panda dataframe
    If nothing is uploaded, an empty dataframe is returned
    """

    uploaded_file = st.file_uploader(text, type="csv")

    if uploaded_file is not None:
        # Load data from uploaded file
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.capitalize()
        return data

    else:
        return pd.DataFrame()


def ask_protected_features(data):
    """
    Asks the user which features he/she wants to analyze.
    Returns a list of these features.
    When an empty dataframe was given, an empty list is returned.
    """
    if not data.empty:
        allvariables = data.columns
        protected_features = []

        st.markdown("Please include all protected features you wish analyze.")

        for variable in allvariables:
            if st.checkbox(variable):
                protected_features.append(variable)

        st.write("Selected features:")
        write_features(protected_features)

        return protected_features
    else:
        return []


def read_data(dataset_key, model_key, discrimination_key):
    """
    read csv's with names composed of dataset_key, model_key, discrimination_key
    lucid model requires a lucid file and a uniform distribution file
    lucid gan model requires a two files of positive and negative cases, respectively.
    """
    ## to change: download once alle files from github and cache it. (not needed anymore)
    if model_key == "lucid":
        csv_lucid_file = "./data/{}_lucid_{}.csv".format(
            dataset_key, discrimination_key
        )
        csv_uniform_file = "./data/{}_uniform_{}.csv".format(
            dataset_key, discrimination_key
        )
        return {
            "uniform": pd.read_csv(csv_uniform_file),
            "lucid": pd.read_csv(csv_lucid_file),
        }
    elif model_key == "lucid_gan":
        csv_pos_file = "./data/{}_lucid_gan_pos_{}.csv".format(
            dataset_key, discrimination_key
        )
        csv_neg_file = "./data/{}_lucid_gan_neg_{}.csv".format(
            dataset_key, discrimination_key
        )
        return {
            "pos": pd.read_csv(csv_pos_file),
            "neg": pd.read_csv(csv_neg_file),
        }


def export_dataframe(dataframe, filename, display_text):
    """
    Export dataframe as csv file with a certain text displayed.
    """
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{display_text}</a>'
    return href
