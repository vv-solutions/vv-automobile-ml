# vv-automobile-machine-learning

## How to run the project 

### Requirements:
Make sure the requirements are installed:
easyocr==1.7.1
imutils==0.5.4
langchain==0.2.3
langchain_community==0.2.4
langchain_weaviate==0.0.2
numpy==1.26.4
opencv_python==4.9.0.80
opencv_python_headless==4.9.0.80
pandas==1.4.4
selenium==4.21.0
weaviate_client==4.6.3
webdriver_manager==4.0.1

### vv-price-predictor-2.0
To run project, use: python main.py --image (takes path to an image, this works only in some cases, you can instead use --numberplate to skip the detection part.) --km km (km = km-count of car, this is optional, as the project will go to findsynsrapport.dk, and find the km-count at last inspection, this count might be outdated, depending on when the last inspection was)

numberplate_detector.py can be used to get the text from the numberplate of a car, see --help for more information.

**Note**: The project works for Petrol, Diesel and electric cars, but not for hybrid cars. 


Notebooks for this part: 
- prediction/prediction.ipynb (contains training and testing of supervised models for price prediction)
- web/motorregisterPOC.ipynb (contains web scraping from motorregister and findsynsrapport)
- NumberplateRecognition/detectNumberplate.ipynb (contains detection of numberplate as well as image to text with easyOCR)


### vv-chat-1.0
To run this project, use python chat.py --question

**Note**: This project requires a Weaviate database with database with the correct index in it, this can be created by running the data ingestion part of llm/llm.ipynb (This might take some time for slower computers. )

Notebooks for this part:
llm/llm.ipynb (contains data ingestion and testing of different chat models)


# Problem statement:
Customers want quick service and fast responses. Running a chat function where customers can get the help they need, or an estimation service where customers can get an estimated valuation of their car, would be very time consuming and also very expensive for vv-automobile if run by humans, we must therefore implement machine learning models for these tasks. 


# Motivation
Calculating the worth of a car is a non-trivial task, for people who do not work with selling cars daily. The price of a used car depends on many factors, this project aims to simplify figuring out how much a car is worth through the use of machine learning models. 

Furthermore, our webshop sells just under 4000 products, it can be difficult to figure out which products might be the right ones for the job, therefore this project aims to help customers get answers to product related questions and general car questions. 

# Theoretical foundation
This project looks at two different areas of machine-learning, being Natural Language Processing, and Supervised machine learning:
- Data exploration and cleaning: Used to visualize and describe the data in our dataset. Removing or interpolating missing values. 
- Feature engineering: Used in this project to transform categorical columns into numerical columns, such as make and model.
- Hyper parameter tuning: Selecting the best hyper parameters for the models. In the project we used both GridSearchCV and RandomizedSearchCV.
- Cross-Validation: Used to split our data into multiple folds which the model is tested on. 
- Text Embedding: Converting text to vectors making it possible to find similarity between words.
- Retrieval-Augmented Generation: Used to enhance our model, by fetching data from our vector database.



# Argumentation of choices
In this project we have tested multiple models both for predicting car prices as well as our chat bot. 

### Prediction:
For the prediction part we chose to test Linear regression, Decision tree regressor, and Random forest Regressor. The reason we have chosen these models is that they range from lightweight to heavy, giving us the opportunity to choose a model based on performance and result. 

The final model we chose to implement in our project was Random forest regressor. Although this was the worst model in terms of speed, we found that this model gave us far better results than the others.

### Chat
For the chat part of the project we chose to test: llama3, mistral, and qwen. When choosing models we went for models that are popular, and again ranging from light to heavy. It is hard to quantify the result of these models, so our final choice was llama3 based on the fact that we found the answers it gave the best. In terms of speed, mistral and llama3 were similar and qwen was much faster, but with almost unusable responses. 


# Design, Code and Artifacts
The project includes the following components:

### Web scraping 
We use web scraping for different purposes in our project, the first purpose was to gather all the cars that we wanted from Bilbasen.dk, so we could make a dataset with cars containing features that we need. This can be seen in web/webscrapingAndDataGeneration.ipynb 

The next purpose of our usage of web scraping is for running our application, when we run the program and type in the number plate it goes to https://motorregister.skat.dk/ and collect informations about the car, afterward it tries to go to https://findsynsrapport.fstyr.dk/ to gather how many kilometers the car have driven this can be seen in web/motorregisterPOC.ipynb  

### Data Exploration, Data cleaning and Prediction
We have identified different columns in our dataset that needed cleaning, to ensure that all the columns are the same data type and we get rid of missing data and removal of outliers.
Lastly we trained and tested several regression models. 
this can be seen in prediction/prediction.ipynb

### NLP/LLM
We have stored different documents regarding general car maintenance, our product and car dataset as vector embeddings in our vector database (Weaviate) which we use as retriever for testing different models this can be seen in llm/llm.ipynb


# Outcomes
### Prediction:
As mentioned earlier, we ended up choosing Random Forest Regressor as our model. Once trained the model gave an r2_score of 93,91% which was quite good, but when we ran cross validation on our model, we ended with a score of 80,60%, this points to the fact that the model might be overfitted. But when giving it less training data, we did not see an improvement. 

### Chat:
It is hard to quantify the result of chatbot, and we chose llama3 based on our opinion of which model gave the best response. While it still might give less good answers at times, it actually gives very good and usable answers most of the time. Through the used of mmr in our vector database the model is both able to recommend products which are sold in our shop, as well as answer questions about general repair. 











