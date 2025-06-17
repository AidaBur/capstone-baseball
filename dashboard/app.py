import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set wide page layout
st.set_page_config(layout="wide")

st.markdown(
    """
    <h1 style="text-align:center; font-size:2.5rem; margin-bottom:0.2rem;">Baseball Analytics Dashboard</h1>
    <p style="text-align:center; font-size:1.2rem; color:#999;">Player • Pitcher • Team • Events</p>
    <p style="text-align:center; font-size:0.9rem; color:#888;">
        Data Source: <a href="https://www.baseball-almanac.com/yearmenu.shtml" target="_blank" style="color:#A0C4FF; text-decoration:none;">Baseball Almanac</a>
    </p>
    """,
    unsafe_allow_html=True
)

# Load cleaned data
player_df = pd.read_csv("dashboard/statistics_cleaned.csv")
pitcher_df = pd.read_csv("dashboard/pitcher_stats_cleaned.csv")
events_df = pd.read_csv("dashboard/events_cleaned.csv")

# Add type column and combine players + pitchers
player_df["Type"] = "Player"
pitcher_df["Type"] = "Pitcher"
combined_df = pd.concat([player_df, pitcher_df])

# SECTION 1: Focus Year (Collapsible)
st.markdown("## Focus Year")
with st.expander("Explore Yearly Statistics", expanded=True):
    selected_year = st.selectbox("Select Year", sorted(combined_df["Year"].unique()))
    st.markdown(f"### Top Stats in {selected_year} (Players & Pitchers)")

    # Bar chart of top stats + events for selected year
    col1, col2 = st.columns([2, 1])
    with col1:
        year_data = combined_df[combined_df["Year"] == selected_year]
        if not year_data.empty:
            fig = px.bar(
                year_data,
                x="Value",
                y="Name",
                color="Type",
                text="Statistic",
                orientation="h",
                title=f"Top Stats in {selected_year}",
                hover_data=["Team", "Statistic"],
                labels={"Value": "Value"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No player or pitcher data found for this year.")
    with col2:
        st.subheader(f"Notable Events in {selected_year}")
        year_events = events_df[events_df["Year"] == selected_year]
        if year_events.empty:
            st.info("No events found for this year.")
        else:
            for _, row in year_events.iterrows():
                description = row["Description"].lstrip(", ").strip()
                st.markdown(f"**{row['Date']}** — {description}")


# SECTION 2: Trends across all years
st.markdown("---")
st.markdown("## Statistics Across All Years")

with st.expander("Explore Trends & Highlights", expanded=True):
    # Filters: statistic and year range
    global_stat = st.selectbox("Choose a statistic to explore:", sorted(combined_df["Statistic"].unique()), key="global_stat")
    min_year, max_year = int(combined_df["Year"].min()), int(combined_df["Year"].max())
    selected_years = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(1920, 2000)
    )

    # Filter data by year range and stat
    start_year, end_year = selected_years
    filtered_df = combined_df[
        (combined_df["Year"] >= start_year) &
        (combined_df["Year"] <= end_year) &
        (combined_df["Statistic"] == global_stat)
    ]

    # Line chart: average stat over time
    st.subheader(f"Average {global_stat} Over Time ({start_year}–{end_year})")
    st.markdown("This chart shows how the selected statistic changes over time.")
    trend = filtered_df.groupby("Year")["Value"].mean().reset_index()
    fig_line = px.line(trend, x="Year", y="Value", markers=True, labels={"Value": global_stat})
    st.plotly_chart(fig_line, use_container_width=True)

    # Top 10 performers chart
    st.subheader(f"Top 10 Performers by {global_stat}")
    st.markdown("These are the top 10 players or pitchers by this stat.")
    top10 = filtered_df.sort_values("Value", ascending=False).head(10)
    fig_top = px.bar(
        top10,
        x="Value",
        y="Name",
        orientation="h",
        color="Team",
        text="Value",
        labels={"Value": global_stat}
    )
    st.plotly_chart(fig_top, use_container_width=True)

    # Heatmap of averages by type/year
    st.subheader("Heatmap of Averages by Year")
    st.markdown("This heatmap shows how average values differ across years and between players and pitchers.")
    pivot = combined_df[
        combined_df["Statistic"] == global_stat
    ].pivot_table(index="Type", columns="Year", values="Value", aggfunc="mean")
    fig_heat = px.imshow(pivot, aspect="auto", color_continuous_scale="Viridis")
    st.plotly_chart(fig_heat, use_container_width=True)


# SECTION 3: Team-based visualizations
st.markdown("---")
st.markdown("## Team-Based Visualizations")

with st.expander("Explore Team Insights", expanded=True):
    selected_team_stat = global_stat  # Reuse selected stat

    # Choose time period for team view
    team_period_label = st.radio(
        label="Select Time Period",
        options=["All Years", "Before 1920", "1921–2000", "2001–2025"],
        horizontal=True,
        key="team_period"
    )

    team_periods = {
        "All Years": (combined_df["Year"].min(), combined_df["Year"].max()),
        "Before 1920": (0, 1919),
        "1921–2000": (1921, 2000),
        "2001–2025": (2001, 2025),
    }
    team_start, team_end = team_periods[team_period_label]

    # Filter by year and stat
    team_filtered_df = combined_df[
        (combined_df["Year"] >= team_start) &
        (combined_df["Year"] <= team_end) &
        (combined_df["Statistic"] == selected_team_stat)
    ]

    # Choose team view type
    team_view = st.radio(
        "Choose team-based view:",
        ["Total value by team", "Teams with most top performers", "Trend by team over time"],
        horizontal=False,
        key="team_view"
    )

    # Bar: total stat by team
    if team_view == "Total value by team":
        st.subheader(f"Total {selected_team_stat} per Team ({team_period_label})")
        sum_team = team_filtered_df.groupby("Team")["Value"].sum().round(0).astype(int).sort_values(ascending=False).reset_index()
        fig_sum = px.bar(
            sum_team,
            x="Value",
            y="Team",
            orientation="h",
            text="Value",
            labels={"Value": f"Total {selected_team_stat}"}
        )
        st.plotly_chart(fig_sum, use_container_width=True)

    # Bar: count of top performers by team
    elif team_view == "Teams with most top performers":
        st.subheader(f"Top Performers Count by Team ({team_period_label})")
        top_performers = team_filtered_df.sort_values("Value", ascending=False).head(50)
        count_per_team = top_performers["Team"].value_counts().reset_index()
        count_per_team.columns = ["Team", "Top Performer Count"]
        fig_count = px.bar(count_per_team, x="Top Performer Count", y="Team", orientation="h")
        st.plotly_chart(fig_count, use_container_width=True)

    # Line chart: trend over time by team
    elif team_view == "Trend by team over time":
        st.subheader(f"Trend of {selected_team_stat} by Team Over Time ({team_period_label})")
        selected_team = st.selectbox("Select Team", sorted(team_filtered_df["Team"].dropna().unique()), key="team_trend_select")
        team_trend = team_filtered_df[team_filtered_df["Team"] == selected_team]
        trend_team = team_trend.groupby("Year")["Value"].mean().reset_index()
        fig_team_trend = px.line(trend_team, x="Year", y="Value", markers=True, labels={"Value": selected_team_stat})
        st.plotly_chart(fig_team_trend, use_container_width=True)


# SECTION 4: Tag Clouds
st.markdown("---")
st.markdown("## Tag Clouds")

with st.expander("Show Word Clouds", expanded=True):
    col1, col2 = st.columns(2)

    # Word Cloud of Player Names
    with col1:
        st.subheader("Player Names")
        names_text = " ".join(combined_df["Name"].dropna())
        name_wordcloud = WordCloud(
            width=400, height=300, background_color="white", colormap="Blues"
        ).generate(names_text)

        fig_name, ax_name = plt.subplots(figsize=(5, 3))
        ax_name.imshow(name_wordcloud, interpolation="bilinear")
        ax_name.axis("off")
        st.pyplot(fig_name)

    # Word Cloud of Team Names
    with col2:
        st.subheader("Team Names")
        team_text = " ".join(combined_df["Team"].dropna())
        team_wordcloud = WordCloud(
            width=400, height=300, background_color="white", colormap="Greens"
        ).generate(team_text)

        fig_team, ax_team = plt.subplots(figsize=(5, 3))
        ax_team.imshow(team_wordcloud, interpolation="bilinear")
        ax_team.axis("off")
        st.pyplot(fig_team)

