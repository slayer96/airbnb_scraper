airbnb-budapest

Scrapy spider for Airbnb Budapest, Hungary

Instructions

    Install scrapy and json using pip, preferably on a virtualenv
    Edit the QUERY const on bnbspider.py for crawling a different location ('Contry--City' syntax, query filter parameters can also be used).
    Run scrapy crawl bnbspider -o output.csv
