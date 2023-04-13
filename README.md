# Machin-Learning-for-Cars-Price
Machin Learning for Cars Price using Selenium web scraping and Decision Tree method.

First, by using the Selenium library, the desired car data is extracted from the website Divar.ir (Iranian second-hand vehicles). To change the car model, uncomment the input section and comment the default name. It takes a while to scrape enough data.

Then the data is cleaned using regex and organized into a data frame.

Correlation of the data is displayed by linear regression using Seaborn library.

Finally, the data predicts the price of the car by using machine learning in the decision tree method by entering the model and Km-age.
