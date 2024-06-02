import pandas as pd
import pickle
import argparse

import warnings

def load_model(model_path):
    model = None
    with open(model_path, 'rb') as file:  
        model = pickle.load(file)
    return model

def get_prediction(model_path, car_dict):
    model = load_model(model_path)
    
    car_df = pd.DataFrame([car_dict])
    
    return model.predict(car_df)