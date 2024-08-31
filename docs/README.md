# Depok City House Price Prediction

## Introduction

A house is one of the basic needs that serves as a place to live, a place to do an activity, and a shelter, which provides a sense of security and comfort. For this reason, a house is considered one of the most important assets for everyone. In addition, a house is a profitable investment because it is one of the assets that experience price increases every year.

Population growth that continues to increase every year results in the need for houses that continue to increase. Everyone wants a nice and comfortable house at an affordable price. The difficulty of finding an ideal house at an affordable price is a problem for some people. Based on these problems, a project is carried out in which a model will be built that can predict house prices in the city of Depok, West Java, by considering the characteristics of the house.

## Goals

This project aims to build a model that will be able to predict house prices in Depok City based on the characteristics and facilities of each house. Also, this project can provide insight into the following:

- Features/factors that have the most influence on house prices.
- Areas in Depok City that have the most expensive house prices.

## Web Scraping

The data was obtained through web scraping the website www.lamudi.co.id in ~~January 2023~~ March 2024 using the selenium library. The scraped data consists of 8113 houses in Depok City, from each house data, the following features are obtained:

- categories
- subcategories
- bedroom
- bathroom
- building size
- land size
- number of floors
- furnished
- geo point
- parent url
- page url
- security facility
- pool facility
- yard facility
- balcony facility
- ac unit facility

## Data Preprocessing

After scraping, the data needs to be cleaned so that it can be analyzed and predicted, namely:

- Merge house price dataset wih other house facility dataset
- Convert data types
  - integer: 'bedrooms', 'bathrooms', 'num_floors', 'price'
  - float: 'building_size', 'land_size'
- Parse "subcategories" columns and pick only second element of list
  - example:
    ["house","single-family-house"] to "single-family-house"
- Parse "parent_url" column to get house location
  - example:
    https://www.lamudi.co.id/west-java/depok/cimanggis/house/buy/ to "cimanggis"
- Calculate and fix num_floors by either from url or result of division of "building_size" and "land_size"
- Map "furnished" values to either yes, no, or semi
- Preprocessed facility columns so the value is yes or no
- Address the issue of skewed features using log transformation for "building_size", "land_size", "price"
- Apply one-hot encoding to "subcategories", "furnished", "location"
- Fix some inconsistencies of some values by referring to house description

## Data Analysis

Based on the analysis results:

- Cinere is the area with the most expensive average house price in Depok City, followed by Limo and Beji.

  ![alt text](https://github.com/anggapark/Depok-houseprice-prediction/blob/main/asset/avg_houseprice_loc.png?raw=true)

- Land area has a fairly high correlation with house prices, followed by building area
- Bedroom has a high correlation with bathroom

  ![alt text](https://github.com/anggapark/Depok-houseprice-prediction/blob/main/asset/corr.png?raw=true)

- Most houses do not have any or all of the additional features

  ![alt text](https://github.com/anggapark/Depok-houseprice-prediction/blob/main/asset/facility.png?raw=true)

## Modelling

- In the data preprocessing stage:

  - Features with yes and no values are label encoded into yes: 1 and no: 0.
  - Categorical features with many classes such as location are applied One Hot Encoding.
  - Features with skew distribution are transformed using log transformation.

- In the modeling stage, the algorithms used are:

  - Linear Regression,
  - Ridge Regression,
  - Lasso Regression,
  - RANSAC Regression, dan
  - Random Forest Regression

- The metrics used as model evaluation are Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE).

## Evaluation

| Model                    | RMSE     | MAE      |
| ------------------------ | -------- | -------- |
| Linear Regression        | 0.288594 | 0.209811 |
| Ridge Regression         | 0.288735 | 0.209920 |
| Lasso Regression         | 0.610469 | 0.451481 |
| RANSAC Regression        | 0.318648 | 0.227697 |
| Random forest Regression | 0.254087 | 0.174959 |

It can be seen, the model with the best RMSE and MAE values is Random Forest Regression with an RMSE value of 0.254087 and MAE 0.174959.

After that, parameter tuning is performed on the Random Forest Regression model to find better results using GridSearchCV.

Hasil dari tuning adalah:

|                | RMSE     | MAE      |
| -------------- | -------- | -------- |
| Sebelum Tuning | 0.254087 | 0.174959 |
| Setelah Tuning | 0.253440 | 0.174139 |

## Future Plan

- [x] Perform parameter tuning on the model to find better RMSE and MAE values.
- [x] Deploy machine learning model with flask or streamlit.
