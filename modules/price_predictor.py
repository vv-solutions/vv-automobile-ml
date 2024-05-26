import prediction as pred
from moterregister import motor_register_interaction
from numberplate_detector import detect_numberplate
import pandas as pd
import argparse


def get_one_hot_values(df, cols, electric_car):    
    if(electric_car == False):
        #matches one hot encoded values in bilbasen df
        if 'gear_type_A' in cols and 'gear_type_M' in cols:
            if df.at[0,'gear_type'] == 'A':
                df.at[0,'gear_type_A'] = 1
                df.at[0,'gear_type_M'] = 0
            else:
                df.at[0,'gear_type_A'] = 0
                df.at[0,'gear_type_M'] = 1
        else:
            df.at[0,f'gear_type_{car_dict["gear_type"]}'] = 1
            
        if 'fuel_type_Benzin' in cols and 'fuel_type_Diesel' in cols:
            if df.at[0,'fuel_type'] == 'Benzin':
                df.at[0,'fuel_type_Benzin'] = 1
                df.at[0,'fuel_type_Diesel'] = 0
            else:
                df.at[0,'fuel_type_Benzin'] = 0
                df.at[0,'fuel_type_Diesel'] = 1
        else:
            df.at[0,f'fuel_type_{car_dict["fuel_type"]}'] = 1
            
    del df["gear_type"]
    del df["fuel_type"]
    del df['brand']
    del df['model']
    
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get a predicted price for your car')
    parser.add_argument('--image', help='path to image of car', required=True)
    parser.add_argument('--km', type=int,help='KM count of input car, optional', required=False)

    
    args = parser.parse_args()
    
    numerplate = detect_numberplate(args.image)
    
    car_dict = motor_register_interaction(numerplate)
    
    df_detected = pd.DataFrame(car_dict, index=[0])
    
    df_bilbasen,electric_car = pred.clean_data(pd.read_csv(f'../data/{car_dict["model"]}_data.csv',sep=';'))
    #df_bilbasen,electric_car = pd.read_csv(f'../data/{car_dict["model"]}_data.csv',sep=';')
    
    df_detected = get_one_hot_values(df_detected,df_bilbasen.columns,electric_car)
    
    if(args.km):
        df_detected['km'] = args.km
         
    lr = pred.linear_reg(df_bilbasen,electric_car)
    
    dtr = pred.decision_tree_reg(df_bilbasen,electric_car)
    
    linear_reg_pred = lr['model'].predict(df_detected[0:1])[0].round(2)
    
    dtr_pred = dtr['model'].predict(df_detected[0:1])[0].round(2)
    
    print('------LR-------')
    print(f'Predicted price: {linear_reg_pred}kr')
    print(f'Prediction score: {lr["pred_score"]}%')
    print('------DTR------')
    print(f'Predicted price: {dtr_pred}kr')
    print(f'Prediction score: {dtr["pred_score"]}%')
    