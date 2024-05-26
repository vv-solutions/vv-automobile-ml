import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn import linear_model
import argparse

def clean_data(data):
    
    df = data
    
    #Cleans price and first regestration
    non_word = re.compile(r'\D')
    df['price'] = df['price'].str.replace(r'\D','',regex=True)
    df['price'] = df['price'].astype('int64')
    df['reg'] = df['reg'].str.split('-').str[0]
    df['reg'] = df['reg'].astype('int64')
    
    electric_car = True
    
    #converts categorical variable into dummy/indicator variables if car is not electric
    if(df['fuel_type'][0] != 'El'):
        electric_car = False
        df = pd.get_dummies(df, columns = ['gear_type','fuel_type'])
    
    return df,electric_car

def get_prediction_score(target,pred_target):
    score_list = []
    for num1,num2 in zip(target,pred_target):
        if num1 > num2:
            score_list.append(num2/num1*100)
        elif num2 > num1:
            score_list.append(num1/num2*100)
        else:
            score_list.append(100)
    score = sum(score_list) / len(score_list)
    return score.round(2)
    
    
def linear_reg(df,electric_car):

    #Sets features and target
    feautre_list =[]
    
    X = ''
    if(electric_car == False):
        feautre_list= ['model_year','reg','km','fuel_economy','horse_power','gear_type_A','gear_type_M']
        if 'fuel_type_Benzin' in df.columns:
            feautre_list.append('fuel_type_Benzin')
        if 'fuel_type_Diesel' in df.columns:
            feautre_list.append('fuel_type_Diesel')
        
    else:
        feautre_list = ['model_year','reg','km','fuel_economy','horse_power']
        
    X= df[feautre_list]
    y = df['price']
    
    #split data and fit model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)

    #degree of linear correlation between data and target
    reg_score = regr.score(X,y)
    
    #how well the model predicted price of test cars
    y_pred = regr.predict(X_test)
    pred_score = get_prediction_score(y_test,y_pred)
    
    reg_dict={
        'model':regr,
        'reg_score': reg_score,
        'pred_score': pred_score
             }
    return reg_dict

def decision_tree_reg(df,electric_car):
    #Sets features and target
    feautre_list =[]
    
    X = ''
    if(electric_car == False):
        feautre_list= ['model_year','reg','km','fuel_economy','horse_power','gear_type_A','gear_type_M']
        if 'fuel_type_Benzin' in df.columns:
            feautre_list.append('fuel_type_Benzin')
        if 'fuel_type_Diesel' in df.columns:
            feautre_list.append('fuel_type_Diesel')
        
    else:
        feautre_list = ['model_year','reg','km','fuel_economy','horse_power']
        
    X= df[feautre_list]
    y = df['price']
    
    #split data and fit model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    dtr = DecisionTreeRegressor()
    dtr.fit(X_train, y_train)
    
    #model score
    model_score = dtr.score(X_test, y_test)
    
    #how well the model predicted price of test cars
    y_pred = dtr.predict(X_test)
    pred_score = get_prediction_score(y_test,y_pred)
    
    dtr_dict={
        'model':dtr,
        'model_score': model_score,
        'pred_score': pred_score
             }
    return dtr_dict



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test predictions of linear regression model and DescionTreeRegressor')
    parser.add_argument('--file', help='path to input data file', required=True)
    args = parser.parse_args()
    
    data = pd.read_csv(args.file,sep=';')
    
    df,electric_car = clean_data(data)
    
    lr = linear_reg(df,electric_car)
    
    dtr = decision_tree_reg(df,electric_car)
    
    
    print('--- Linear model ---')
    print(f'Regression score {lr["reg_score"]}')
    print(f'Prediction score {lr["pred_score"]}')
    print('')
    print('--- DecisionTreeRegressor ---')
    print(f'Model score {dtr["model_score"]}')
    print(f'Prediction score {dtr["pred_score"]}')
    
    