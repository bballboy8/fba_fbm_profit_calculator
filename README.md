FBM / FBA Profit Calculator
========================

FBM / FBA Profit Calculator is a used to fetch the product details from www.kroger.com, www.amazon.com and www.keepa.com for calculating the FBM / FBA profits

### Technologies

Developed using following features:

- Python 3
- Scrapy
- bs4
- formulas
- keepa
- pandas

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

A step by step series of examples that tell you how to install the FBM / FBA Profit Calculator

**Install the python packages**

```bash
pip install bs4
pip install Scrapy
pip install formulas
pip install keepa
pip install pandas
```

**Run Module**

*For saving the products which are having profits for FBM/FBA as csv*

*STEP 1*

*Signup for scrapper api free trial with 10,000 requests: https://app.scrapingant.com/signup and add API key in kroger/spiders/amazon.py* 

*STEP 2*
```bash
python run.py
```

**Run scrapper modules from terminal ( optional )**

*For saving kroger scrapped data as csv*
```bash
cd kroger
scrapy crawl kroger -o output/kroger.csv -t csv

```
*For saving amazon scrapped data as csv*
```bash
cd kroger
scrapy crawl amazon -o output/amazon.csv -t csv

```

## Authors

* **Vishnu Prasad** 
