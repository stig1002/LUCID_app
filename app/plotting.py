import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def plot(dataset, feature_to_plot, categorical_columns, missing_values=[]):
    """
    Based on the feature to plot (categorical vs continuous) a plot is generated.
    To know the difference, you have to include a list of colnames with categorical data.
    Additionally a list of missing colnames is needed to included categories with zero count.
    """

    if feature_to_plot in categorical_columns:
        counts = dataset[feature_to_plot].value_counts().reset_index()

        counts.columns = [feature_to_plot, "Count"]

        # Add any missing values
        missing_values_df = pd.DataFrame(
            {feature_to_plot: list(missing_values), "Count": 0}
        )
        counts = pd.concat([counts, missing_values_df], ignore_index=True)

        # Calculate percentages
        total_count = counts["Count"].sum()
        counts["Percentage"] = counts["Count"] / total_count * 100

        # Make barchart with altair
        chart = (
            alt.Chart(counts)
            .mark_bar(width=20)
            .encode(
                x=alt.X("Percentage", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y(feature_to_plot),
                color=alt.Color(
                    feature_to_plot, scale=alt.Scale(scheme="category10")
                ),
                tooltip=[feature_to_plot, "Percentage"],
            )
            .properties(height=alt.Step(40))
        )

        # Show barchart in streamlit
        st.altair_chart(chart, use_container_width=True)
    else:
        # Count each value
        count_data = dataset[feature_to_plot].value_counts().reset_index()
        count_data.columns = [feature_to_plot, "Count"]

        # Make barchart with altair
        chart = (
            alt.Chart(count_data)
            .mark_bar()
            .encode(
                x=alt.X(
                    feature_to_plot,
                    bin=alt.Bin(maxbins=10),
                    title=feature_to_plot,
                ),
                y="Count",
                tooltip=[feature_to_plot, "Count"],
            )
        )
        # Show barchart in streamlit
        st.altair_chart(chart, use_container_width=True)


def combined_alt_plot(datasetpair, plotting_texts):
    """
    Makes an  plot for each dataset in a datasetpair with an extra argument 'plotting_texts' to specify a title for each.
    (altair package)
    """
    datasets = datasetpair.get_data()
    dataset_names = list(datasets.keys())
    dataset1 = dataset_names[0]
    dataset2 = dataset_names[1]

    categorical_columns = datasetpair.get_categorical_cols()

    num_columns = datasetpair.get_numerical_cols()

    feature_to_plot = st.radio(
        " ", sorted(categorical_columns + num_columns), key="alt"
    )

    missing_values = datasetpair.get_missingvalues(feature_to_plot)

    st.markdown("")  # white space
    st.markdown(plotting_texts[0])
    plot(
        datasets[dataset1],
        feature_to_plot,
        categorical_columns,
        missing_values[dataset1],
    )

    st.markdown(plotting_texts[1])
    plot(
        datasets[dataset2],
        feature_to_plot,
        categorical_columns,
        missing_values[dataset2],
    )


def combined_math_plot(datasetpair, plotting_texts):
    """
    Makes a plot to compare each dataset in a datasetpair with an extra argument 'plotting_texts' to specify a title for each.
    (matplotlib package)
    """

    # Change style
    plt.rcParams["text.color"] = "white"
    plt.rcParams["axes.labelcolor"] = "white"
    plt.rcParams["xtick.color"] = "white"
    plt.rcParams["ytick.color"] = "white"
    plt.rcParams["axes.facecolor"] = "black"
    plt.style.use("dark_background")

    # get the data from the dataset pairs
    datasets = datasetpair.get_data()
    dataset_names = list(datasets.keys())
    dataset1 = dataset_names[0]
    dataset2 = dataset_names[1]

    categorical_columns = datasetpair.get_categorical_cols()

    num_columns = datasetpair.get_numerical_cols()

    feature_to_plot = st.radio(
        " ", sorted(categorical_columns + num_columns), key="math"
    )

    missing_values = datasetpair.get_missingvalues(feature_to_plot)

    # Dataframes
    df1 = datasets[dataset1]
    df2 = datasets[dataset2]

    if feature_to_plot in categorical_columns:
        counts_df1 = df1[feature_to_plot].value_counts().reset_index()
        counts_df2 = df2[feature_to_plot].value_counts().reset_index()

        counts_df1.columns = [feature_to_plot, "Count"]
        counts_df2.columns = [feature_to_plot, "Count"]

        # Add any missing values
        missing_values_df1 = pd.DataFrame(
            {feature_to_plot: list(missing_values[dataset1]), "Count": 0}
        )
        missing_values_df2 = pd.DataFrame(
            {feature_to_plot: list(missing_values[dataset2]), "Count": 0}
        )
        counts_df1 = pd.concat(
            [counts_df1, missing_values_df1], ignore_index=True
        )
        counts_df2 = pd.concat(
            [counts_df2, missing_values_df2], ignore_index=True
        )

        # Calculate percentages
        total_count_df1 = counts_df1["Count"].sum()
        total_count_df2 = counts_df2["Count"].sum()

        counts_df1["Percentage"] = counts_df1["Count"] / total_count_df1 * 100
        counts_df2["Percentage"] = counts_df2["Count"] / total_count_df2 * 100

        # combine the dataframes based on the feature to plot.
        df_combined = pd.merge(counts_df1, counts_df2, on=feature_to_plot)

        # Plot the grouped barplot
        fig, ax = plt.subplots()
        y = range(len(df_combined))
        bar_height = 0.35

        # Bars for the first dataset
        rects1 = ax.barh(
            y,
            counts_df1["Percentage"],
            bar_height,
            label=dataset1.capitalize(),
        )

        # Bars for the second dataset
        rects2 = ax.barh(
            [i + bar_height for i in y],
            counts_df2["Percentage"],
            bar_height,
            label=dataset2.capitalize(),
        )

        # Y axis labels
        ax.set_yticks([i + bar_height / 2 for i in y])
        ax.set_yticklabels(counts_df1[feature_to_plot])

        # labels
        ax.legend()
        ax.set_xlabel("Percentage")
        ax.set_ylabel(feature_to_plot)
        ax.set_title("Comparison between {} and {}".format(dataset1, dataset2))

        # print it to streamlit
        st.pyplot(fig)

    else:
        combined_df = pd.concat([df1, df2], ignore_index=True)

        # Calculate the minimal and maximal value of the bistograms. (based on bin_width 10)
        data_min = np.min(combined_df[feature_to_plot])
        data_min = (data_min // 10) * 10
        data_max = np.max(combined_df[feature_to_plot])
        data_max = (data_max // 10 + 1) * 10

        # Choose the bins with bin width 10
        bin_width = 10
        bins = np.arange(data_min, data_max + bin_width, bin_width)

        # Generate the histograms
        hist1, bins1 = np.histogram(df1[feature_to_plot], bins=bins)
        hist2, bins2 = np.histogram(df2[feature_to_plot], bins=bins)

        # Append an empty value. Necessary to plot.
        hist1 = np.append(hist1, 0)
        hist2 = np.append(hist2, 0)

        bar_width = 0.35

        # X-locations for the bars
        x = np.arange(len(bins))

        # Make a new figure and subplot
        fig, ax = plt.subplots()

        # Place the bars for the first dataset
        ax.bar(x + bar_width, hist1, bar_width, label=dataset1.capitalize())

        # Place the bars for the second dataset
        ax.bar(
            x + 2 * bar_width, hist2, bar_width, label=dataset2.capitalize()
        )

        # labels
        ax.set_xlabel(feature_to_plot)
        ax.set_ylabel("Counts")
        ax.set_title("Comparison between {} and {}".format(dataset1, dataset2))

        # X axis labels
        ax.set_xticks(x)
        ax.set_xticklabels(bins.astype(int))

        # legend
        ax.legend()

        # print it to streamlit
        st.pyplot(fig)
