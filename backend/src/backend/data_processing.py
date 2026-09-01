from backend.constants import DATA_DIRECTORY
import pandas as pd

df = pd.read_csv(DATA_DIRECTORY / "solar.csv")
# Basic cleaning converting dataset into snakecase
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[()]", "", regex=True)
)
# Filling nulls with missing based on EDA
df["path_width_km"] = df["path_width_km"].fillna("missing")
df["central_duration"] = df["central_duration"].fillna("missing")