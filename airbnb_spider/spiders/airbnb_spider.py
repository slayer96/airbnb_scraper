import json
import logging

import scrapy
from lxml import html
from ..items import AirbnbSpiderItem, ReviewItem

QUERY = 'Budapest--Hungary'


class BnbSpider(scrapy.Spider):
    name = "bnbspider"
    allowed_domains = ["airbnb.com"]
    start_urls = (
        'https://www.airbnb.com/s/' + QUERY,
    )

    def parse(self, response):
        last_page_number = self.last_pagenumer_in_search(response)
        if last_page_number < 1:
            return
        else:
            page_urls = [response.url + "?page=" + str(pageNumber)
                         for pageNumber in range(1, last_page_number + 1)]
            for page_url in page_urls:
                yield scrapy.Request(page_url,
                                     callback=self.parse_listing_results_page)

    def parse_listing_results_page(self, response):
        for href in response.xpath('//a[@class="media-photo media-cover"]/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_content_listing)

    def parse_content_listing(self, response):
        item = AirbnbSpiderItem()

        json_array = response.xpath('//meta[@id="_bootstrap-room_options"]/@content').extract()
        amenities = []
        if json_array:
            airbnb_json_all = json.loads(json_array[0])
            airbnb_json = airbnb_json_all['airEventData']
            amenities = airbnb_json['amenities']
            item['response_time'] = airbnb_json['response_time_shown']
        item['availability'] = ''
        item['accuracy_rating'] = airbnb_json['accuracy_rating']
        item['air_conditioning'] = 5 in amenities
        item['accommodates'] = response.xpath('//strong[contains(@data-reactid,"Accommodates")]/text()').extract_first();
        item['beds'] = response.xpath('//strong[contains(@data-reactid,"Beds")]/text()').extract_first()
        item['bedrooms'] = response.xpath('//strong[contains(@data-reactid,"Bedrooms")]/text()').extract_first()
        item['breakfast'] = 16 in amenities
        item['buzzer_of_wireless_intercom'] = 28 in amenities
        item['cable_TV'] = 2 in amenities
        item['check_in_time'] = ''
        item['cleaning_free'] = response.xpath('//strong[contains(@data-reactid,"Cleaning")]/text()').extract_first()
        item['cancellation_type'] = response.xpath('//strong[contains(@data-reactid,"Cancellation")]/text()').extract_first()
        item['cleanliness_review'] = airbnb_json['cleanliness_rating']
        item['check_in_review'] = airbnb_json['cleanliness_rating']
        item['communication_review'] = airbnb_json['communication_rating']
        item['doorman'] = 14 in amenities
        item['dryer'] = 34 in amenities
        item['description'] = response.xpath('/html/head/meta[@property="og:description"]/@content').extract_first()
        item['essentials'] = 40 in amenities
        item['extra_people_charge'] = response.xpath('//strong[contains(@data-reactid,"Extra people")]/text()').extract_first()
        item['family_or_kid_friendly'] = 31 in amenities
        item['free_parking_on_premises'] = 9 in amenities
        item['gym'] = 15 in amenities
        item['hangers'] = 44 in amenities
        item['hair_dryer'] = 45 in amenities
        item['heating'] = 30 in amenities
        item['h24_check_in'] = 43 in amenities
        item['host_name'] = airbnb_json_all['hostFirstName']
        item['host_description'] = ''
        item['indoor_fireplace'] = 27 in amenities
        item['iron'] = 46 in amenities
        item['internet'] = 3 in amenities
        item['kitchen'] = 8 in amenities
        item['lift'] = 21 in amenities
        item['location_review'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:locality"]/@content').extract_first()
        item['laptop_friendly_workspace'] = 47 in amenities
        item['latitude'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:latitude"]/@content').extract_first()
        item['longtitude'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:longitude"]/@content').extract_first()
        item['monthly_discount'] = response.xpath('//strong[contains(@data-reactid,"Monthly Discount")]/text()').extract_first()
        item['name_of_district'] = ''
        item['property_type'] = response.xpath('//strong[contains(@data-reactid,"Property type")]/text()').extract_first()
        item['pets_allowed'] = 12 in amenities
        item['pool'] = 7 in amenities
        item['photo_urls'] = [url['thumbnail_url'] for url in airbnb_json_all['photoData']]
        item['private_entrance'] = 57 in amenities
        item['response_date'] = ''
        item['response_time'] = ''
        item['reviews'] = ''
        item['room_type'] = response.xpath('//strong[contains(@data-reactid,"Room type")]/text()').extract_first()
        item['spa'] = ''
        item['smoking_allowed'] = 11 in amenities
        item['suitable_for_events'] = 32 in amenities
        item['shampoo'] = 41 in amenities
        item['TV'] = 1 in amenities
        item['wireless_internet'] = 4 in amenities
        item['wheelchair_accessible'] = 6 in amenities
        item['washer'] = 33 in amenities
        item['weekly_discount'] = response.xpath('//strong[contains(@data-reactid,"Weekly Discount")]/text()').extract_first()
        item['url'] = response.url

        yield item

    def last_pagenumer_in_search(self, response):
        try:  # to get the last page number
            last_page_number = int(response
                                   .xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href')
                                   .extract()[0]
                                   .split('page=')[1]
                                   )
            return last_page_number

        except IndexError:  # if there is no page number
            # get the reason from the page
            reason = response.xpath('//p[@class="text-lead"]/text()').extract()
            # and if it contains the key words set last page equal to 0
            if reason and ('find any results that matched your criteria' in reason[0]):
                logging.log(logging.DEBUG, 'No results on page' + response.url)
                return 0
            else:
                # otherwise we can conclude that the page
                # has results but that there is only one page.
                return 1


Amenities = {
    '43' : '24_h',
    '5': 'air_conditioning'
}
