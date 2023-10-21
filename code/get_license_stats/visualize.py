import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size': 20})


def visualize_license_usage(infile):
    # Load CSV file into a DataFrame
    data = pd.read_csv(infile)

    # Handle NaN values in the license columns
    data['license'].fillna('Unknown', inplace=True)

    # Group licenses so only the 10 most popular licenses are shown
    threshold = data.sort_values(by="f0_", ascending=False).iloc[9]['f0_']

    # Group licenses with less usage than the threshold into 'Other'
    other_licenses_count = len(data[data['f0_'] < threshold]['license'].unique())  # Count for annotation
    data.loc[data['f0_'] < threshold, 'license'] = 'Other'
    grouped_data = data.groupby('license').sum().reset_index().sort_values(by='f0_', ascending=False)

    # Calculate total number of licenses observed (sum of f0_ column)
    total_licenses = data['f0_'].sum()

    # Create horizontal bar chart with changed dimensions
    fig, ax = plt.subplots(figsize=(18, 9))

    # Color differentiation for 'Other'
    colors = ['lightgrey' if license == 'Other' else 'grey' for license in grouped_data['license']]

    # Plotting horizontal bar chart
    bars = ax.barh(grouped_data['license'].astype(str), grouped_data['f0_'], color=colors)

    # Set title and labels with increased padding
    ax.set_title('Usage of Open Source Licenses\n$n = {:,}$'.format(total_licenses), fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Number of Repositories Using License', labelpad=16)
    ax.set_ylabel('License', labelpad=16)

    # Add footnote for "Other"
    labels = [item.get_text() for item in ax.get_yticklabels()]
    labels = ['Other¹' if label == 'Other' else label for label in labels]
    ax.set_yticklabels(labels)

    # Percentage Annotations
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width/total_licenses:.1%}',
                    xy=(width + total_licenses*0.02, bar.get_y() + bar.get_height()/2),
                    ha='center', va='center', fontsize=16)

    # Subtle grid
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    # Legend for "Other" with increased padding
    # ax.annotate(f'"Other" comprises {other_licenses_count} less common licenses',
    #                 xy=(0, 0), xycoords='axes fraction', xytext=(0.05, -30), textcoords='offset points', 
    #                 fontsize=12, color='dimgrey', verticalalignment='top')

    # Remove top and right spines for a minimalistic look
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Ensure both plots use German number format
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)).replace(',', '.')))

    # Increase size
    plt.rcParams['savefig.dpi'] = 600

    # Convert text to paths
    plt.rcParams['svg.fonttype'] = 'path'

    # Display plot with final layout adjustments
    plt.tight_layout()
    plt.show()

    # Save as svg
    fig.savefig(f"{infile.split('.')[0]}.svg", format="svg")


# Visualize data from both files
visualize_license_usage('bquxjob_4802e09_18a136a0aa7.csv')
visualize_license_usage('bquxjob_33114a4c_18a1382b220.csv')
