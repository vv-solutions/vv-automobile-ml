from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import bs4
import json
import argparse
import requests as req
import re
import pandas as pd
import json
import csv

def bilbasen_interaction(make, model):
    url = f'https://www.bilbasen.dk/brugt/bil/{make}/{model}?IncludeEngrosCVR=true&PriceFrom=0&includeLeasing=false&IncludeCallForPrice=false'
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    browser.get(url)
    
    links = []
    next_page = True;
    
    print('Getting links')
    while (next_page):
        anchor = None;
        next_page = False
        
            #Get all a tags
        browser.refresh()
        elmns = browser.find_elements(By.TAG_NAME,"a")
        for elm in elmns:
            try:
                #Find the a tags we need to get links
                if(elm.get_attribute("class") == "listing-heading darkLink"):
                    links.append(elm.get_attribute("href"))
                #Check for next page
                if(elm.get_attribute("class") =="next"):
                    anchor = elm
                    next_page = True
            except exceptions.StaleElementReferenceException:
                print("stale link")
        if (next_page):
            browser.get(anchor.get_attribute("href"))
    print('Done getting links')
    browser.close()
    return links

def get_details(urls):
    df = pd.DataFrame()
    print(f'Getting details for {len(urls)} cars')
    for url in urls:
        try:
            info_dict ={}
            html = req.get(url)
            soup = bs4.BeautifulSoup(html.text, 'html.parser')
            scripts = soup.select('script')
            script = scripts[-1].text
            json_string = script.replace("var _props = ","").replace(";","")
            json_object = json.loads(json_string)
            info_dict['price']=json_object['listing']['price']['displayValue']
            info_dict['model_year']=json_object['listing']['vehicle']['modelYear']
            info_dict['km']=json_object['tracking']['gtm']['dataLayer']['a']['attr']['vehicle_history_kilometers_driven']
            info_dict['reg']=json_object['tracking']['gtm']['dataLayer']['a']['attr']['vehicle_history_registration_date']
            info_dict['fuel_type'] = json_object['tracking']['gtm']['dataLayer']['a']['attr']['vehicle_model_fuel_type']
            info_dict['fuel_economy'] = json_object['tracking']['gtm']['dataLayer']['a']['attr']['vehicle_model_fuel_economy']
            info_dict['horse_power'] = json_object['tracking']['gtm']['dataLayer']['a']['attr']['vehicle_model_effect']
            info_dict['gear_type'] = json_object['tracking']['gtm']['dataLayer']['a']['attr']['vehicle_model_gear_type']
            new_row = pd.Series(data= info_dict)
            df = pd.concat([df,new_row.to_frame().T], ignore_index=True) 
        except Exception:
            print(f'Could not get data for car: {url}')
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape car information from Bilbasen by Make and Model of car')
    parser.add_argument('--make', help='Make of car', required=True)
    parser.add_argument('--model', help='Model of car', required=True)
    parser.add_argument('--path', help='path to output file', required=True)
    args = parser.parse_args()
    
    links = bilbasen_interaction(args.make,args.model)
    
    df = get_details(links)
    
    df.to_csv(f'{args.path}/{args.model}_data.csv', sep=';',index=False)
    print(f'File saved at {args.path}/{args.model}_data.csv')
    
    

