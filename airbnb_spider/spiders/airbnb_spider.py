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

        #json_array = response.xpath('//meta[@id="_bootstrap-room_options"]/@content').extract()
        #logging.info(json_array)
        # if json_array:
        #    airbnb_json_all = json.loads(json_array[0])
        #    airbnb_json = airbnb_json_all['airEventData']
        #    item['value_review'] = airbnb_json['visible_review_count']
        #    item['room_type'] = airbnb_json['room_type']
        #    item['response_time'] = airbnb_json['response_time_shown']
        item['availability'] = ''
        item
        item['accommodates'] = response.xpath('//strong[contains(@data-reactid,"Accommodates")]/text()').extract_first();
        item['beds'] = response.xpath('//strong[contains(@data-reactid,"Beds")]/text()').extract_first()
        item['bedrooms'] = response.xpath('//strong[contains(@data-reactid,"Bedrooms")]/text()').extract_first()
        item['cancellation_type'] = response.xpath('//strong[contains(@data-reactid,"Cancellation")]/text()').extract_first()
        item['cleaning_free'] = response.xpath('//strong[contains(@data-reactid,"Cleaning")]/text()').extract_first()
        item['extra_people_charge'] = response.xpath('//strong[contains(@data-reactid,"Extra people")]/text()').extract_first()
        item['latitude'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:latitude"]/@content').extract_first()
        item['longtitude'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:longitude"]/@content').extract_first()
        item['monthly_discount'] = response.xpath('//strong[contains(@data-reactid,"Monthly Discount")]/text()').extract_first()
        item['property_type'] = response.xpath('//strong[contains(@data-reactid,"Property type")]/text()').extract_first()
        item['room_type'] = response.xpath('//strong[contains(@data-reactid,"Room type")]/text()').extract_first()
        item['smoking_allowed'] = response.xpath('//span[contains(@data-reactid,"smoking")]/text()').extract_first()
        item['suitable_for_events'] = response.xpath('//span[contains(@data-reactid,"event")]/text()').extract_first()
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
