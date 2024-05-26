from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import argparse
from selenium.common import exceptions


def motor_register_interaction(numberplate):
    # Base url:
    url = 'https://motorregister.skat.dk/dmr-kerne/koeretoejdetaljer/visKoeretoej?execution=e2s1'
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    browser.get(url)
    try:
        #Finds search input field
        search_field = browser.find_element(By.ID, 'soegeord')

        #Set the value of the search input field to numberplate
        search_field.send_keys(numberplate)

        #Finds search button and clicks
        buttonSearch = browser.find_element(By.ID,'fremsoegKtBtn')
        buttonSearch.click()

        brand_model_variant = browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/div[2]/span[2]').text
        brand=brand_model_variant.split(',')[0] 
        model=brand_model_variant.split(',')[1] 

        year= browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[4]/div/div[1]/div[4]/div[2]/span').text
        first_reg_year= browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/span[2]').text
        gear_type = browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[12]/div/div[1]/div[1]/div[2]/span').text

        tech_data_button = browser.find_element(By.XPATH, '//*[@id="center"]/div[2]/div[3]/div/div[1]/ul/li[2]/div/a')
        tech_url = tech_data_button.get_attribute("href")
        browser.get(tech_url)
        browser.implicitly_wait(2)

        fuel_type= browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/span').text
        fuel_economy= browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[4]/div/div[1]/div[3]/div[2]/span[1]').text
        kw= browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/span[1]').text

        #Gets KM from findsynsrapport
        browser.get("https://findsynsrapport.fstyr.dk/Sider/resultater.aspx?Reg="+numberplate)
        browser.implicitly_wait(2)
        table_inspect = browser.find_element(By.ID, 'tblInspections')
        km = table_inspect.find_elements(By.TAG_NAME, 'tr')[1].find_elements(By.TAG_NAME, 'td')[2].text.replace('.', '')
        car_dict = cleanupData(brand,model,year,first_reg_year,gear_type,km,fuel_type,fuel_economy,kw)
        return car_dict
    
    except exceptions.NoSuchElementException:
        print("Could not fetch the element")
    
    finally: 
        browser.close()

def cleanupData(brand, model, year, first_reg_year, gear_type, km,fuel_type, fuel_economy, kw):
    brand_dict = {"MERCEDES-BENZ": "MERCEDES",
                  "VOLKSWAGEN": "VW"}

    if brand in brand_dict:
        brand = brand_dict[brand]

    gear_type = gear_type.replace('Nej', 'M').replace('Ja', 'A')
    model = model.lstrip().replace(' ', '_')
    horse_power = round(float(kw) * 1.35962)
    first_reg_year = first_reg_year.split('-')[2]
    fuel_economy = fuel_economy.replace(',','.')
    if year == "-":
        year=first_reg_year
        
    car_dict_cleaned = {'brand': brand,
                        'model': model,
                        'model_year': year,
                        'reg': first_reg_year,
                        'gear_type': gear_type,
                        'km': km,
                        'fuel_type': fuel_type,
                        'fuel_economy': fuel_economy,
                        'horse_power': horse_power}
    return car_dict_cleaned
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from Motor register')
    parser.add_argument('--numberplate', help='Insert the numberplate you want to fetch', required=True)
    args = parser.parse_args()
    car_info = motor_register_interaction(args.numberplate)
    print(car_info)
