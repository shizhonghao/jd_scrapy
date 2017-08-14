import scrapy
import re
import json
from .info import parse_info

class QuotesSpider(scrapy.Spider):
    name = "jd_qa"
    start_urls = [
        'https://item.jd.com/4835534.html',
        'https://item.jd.com/2967929.html'
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
        answer_list = []
        res = json.loads(response.body)

        if res["answers"]:
            item_id = res["answers"][0]["productId"]
            for answer in res["answers"]:
                answer_list.append(answer["content"])
            page_number = page_number + 1
            question_url = "https://question.jd.com/question/getAnswerListById." \
                           "action?page=%d&questionId=%d" %(page_number,question_id)
            yield scrapy.Request(question_url,callback=self.parse_buyer_makeup)
            yield {
                "item_id":item_id,
                "question_id": question_id,
                "page_number": page_number,
                "buyer_makeup": answer_list
            }
        else:
            print("end of buyer_qa makeup parser.")
            pass

    def parse_seller(self,response):
        print("seller:",response)
        item_id = int(re.findall('\d+', response.url)[0])
        page_number = int(re.findall('\d+', response.url)[1])
        # process here
        question_list = []
        q = response.xpath(
            '''
            /html/body//div[@class="w"]//div[@class="right"]
            //div[@class="Refer_List"]//div//dl[@class="ask"]/dd/a/text()
            ''').extract()
        a = response.xpath(
            '''
            /html/body//div[@class="w"]//div[@class="right"]
            //div[@class="Refer_List"]//div//dl[@class="answer"]/dd/text()
            ''').extract()
        for question in q:
            question_list.append({"question":question.strip()})
        for index,answer in enumerate(a):
            question_list[index]["answer"] = answer.strip()

        if question_list:
            yield {
                "item_id": item_id,
                "page_number": page_number,
                "seller_qa": question_list
            }
            page_number = page_number + 1
            question_url = "https://club.jd.com/allconsultations/%d-%d-1.html" % (item_id, page_number)
            yield scrapy.Request(question_url, callback=self.parse_seller)
        else:
            print("end of seller_qa parser.")

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

