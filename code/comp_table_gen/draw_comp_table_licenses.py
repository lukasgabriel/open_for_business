import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def load_license_data(file_path: str) -> pd.DataFrame:
    """Load data from excel and pivot."""
    df = pd.read_excel(file_path)
    return df.set_index("Name (SPDX Identifier)").transpose()


def map_values(value: str) -> float:
    if value == "Yes":
        return 1
    elif value == "No":
        return 0
    elif value == "Manually":
        return 0.25
    elif value == "Public Domain":
        return 1
    elif value == "Permissive":
        return 1
    elif (
        value == "GPLv3 only"
        or "GPL only"
        or "GPLv3 compatible only"
        or "GPLv2 compatible only"
    ):
        return 0.75
    elif value == "Copylefted":
        return 0.75
    elif value == "Restricted":
        return 0.25
    elif value == "Partial":
        return 0.5
    else:
        return 0.1


def plot_license_heatmap(data: pd.DataFrame):
    """Plot table of license attributes."""
    heatmap_values = data.applymap(map_values)

    # Sort columns based on feature count
    sorted_columns = heatmap_values.sum().sort_values(ascending=False).index
    heatmap_values = heatmap_values[sorted_columns]

    # Create mask for "Unknown" values
    mask_unknown = (data == "Unknown")[sorted_columns]
    annotation_df = data.where(~mask_unknown, "")

    # Set plot settings and colors
    pal = sns.diverging_palette(20, 200, as_cmap=True)
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.figure(figsize=(14, 16))

    ax = sns.heatmap(
        heatmap_values,
        cmap=pal,
        annot=annotation_df[sorted_columns],
        fmt="s",
        cbar=False,
        linewidths=0.5,
        linecolor="black",
        mask=mask_unknown,
    )

    # Customize plot
    ax.set_facecolor("#f2f2f2")  # Set background color for "Unknown" values
    plt.title("Open-Source License Attributes", fontsize=18)
    plt.ylabel("Attributes", fontsize=16)
    plt.xlabel("Licenses", fontsize=16)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    # Save plot
    plt.rcParams["savefig.dpi"] = 600
    plt.rcParams["svg.fonttype"] = "path"
    plt.savefig("license_attributes_heatmap.svg", format="svg", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    data = load_license_data("./license_attributes.xlsx")
    plot_license_heatmap(data)
