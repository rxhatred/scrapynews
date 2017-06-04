# -*- coding: utf-8 -*-
import urllib
import scrapy

from scrapy import Spider, Request
from scrapy.selector import Selector, HtmlXPathSelector
from readability.readability import Document

from scrapynews.items import ScrapynewsItem

class NewsspiderSpider(scrapy.Spider):
    name = "scrapynews"
    allowed_domains = ["theguardian.com"]
    
    start_urls = [
        "https://www.theguardian.com/au",    
    ]
    
    def parse(self,response):
        news = Selector(response).css('.u-faux-block-link__overlay')
        
        for new in news:
            item = ScrapynewsItem()
            item['url'] = new.css('.u-faux-block-link__overlay::attr(href)').extract()[0]
            item['title'] = new.css('.u-faux-block-link__overlay::text').extract()[0]

            yield Request(url=item['url'], meta={'item': item}, callback=self.parse_item_page)
        
    
        """
        next_page = response.css(".pagination__action--static::attr(href)").extract_first()
        
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        #"""
    
    def parse_item_page(self, response):
        hxs = HtmlXPathSelector(response)

        item = response.meta['item']
        item['description'] = Document(response.text).summary()
        item['author'] = hxs.select('//*[@id="article"]/div[4]/div/div[1]/div[4]/p[1]/span/a/span/text()').extract()
        if not item['author']:
            item['author'] = 'N/A'
        return item

