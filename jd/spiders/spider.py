import scrapy
import re
import json
from .info import parse_info
import win_unicode_console
win_unicode_console.enable()

#response.xpath('body/div[@id="J_searchWrap"]/div[@id="J_container"]/div[@id="J_main"]/div[@class="m-list"]/div[@class="ml-wrap"]/div[@id="J_goodsList"]/ul/li/@data-sku').extract()

class QuotesSpider(scrapy.Spider):
    name = "jd_qa"
    id_list = [
        '5706771','6629390','6737464','6023686','6627494','5663902','6008133','5853593',
        '3234250','3888216','4914531','3355143','5544038','6001239','5181380','4483094',
        '4207732','5005731','5963064','3893501','6558982','5148371','4154589','4483072',
        '2600242','5007536','5105028','4483108','4193810','3604173','5001175','5001209',
        '5089275','4230919','5089253','5663902','6019534','5924252','5089225','5826214',
        '5835263','5618804','4554941','5544038','5544036','5912043','6008133','4120319',
        '4586850','5425721','5181380','1861102','4914531','3234250','3888216','6558984',
        '5005733','3355143','5159262','5842519','4207732','6708229','6022664','4143422',
        '4483094','4768465','5159242','5962246','5963064','4720749','3893501','4746262',
        '4432052','5911960','6070852','4154589','3458059','3133827','3133857','5148371',
        '4094680','4611415','2600242','6389385','4510588','5283387','5357340','4112338',
        '4483072','6631219','3889169','5762407','5495676','6661976','5813073','4577217',
        '4554969','5437633','5484048','6405876','6176077','5283377','5495676','4734101',
        '1592994','4884236','1945514','4938584','5107323','5901119','5204046','6022742',
        '5906527','5980401','6134977','3604173','4024777','3749095','4934609','6113024',
        '4571451','4503858',''
    ]
    #'https://item.jd.com/4586850.html'
    start_urls = []
    for id in id_list:
        newUrl = 'https://item.jd.com/'+id+'.html'
        start_urls.append(newUrl)
        #'https://item.jd.com/2967929.html',
        #'https://item.jd.com/4835534.html'

    # however this function can only get the front two answers in answerlist
    # because the rest is not included in the returning json
    def parse_buyer(self,response):
        #print("buyer:",response)
        # question list of buyer-answers
        res = json.loads(response.body_as_unicode())
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
                        "question_id": str(question["id"]),
                        "question": question["content"],
                        "answer": answer_list.copy()
                    }
                )

                question_url = "https://question.jd.com/question/getAnswerListById." \
                               "action?page=%d&questionId=%d" % (1, question["id"])
                yield scrapy.Request(question_url, callback=self.parse_buyer_makeup)

            yield {
                "item_id":item_id,
                #"page_number":page_number,
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
        res = json.loads(response.body_as_unicode())

        if res["answers"]:
            item_id = res["answers"][0]["productId"]
            for answer in res["answers"]:
                answer_list.append(answer["content"])
            page_number = page_number + 1
            question_url = "https://question.jd.com/question/getAnswerListById." \
                           "action?page=%d&questionId=%d" %(page_number,question_id)
            if(res["moreCount"]>1):
                yield scrapy.Request(question_url,callback=self.parse_buyer_makeup)
            yield {
                "item_id":item_id,
                "question_id": question_id,
                #"page_number": page_number,
                "buyer_makeup": answer_list
            }
        else:
            print("end of buyer_qa makeup parser:",question_id)
            pass

    def parse_seller(self,response):
        #print("seller:",response)
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
                #"page_number": page_number,
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
        #print("item-id:",item_id,type(item_id))

        # parse item info
        info = parse_info(response)
        yield {
            'item_id':item_id,
            'item_info':info
        }

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

