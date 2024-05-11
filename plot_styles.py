import matplotlib.pyplot as plt

# Define the colors from the C-CoMP pallette
LIGHT_BLUE = "#3CB3C0"
DARK_BLUE = "#024064"
ORANGE = "#FF6C2C"


# Define the style for the plots (gray axes, no top or right axis lines)
def set_plot_style(g):
    # Make the axis lines gray
    g.spines["bottom"].set_color("gray")
    g.spines["left"].set_color("gray")
    # Make the tick marks gray
    g.tick_params(axis="x", colors="gray")
    g.tick_params(axis="y", colors="gray")
    # Remove the top and right axis lines
    g.spines["top"].set_visible(False)
    g.spines["right"].set_visible(False)


def carbon_fates_bar(data):
    # Check that the column names and order are correct
    assert data.columns.to_list() == ["biomass", "organic_c", "co2"]
    # Plot the stacked bar plot
    g = data.plot(kind="bar", stacked=True, color=[DARK_BLUE, LIGHT_BLUE, ORANGE])
    # Add the title and axis labels (in gray)
    g.set_title("Fate of Carbon", color="gray")
    g.set_xlabel("Simulation Conditions", color="gray")
    g.set_ylabel("Carbon Flux (mmol C/ mmol C)", color="gray")  # TODO: Check the units
    # Use tight layout so that the axis labels are not cut off
    plt.tight_layout()
    # Move the legend outside of the plot
    custom_labels = ["Biomass", "Organic C", "CO2"]
    lgd = plt.legend(
        bbox_to_anchor=(1, 0.5),
        loc="center left",
        borderaxespad=1,
        labels=custom_labels,
    )
    # Extend the plot area to fit the legend
    plt.subplots_adjust(right=0.75)
    # Make the legend text gray too
    for text in lgd.get_texts():
        text.set_color("gray")
    # Style
    set_plot_style(g)

    # Return the plot
    return g
