import scrapy
import re
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://item.jd.com/4835534.html'
    ]

    def parse_buyer(self,response):
        print("buyer:",response)
        # question list of buyer-answers
        res = json.loads(response.body)
        # "ensure_ascii=False" ensure the proper presentation of Chinese characters
        # show what's in the json received
        #print(json.dumps(res,indent=4,ensure_ascii=False))
        pass

    def parse_seller(self,response):
        print("seller:",response)
        print(response.body)
        res = json.loads(response.body.decode("gbk"))
        print(json.dumps(res, indent=4, ensure_ascii=False))
        pass

    def parse(self, response):
        # get item id
        item_id = int(re.findall('\d+',response.url)[0])
        print("item-id:",item_id,type(item_id))

        # buyer's answer
        page_number = 1
        # should be an iterator here
        question_url_b = "https://question.jd.com/question/getQuestionAnswerList.action?page=%d&productId=%d" % (page_number,item_id)
        req = scrapy.Request(question_url_b,callback=self.parse_buyer)
        yield req

        # seller's answer
        page_number = 1
        # should be an iterator here
        question_url_s = "https://club.jd.com/clubservice/newconsulation-%d-%d.html" % (item_id,page_number)
        yield scrapy.Request(question_url_s,callback=self.parse_seller)

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

