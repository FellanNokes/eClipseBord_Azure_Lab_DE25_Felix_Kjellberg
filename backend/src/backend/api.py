from fastapi import FastAPI
from backend.data_processing import df


app = FastAPI()


@app.get("/eclipse/solar")
async def show_data():
    return df.to_dict(orient="records")