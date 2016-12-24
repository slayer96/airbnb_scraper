# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AirbnbSpiderItem(scrapy.Item):
    availability = scrapy.Field()   #g
    accuracy_rating = scrapy.Field()  #
    accommodates = scrapy.Field()  #
    air_conditioning = scrapy.Field()  #
    bathrooms = scrapy.Field()  #
    beds = scrapy.Field()  #
    breakfast = scrapy.Field()  #
    buzzer_of_wireless_intercom = scrapy.Field()  #
    cable_TV = scrapy.Field()  #
    check_in_time = scrapy.Field()
    cleaning_fee = scrapy.Field()  #
    cancellation_type = scrapy.Field()  #
    communication_review = scrapy.Field()  #
    cleanliness_review = scrapy.Field()  #
    check_in_review = scrapy.Field()  #
    doorman = scrapy.Field()  #
    dryer = scrapy.Field()  #
    description = scrapy.Field()  #
    essentials = scrapy.Field()   #
    extra_people_charge = scrapy.Field()  #
    family_or_kid_friendly = scrapy.Field()  #
    free_parking_on_premises = scrapy.Field()  #
    gym = scrapy.Field()  #
    hangers = scrapy.Field()  #
    hair_dryer = scrapy.Field()  #
    heating = scrapy.Field()  #
    house_rules = scrapy.Field()
    h24_check_in = scrapy.Field()  #
    host_name = scrapy.Field()  #
    host_description = scrapy.Field()
    host_reviews = scrapy.Field()
    indoor_fireplace = scrapy.Field()  #
    iron = scrapy.Field()  #
    internet = scrapy.Field()  #
    kitchen = scrapy.Field()  #
    lift = scrapy.Field()  #
    location_review = scrapy.Field()  #
    laptop_friendly_workspace = scrapy.Field()  #

    latitude = scrapy.Field()  #
    longitude = scrapy.Field()  #

    monthly_discount = scrapy.Field()  #
    name_of_district = scrapy.Field()
    property_type = scrapy.Field()  #
    pets_allowed = scrapy.Field()  #
    pool = scrapy.Field()  #
    photo_urls = scrapy.Field()   #
    private_entrance = scrapy.Field()  #

    reviews_text = scrapy.Field()
    response_rate = scrapy.Field()
    response_time = scrapy.Field()
    reference = scrapy.Field()
    reviews = scrapy.Field()
    review_summary = scrapy.Field()
    room_type = scrapy.Field()  #
    spa = scrapy.Field()
    smoking_allowed = scrapy.Field()  #
    suitable_for_events = scrapy.Field()  #
    shampoo = scrapy.Field()  #
    TV = scrapy.Field()  #
    wireless_internet = scrapy.Field()  #
    wheelchair_accessible = scrapy.Field()  #
    washer = scrapy.Field()  #
    weekly_discount = scrapy.Field()  #
    value_review = scrapy.Field()  #
    url = scrapy.Field()  #




