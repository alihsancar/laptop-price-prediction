import pandas as pd
import numpy as np
import pickle
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

with open('model_encoder_scaler.pkl', 'rb') as f:
    model_file = pickle.load(f)
    model = model_file['model']
    encoder = model_file['encoder']
    scaler = model_file['scaler']

class Laptop(BaseModel):
    Company: str
    TypeName: str
    Ram: int
    Weight: float
    TouchScreen: int
    Ips: int
    Ppi: float
    Cpu_brand: str
    HDD: int
    SSD: int
    Gpu_brand: str
    Os: str

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(features: Laptop):
    
    # Take input data and convert to dataframe.
    input_data = features.model_dump()
    input_data = pd.DataFrame([input_data])
    
    # Encode categorical columns
    input_empty = pd.DataFrame(index=input_data.index)
    for col in ['Company', 'TypeName', 'Cpu_brand', 'Gpu_brand', 'Os']:
        transformed_col = encoder[col].transform(input_data[[col]])
        col_name = encoder[col].get_feature_names_out([col])
        input_empty = pd.concat([input_empty, pd.DataFrame(transformed_col, columns=col_name, index=input_data.index)], axis=1)
   
    num_cols = [col for col in input_data.columns if input_data[col].dtype != 'O']
    input_empty = pd.concat([input_empty, input_data[num_cols]], axis=1)

    
    # Scaling process
    scaled_input = scaler.transform(input_empty)
    
    # Predict result
    prediction = model.predict(scaled_input)

    # Return prediction as dollar
    return {"Prediction" : np.exp(prediction[0]) * 0.012}




    