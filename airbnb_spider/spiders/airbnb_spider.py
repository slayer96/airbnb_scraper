import re
import json
import logging

import scrapy
from ..items import AirbnbSpiderItem

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

        room_array = response.xpath('//meta[@id="_bootstrap-room_options"]/@content').extract()
        amenities = []
        if room_array:
            room_options_all = json.loads(room_array[0])
            room_options = room_options_all['airEventData']
            amenities = room_options['amenities']
            item['accuracy_rating'] = room_options['accuracy_rating']
            item['check_in_review'] = room_options['cleanliness_rating']
            item['communication_review'] = room_options['communication_rating']
            item['cleanliness_review'] = room_options['cleanliness_rating']
            item['host_name'] = room_options_all['hostFirstName']
            item['photo_urls'] = [url['thumbnail_url'] for url in room_options_all['photoData']]
            item['response_time'] = room_options['response_time_shown']

        listing_array = response.xpath('//meta[@id="_bootstrap-listing"]/@content').extract()
        if listing_array:
            listing_json_all = json.loads(listing_array[0])
            listing_json = listing_json_all['listing']
            listing_description = listing_json['localized_sectioned_description']
            item['availability'] = re.sub('<[^>]*>', '', listing_json['localized_minimum_nights_description'])
            item['reviews_text'] = '\n\n'.join([r['comments'] for r in listing_json['sorted_reviews']])
            item['reference'] = listing_json['user']['profile_path']
            if listing_description:
                item['description'] = listing_description['description']
                item['house_rules'] = listing_description['house_rules']
                item['review_summary'] = listing_description['summary']
            else:
                item['description'] = listing_json.get('localized_description', listing_json['description'])
                item['house_rules'] = ''
                item['review_summary'] = listing_json['summary']
        neigborhood_card_array = response.xpath('//meta[@id="_bootstrap-neighborhood_card"]/@content').extract()
        if neigborhood_card_array:
            neigborhood_card = json.loads(neigborhood_card_array[0])
            item['name_of_district'] = neigborhood_card['neighborhood_localized_name']
        else:
            item['name_of_district'] = ''

        item['air_conditioning'] = 5 in amenities
        item['accommodates'] = response.xpath('//strong[contains(@data-reactid,"Accommodates")]/text()').extract_first()
        item['beds'] = response.xpath('//strong[contains(@data-reactid,"Beds")]/text()').extract_first()
        item['bathrooms'] = response.xpath('//strong[contains(@data-reactid,"Bathrooms")]/text()').extract_first()
        item['breakfast'] = 16 in amenities
        item['buzzer_of_wireless_intercom'] = 28 in amenities
        item['cable_TV'] = 2 in amenities
        item['check_in_time'] = response.xpath('//strong[contains(@data-reactid,"Check In")]/text()').extract_first()
        item['cleaning_fee'] = response.xpath('//strong[contains(@data-reactid,"Cleaning")]/text()').extract_first()
        item['cancellation_type'] = response.xpath('//strong[contains(@data-reactid,"Cancellation")]/text()').extract_first()
        item['doorman'] = 14 in amenities
        item['dryer'] = 34 in amenities
        item['essentials'] = 40 in amenities
        item['extra_people_charge'] = response.xpath('//strong[contains(@data-reactid,"Extra people")]/text()').extract_first()
        item['family_or_kid_friendly'] = 31 in amenities
        item['free_parking_on_premises'] = 9 in amenities
        item['gym'] = 15 in amenities
        item['hangers'] = 44 in amenities
        item['hair_dryer'] = 45 in amenities
        item['heating'] = 30 in amenities
        item['h24_check_in'] = 43 in amenities

        description = response.xpath('//div[@class="expandable-content expandable-content-long"]/div/p').extract()
        item['host_description'] = [''.join(re.sub('<[^>]*>', '', i)) for i in description]
        item['indoor_fireplace'] = 27 in amenities
        item['iron'] = 46 in amenities
        item['internet'] = 3 in amenities
        item['kitchen'] = 8 in amenities
        item['lift'] = 21 in amenities
        item['location_review'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:locality"]/@content').extract_first()
        item['laptop_friendly_workspace'] = 47 in amenities
        item['latitude'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:latitude"]/@content').extract_first()
        item['longitude'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:longitude"]/@content').extract_first()
        item['monthly_discount'] = response.xpath('//strong[contains(@data-reactid,"Monthly Discount")]/text()').extract_first()

        item['property_type'] = response.xpath('//strong[contains(@data-reactid,"Property type")]/text()').extract_first()
        item['pets_allowed'] = 12 in amenities
        item['pool'] = 7 in amenities
        item['private_entrance'] = 57 in amenities
        item['response_rate'] = response.xpath('//span[text()="Response rate:"]/following-sibling::strong/text()').extract_first()
        item['response_time'] = response.xpath('//span[text()="Response time:"]/following-sibling::strong/text()').extract_first()
        item['host_reviews'] = response.xpath('//span[contains(@data-reactid,"Reviews")]/text()').extract_first()
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

