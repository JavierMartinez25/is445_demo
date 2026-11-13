import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(
    page_title="IS445 HW6 - Bigfoot Sightings",
    layout="wide"
)

st.title("Bigfoot Sightings in the United States")

st.write(
    "This project explores reported Bigfoot sightings across "
    "different states and seasons using the BFRO dataset. "
    "The two visualizations show where reports are most common "
    "and how they vary throughout the year."
)

data_url = (
    "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/"
    "is445_data/main/bfro_reports_fall2022.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(
        data_url,
        usecols=["state", "season", "classification"]
    )

    df["state"] = df["state"].fillna("").str.strip()
    df["season"] = (
        df["season"].fillna("").str.strip().str.title()
    )
    df["classification"] = (
        df["classification"]
        .fillna("Unclassified")
        .str.strip()
    )

    df = df[df["state"] != ""]

    return df

df = load_data()

state_counts = (
    df.groupby("state")
    .size()
    .reset_index(name="reports")
    .sort_values("reports", ascending=False)
    .head(15)
)

click = alt.selection_point(
    fields=["state"],
    empty=True,
    clear="dblclick"
)

bars = (
    alt.Chart(state_counts)
    .mark_bar()
    .encode(
        x=alt.X(
            "reports:Q",
            title="Number of Reports",
            scale=alt.Scale(zero=True)
        ),
        y=alt.Y(
            "state:N",
            sort="-x",
            title="State"
        ),
        color=alt.condition(
            click,
            alt.value("steelblue"),
            alt.value("lightgray")
        ),
        tooltip=[
            alt.Tooltip("state:N", title="State"),
            alt.Tooltip("reports:Q", title="Reports")
        ]
    )
    .properties(
        width=700,
        height=430,
        title="Visualization 1: Top 15 States by Bigfoot Reports"
    )
    .add_params(click)
)

seasons = ["Spring", "Summer", "Fall", "Winter"]

season_df = df[df["season"].isin(seasons)].copy()

season_counts = (
    season_df.groupby(
        ["state", "season", "classification"]
    )
    .size()
    .reset_index(name="reports")
)

season_chart = (
    alt.Chart(season_counts)
    .mark_bar()
    .encode(
    x=alt.X(
        "season:N",
        sort=seasons,
        title="Season",
        axis=alt.Axis(labelAngle=0)
        ),
        y=alt.Y(
            "sum(reports):Q",
            title="Number of Reports",
            scale=alt.Scale(zero=True)
        ),
    color=alt.Color(
        "classification:N",
        title="Report Classification",
        scale=alt.Scale(scheme="tableau10"),
        legend=alt.Legend(orient="bottom")
        ),
        tooltip=[
            alt.Tooltip("season:N", title="Season"),
            alt.Tooltip(
                "classification:N",
                title="Classification"
            ),
            alt.Tooltip(
                "sum(reports):Q",
                title="Reports"
            )
        ]
    )
    .transform_filter(click)
    .properties(
        width=700,
        height=320,
        title="Visualization 2: Bigfoot Reports by Season"
    )
)

st.header("Interactive Visualizations")

st.write(
    "The first chart compares the 15 states with the most "
    "reported Bigfoot sightings. The second chart shows "
    "the number of reports by season and classification."
)

st.info(
    "Click on a state in the first chart to filter the "
    "second chart. Double-click to clear the selection "
    "and return to all states."
)
chart = alt.vconcat(
    bars,
    season_chart,
    spacing=35
)

st.altair_chart(chart, use_container_width=True)

st.divider()

st.header("Visualization 1 Write-Up")
st.subheader("Bigfoot Reports by State")

st.write(
    """
    For my first visualization, I wanted to show which states
    have the highest number of reported Bigfoot sightings.
    I chose a horizontal bar chart because it makes comparing
    states easier, especially with the state names along the
    y-axis. I used a scale starting at zero and sorted the
    bars from highest to lowest so the differences are easier
    to see. Washington has the most reports, followed by
    California. I also added interactivity so users can click
    on a state and see the second chart update to show only
    that state's seasonal reports. The selected state stays
    blue while the other bars turn gray, making it easier
    to see which state is selected. If I had more time,
    I would compare the number of reports with each state's
    population to see if the rankings would change.
    """
)

st.write(
    "HW5 overlap: I did not complete Homework 5, "
    "so no plots, analysis, or written material "
    "from HW5 were reused in this visualization."
)

st.divider()

st.header("Visualization 2 Write-Up")
st.subheader("Bigfoot Reports by Season")

st.write(
    """
    For my second visualization, I wanted to explore how
    Bigfoot reports vary throughout the year and across
    different report classifications. I chose a stacked
    bar chart because it shows the total number of reports
    for each season while also separating them by
    classification. I placed the seasons in order along
    the x-axis and used a scale starting at zero on the
    y-axis. I also used different colors to make the
    classifications easier to distinguish. Looking at the
    overall data, summer has the most reported sightings,
    while winter has the fewest. This chart is linked to
    the first visualization, so when I click on a state,
    the seasonal chart automatically changes to show
    reports for that state. This makes it possible to
    compare seasonal patterns across different states
    instead of only looking at the overall totals.
    If I had more time, I would add an option to compare
    percentages instead of just the total number of reports.
    """
)

st.write(
    "HW5 overlap: I did not complete Homework 5, "
    "so no plots, analysis, or written material "
    "from HW5 were reused in this visualization."
)