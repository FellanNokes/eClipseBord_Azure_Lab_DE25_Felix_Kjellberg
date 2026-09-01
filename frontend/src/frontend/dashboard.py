import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import httpx
import os


# try to get enviroment variable BACKEND_URL, if not exist default to 2nd argument
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def main():
    st.markdown("# SolarEclipse")
    st.write(BASE_URL)

    solar = httpx.get(f"{BASE_URL}/eclipse/solar", timeout = 30).json()
    df = pd.DataFrame(solar)

    df_filtered = year_filter(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total amount of eclipses", len(df_filtered))
    col2.metric("Most common type", df_filtered["eclipse_type"].value_counts().idxmax())
    col3.metric("Mean magnitude", round(df_filtered["eclipse_magnitude"].mean(), 2))

    st.dataframe(df_filtered)
    show_eclipse_map(df_filtered)
    show_eclipse_type_chart(df_filtered)
    show_path_width_chart(df_filtered)


def show_eclipse_type_chart(df):
    counts = df["eclipse_type"].value_counts()
    st.bar_chart(counts, x_label="Eclipse Type", y_label="Count")

def show_path_width_chart(df):
    path_width = df[df["path_width_km"] != "missing"]["path_width_km"].astype(float)
    binned, bins = pd.cut(path_width, bins=10, retbins=True)
    counts = binned.value_counts().sort_index()
    counts.index = [f"{int(edge)}km" for edge in bins[1:]]
    st.bar_chart(counts, x_label="Path Width (km)", y_label="Frequency")

# Got help from LLM with creating this
def show_eclipse_map(df):
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_radius=100000,
        get_fill_color=[200, 30, 0, 160],
        pickable=True,
    )

    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1)

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Date and time: {calendar_date} {eclipse_time} Magnitude: {eclipse_magnitude}"},
    ))

def year_filter(df):
    year_range = st.slider("Year", 0, 2100,(2000, 2026))
    return df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

if __name__ == "__main__":
    main()