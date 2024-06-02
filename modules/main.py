import predictor
from moterregister import motor_register_interaction
from numberplate_detector import detect_numberplate
import pandas as pd
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get a predicted price for your car')
    parser.add_argument('--image', help='path to image of car', required=False)
    parser.add_argument('--numberplate', help='path to image of car', required=False)
    parser.add_argument('--km', type=int,help='KM count of input car, optional', required=False)
    
    
    args = parser.parse_args()

    numberplate = "";
    
    if args.numberplate:
        numberplate = args.numberplate
    else:
        numberplate = detect_numberplate(args.image)

    car_dict = motor_register_interaction(numberplate)
    
    
    if(args.km):
        car_dict['Kilometers'] = args.km
        
    predicted_price = predictor.get_prediction("../prediction/models/rf_pipeline_price_outliers_removed.pkl", car_dict)
         
    print(predicted_price[0])