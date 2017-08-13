import scrapy
import re
import json
from .info import parse_info

class QuotesSpider(scrapy.Spider):
    name = "jd_qa"
    start_urls = [
        'https://item.jd.com/4835534.html'
    ]

    # however this function can only get the front two answers in answerlist
    # because the rest is not included in the returning json
    def parse_buyer(self,response):
        print("buyer:",response)
        # question list of buyer-answers
        res = json.loads(response.body)
        question_list = []
        answer_list = []
        page_number = int(re.findall('\d+', response.url)[0])
        item_id = int(re.findall('\d+', response.url)[1])

        if res["questionList"]:
            for question in res["questionList"]:
                answer_list.clear()
                for answer in question["answerList"]:
                    answer_list.append(answer["content"])

                question_list.append(
                    {
                        "question_id": question["id"],
                        "question":question["content"],
                        "answer":answer_list.copy()
                    }
                )
            yield {
                "item_id":item_id,
                "page_number":page_number,
                "buyer_qa":question_list
            }

            page_number = page_number + 1
            question_url = "https://question.jd.com/question/getQuestionAnswerList.action?page=%d&productId=%d" % (
            page_number, item_id)
            yield scrapy.Request(question_url, callback=self.parse_buyer)
        else:
            print("end of buyer_qa parser.")
            pass

        # "ensure_ascii=False" ensure the proper presentation of Chinese characters
        # show what's in the json received
        #print(json.dumps(res,indent=4,ensure_ascii=False))
        pass

    # the complete answerlist could be accessed through this function
    def parse_buyer_makeup(self,response):
        page_number = int(re.findall('\d+', response.url)[0])
        question_id = int(re.findall('\d+', response.url)[1])
        question_list = []

        question_url = "https://question.jd.com/question/getAnswerListById.action?page=1&questionId=3961029"
        yield {
            "question_id": question_id,
            "page_number": page_number,
            "buyer_makeup": question_list
        }

    def parse_seller(self,response):
        print("seller:",response)
        page_number = int(re.findall('\d+', response.url)[0])
        item_id = int(re.findall('\d+', response.url)[1])
        # process here

        page_number = page_number + 1
        question_url = "https://club.jd.com/allconsultations/%d-%d-1.html" % (item_id, page_number)
        yield scrapy.Request(question_url, callback=self.parse_seller)

        #print(response.body)
        #res = json.loads(response.body.decode("gbk"))
        #print(json.dumps(res, indent=4, ensure_ascii=False))

        pass

    def parse(self, response):
        # get item id
        item_id = int(re.findall('\d+',response.url)[0])
        print("item-id:",item_id,type(item_id))

        # parse item info
        info = parse_info(response)

        # buyer's answer, start from page_number
        page_number = 1
        # the parser will iterate itself till the end page
        question_url_b = "https://question.jd.com/question/getQuestionAnswerList.action?page=%d&productId=%d" % (page_number,item_id)
        req = scrapy.Request(question_url_b,callback=self.parse_buyer)
        yield req

        # seller's answer, start from page_number
        page_number = 1
        # the parser will iterate itself till the end page
        question_url_s = "https://club.jd.com/allconsultations/%d-%d-1.html" % (item_id,page_number)
        yield scrapy.Request(question_url_s,callback=self.parse_seller)

        """
        yield{
            'item_id':item_id,
            'url1':question_url_b,
            'url2':question_url_s,
        }

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            
        """

