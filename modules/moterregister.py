from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import argparse

def motor_register_interaction(numberplate):
    # Base url:
    url = 'https://motorregister.skat.dk/dmr-kerne/koeretoejdetaljer/visKoeretoej?execution=e2s1'
    options = Options()
    options.add_argument("--headless")
    

    service = Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(service=service, options=options)
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
        kw= browser.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[2]/span[1]').text

        #Gets KM from findsynsrapport if there is no report, set km to 0
        try:
            browser.get("https://findsynsrapport.fstyr.dk/Sider/resultater.aspx?Reg="+numberplate)
            browser.implicitly_wait(2)
            table_inspect = browser.find_element(By.ID, 'tblInspections')
            km = table_inspect.find_elements(By.TAG_NAME, 'tr')[1].find_elements(By.TAG_NAME, 'td')[2].text.replace('.', '')
        except:
            km = 0
            
        car_dict = cleanupData(brand,model,year,first_reg_year,gear_type,km,fuel_type,kw)
        return car_dict
    
    except exceptions.NoSuchElementException:
        print("Could not fetch the element")
    
    finally: 
        browser.close()

def cleanupData(brand, model, year, first_reg_year, gear_type, km,fuel_type, kw):
    brand_dict = {"MERCEDES-BENZ": "MERCEDES",
                  "VOLKSWAGEN": "VW"}

    if brand in brand_dict:
        brand = brand_dict[brand]
        

    gear_type = gear_type.replace('Nej', 'M').replace('Ja', 'A')
    

    if(fuel_type == "El"):
        gear_type ="A"
    
    model = model.lstrip().replace(' ', '_')
    horse_power = round(float(kw) * 1.35962)
    first_reg_year = first_reg_year.split('-')[2]
    if year == "-":
        year=first_reg_year
        
    car_dict_cleaned = {'Make': brand.lower(),
                        'Model': model.lower(),
                        'ModelYear': year,
                        'Reg': first_reg_year,
                        'GearType': gear_type,
                        'Kilometers': km,
                        'FuelType': fuel_type,
                        'HorsePower': horse_power}
    return car_dict_cleaned
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from Motor register')
    parser.add_argument('--numberplate', help='Insert the numberplate you want to fetch', required=True)
    args = parser.parse_args()
    car_info = motor_register_interaction(args.numberplate)
    print(car_info)
