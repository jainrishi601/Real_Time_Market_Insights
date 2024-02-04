

![Screenshot 2024-02-04 211829](https://github.com/jainrishi601/Real_Time_Market_Insights/assets/128663753/081e36bb-0205-4794-9a7a-f9751352eab8)


## Methodology
The aim of this project is to build an application which outputs accurate 
recommendations in a quantifiable manner. For this purpose, 3 modules are 
implemented which are as follows:
- Machine Learning module
- Sentiment Analysis module
- Fuzzy logic Module

## Machine learning Module 
The purpose of this module is to output Stock Prediction value. Stock Prediction 
value is the strength of difference in opening price and closing price. For this we need 
to predict the closing price of the stock. This is achieved by applying Machine 
Learning on Historical data of the stock.

![Screenshot 2024-02-04 213451](https://github.com/jainrishi601/Real_Time_Market_Insights/assets/128663753/fac93b60-4dd1-43a7-b7b2-afdfa0908aad)

## Sentiment Analysis Module 
The purpose of this module is to obtain the sentiment value of latest news headlines 
regarding each stock and output its average as sentiment value to fuzzy module.
The steps used in this module are as follows:
1. **Data Collection**:
The data is collected by crawling through Indian Financial news websites. Minimum 4 news Headlines are scraped for each stock and stored against the company Symbol.
2. **Tokenizing**:
Each news headline is broken down into sentences and then in turn broken down into words.
3. **Lemmatizing**:
It is the process of reducing inflected (or sometimes derived) words to 
their word stem, base or root form. For example, “the boy's cars are 
different colours” reduces to “the boy car be differ colour”
4. Finding Most Informative Features:
Words that contribute most in adding polarity to a sentence are found.


## Fuzzy logic Module
The purpose of this module is to output Stock Faith which is the strength of 
Recommendation. 
The activation rules for this module are:
- IF the News Sentiment was good or the Stock Prediction value was good, 
THEN the Stock faith will be high.
- IF the Stock Prediction value was average, THEN the Stock faith will be 
medium and completely based on weights assigned.
- IF the News Sentiment was poor and the Stock Prediction value was poor 
THEN the Stock faith will be low.





