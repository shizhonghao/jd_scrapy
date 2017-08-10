import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://item.jd.com/4835534.html'
    ]

    def parse_buyer(self,response):
        print("buyer",response.extract())
        return "???"
        pass

    def parse_seller(self,response):
        print("seller:",response)
        pass

    def parse(self, response):
        # get item id
        item_id = int(re.findall('\d+',response.url)[0])
        print("item-id:",item_id,type(item_id))

        # buyer's answer
        page_number = 1
        question_url_b = "https://question.jd.com/question/getQuestionAnswerList.action?page=%d&productId=%d" % (page_number,item_id)
        req = scrapy.Request(question_url_b,callback=self.parse_buyer)
        print("req:",req.body())
        print("here")

        # seller's answer
        page_number = 1
        question_url_s = "https://club.jd.com/clubservice/newconsulation-%d-%d.html" % (page_number,item_id)
        yield{
            'item_id':item_id,
            'url1':question_url_b,
            'url2':question_url_s,
        }

        """
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            
        """

