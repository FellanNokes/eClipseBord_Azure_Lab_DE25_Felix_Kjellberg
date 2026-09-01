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
# Creating year from calendar date
df["year"] = df["calendar_date"].str.split(" ").str[0].astype(int)
# Filling nulls and replacing - with missing based on EDA
df["path_width_km"] = df["path_width_km"].replace("-", pd.NA).fillna("missing")
df["central_duration"] = df["central_duration"].replace("-", pd.NA).fillna("missing")

# Converting coordinates (got help from LLM with this)
def convert_coord(val):
    direction = val[-1]
    number = float(val[:-1])
    return -number if direction in ["S", "W"] else number

df["lat"] = df["latitude"].apply(convert_coord)
df["lon"] = df["longitude"].apply(convert_coord)