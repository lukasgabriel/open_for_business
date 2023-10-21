import pandas as pd
import plotly.graph_objects as go


# Function to prepare data (both with and without "Other" grouping)
def prepare_data(data_path):
    data = pd.read_csv(data_path)
    grouped_data_all = (
        data.groupby("license")
        .sum()
        .reset_index()
        .sort_values(by="f0_", ascending=False)
    )

    threshold = data.sort_values(by="f0_", ascending=False).iloc[9]["f0_"]
    data.loc[data["f0_"] < threshold, "license"] = "Other"
    grouped_data_other = (
        data.groupby("license")
        .sum()
        .reset_index()
        .sort_values(by="f0_", ascending=False)
    )

    return grouped_data_all, grouped_data_other


# Prepare data for both GitHub and libraries.io
github_all, github_other = prepare_data("bquxjob_4802e09_18a136a0aa7.csv")
libraries_all, libraries_other = prepare_data("bquxjob_33114a4c_18a1382b220.csv")

# Create initial figure with GitHub data with "Other" grouping
fig = go.Figure(
    go.Bar(x=github_other["f0_"], y=github_other["license"], orientation="h")
)

# Add buttons
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            showactive=True,
            buttons=[
                dict(
                    label="GitHub (Group 'Other')",
                    method="update",
                    args=[
                        {"x": [github_other["f0_"]], "y": [github_other["license"]]},
                        {"title": "GitHub Licenses with 'Other' Grouped"},
                    ],
                ),
                dict(
                    label="GitHub (Show All)",
                    method="update",
                    args=[
                        {"x": [github_all["f0_"]], "y": [github_all["license"]]},
                        {"title": "GitHub All Licenses"},
                    ],
                ),
                dict(
                    label="libraries.io (Group 'Other')",
                    method="update",
                    args=[
                        {
                            "x": [libraries_other["f0_"]],
                            "y": [libraries_other["license"]],
                        },
                        {"title": "libraries.io Licenses with 'Other' Grouped"},
                    ],
                ),
                dict(
                    label="libraries.io (Show All)",
                    method="update",
                    args=[
                        {"x": [libraries_all["f0_"]], "y": [libraries_all["license"]]},
                        {"title": "libraries.io All Licenses"},
                    ],
                ),
            ],
        )
    ]
)

# Set plot title and axis labels
fig.update_layout(
    title="GitHub Licenses with 'Other' Grouped",
    xaxis_title="Number of Repositories Using License",
    yaxis_title="License",
)


# Save plot to HTML
fig.write_html("interactive_plot_multi.html")
fig.show()
