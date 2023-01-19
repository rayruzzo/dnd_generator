import scrapy


class Elf(scrapy.Spider):
    name = 'elf'
    allowed_domains = ['dungeons.fandom.com']
    start_urls = ['https://dungeons.fandom.com/wiki/SRD:Elves,_High_(Race)']

    def parse(self, response):
        return {'modifiers': response.xpath('//pre/text()').get()}
