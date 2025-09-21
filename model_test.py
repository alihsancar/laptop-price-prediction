import pandas as pd
import numpy as np
import pickle

with open('model_encoder_scaler.pkl', 'rb') as f:
    model_file = pickle.load(f)

model = model_file['model']
encoder = model_file['encoder']
scaler = model_file['scaler']
test_data = pd.read_csv('testdata.csv')
print(model.predict(test_data))
