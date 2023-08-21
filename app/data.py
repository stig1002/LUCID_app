import pandas as pd
import streamlit as st


class DatasetPair(object):
    def __init__(
        self, datasetdict: dict = None, key=None, protected_features=[]
    ):
        self.datasetdict = datasetdict
        self.key = key
        self.protected_features = protected_features

        if datasetdict != None:
            self.dataset_names = list(datasetdict.keys())
        else:
            self.dataset_names = []

    def set_key(self, key):
        self.key = key

    def set_protected_features(self, protected_features):
        self.protected_features = protected_features

    def get_data(self):
        return self.datasetdict

    def get_key(self):
        return self.key

    def get_protected_features(self):
        return self.protected_features

    def capitalize_columns(self):
        datasetdict = self.datasetdict
        dataset_names = self.dataset_names

        for dataset in dataset_names:
            datasetdict[dataset].columns = datasetdict[
                dataset
            ].columns.str.capitalize()

    def get_categorical_cols(self):
        datasetdict = self.datasetdict
        dataset_names = self.dataset_names
        protected_features = self.protected_features

        dataset1 = dataset_names[0]

        return (
            datasetdict[dataset1]
            .filter(items=protected_features)
            .select_dtypes(include="object")
            .columns.tolist()
        )

    def get_numerical_cols(self):
        datasetdict = self.datasetdict
        dataset_names = self.dataset_names
        protected_features = self.protected_features

        dataset1 = dataset_names[0]

        return (
            datasetdict[dataset1]
            .filter(items=protected_features)
            .select_dtypes(include="number")
            .columns.tolist()
        )

    def get_missingvalues(self, feature_to_plot):
        datasetdict = self.datasetdict
        dataset_names = self.dataset_names

        dataset1 = dataset_names[0]
        dataset2 = dataset_names[1]

        # add missing categories in feature_to_plot (needed for representative plotting)
        unique_values_dataset1 = datasetdict[dataset1][
            feature_to_plot
        ].unique()
        unique_values_dataset2 = datasetdict[dataset2][
            feature_to_plot
        ].unique()

        # Missing values
        missing_values_dataset1 = set(unique_values_dataset2) - set(
            unique_values_dataset1
        )
        missing_values_dataset2 = set(unique_values_dataset1) - set(
            unique_values_dataset2
        )

        return {
            dataset1: missing_values_dataset1,
            dataset2: missing_values_dataset2,
        }


def adult(discrimination_key):
    """
    Explains the adult dataset/model (excludes race and sex in indirect discrimination)
    """
    dataset_text = """
            - Model to predict who earns 💰 +50k/y based on these variables:
                - Age
                - Workclass
                - Final weight ??
                - Education
                - Educational years
                - Martial status
                - Occupation
                - Relationship
                - Capital gain
                - Capital loss
                - Working hours per week
                - Native country
            """
    if discrimination_key == "direct":
        st.code(
            dataset_text
            + """    - Race
                - Sex"""
        )
    else:
        st.code(dataset_text)


def compas(discrimination_key):
    """
    Explains the adult dataset/model (excludes race and sex in indirect discrimination)
    """
    dataset_text = """
        - Model to predict if a person will commit recidivism 🚓 👮‍♀️ in the next two years.

        - Variables:
            - Age
            - Charge degree
            - Prior criminal records
            - Days between screening and arrest
            - Decile score: indicate the risk of recidivism
            - Length of stay in jail
    """
    if discrimination_key == "direct":
        st.code(
            dataset_text
            + """        - Race
            - Sex"""
        )
    else:
        st.code(dataset_text)
