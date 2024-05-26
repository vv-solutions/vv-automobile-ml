# Car Price Predictor

## Description:
This project detectes and reads numberplates, scrapes data from multiple sites (motorregister, findsynsrapport and bilbasen) to give an estimated price for the car, through linear regression and descision tree regressor


## How to run the project 
To run project, use: python3 price_predictor.py --image path (path = path to any of the images in the images folder, these have corresponding bilbasen data in the data folder) --km km (km = km-count of car, this is optional.)

more car data can be scraped with bilbasen.py, see --help for more information.

numberplate_detector.py can be used to get the text from the numberplate of a car, see --help for more information.

motorregister.py scrapes data from motorregisteret and findsynsrapport, see --help for more information.

## Status
The project works for Petrol, Diesel and electric cars, but not for hybrid cars. 


## Challenges:
There were several challenges in this project:
- cropping numberplates in images so easyOCR is able to read the text.
- Webscraping the data we need.
- Finding the best models to predict price. 


# Requirements:
- selenium
- webdriver-manager
- opencv-python
- easyOCR

## Installation:
- conda install -c conda-forge selenium -y
- conda install -c conda-forge webdriver-manager -y
- pip install opencv-python

## For X86 computers use:
- conda install -c conda-forge easyocr

## For ARM computers use:
- pip install easyocr
    
## Other requirements (These come pre packaged with anaconda):
- bs4
- json
- requests
- sklearn
- pandas
- csv
- numpy
