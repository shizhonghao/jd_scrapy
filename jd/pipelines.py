# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo

class JdPipeline(object):

    def process_item(self, item, spider):

        # should be updating a document
        if "buyer_qa" in item:
            with open("buyerQ.txt",'a',encoding="utf-8") as f:
                for question in item["buyer_qa"]:
                    question["question"] = question["question"].replace('\n', '')
                    f.write(question["question"]+'\n')
                    pass

            collection = self.db["buyer_qa"]
            #for question in item["buyer_qa"]:
            collection.update({"item_id":item["item_id"]},{"$addToSet": {"buyer_qa":{"$each":item["buyer_qa"]}}},upsert=True)

        elif "seller_qa" in item:
            with open("sentence.txt",'a',encoding="utf-8") as f_q:
                with open("answer.txt",'a',encoding="utf-8") as f_a:
                    for question in item["seller_qa"]:
                        question["question"] = question["question"].replace('\n','')
                        f_q.write(question["question"]+'\n')
                        question["answer"] = question["answer"].replace('\n','')
                        question["answer"] = question["answer"][3:-17]
                        f_a.write(question["answer"]+'\n')
            collection = self.db["seller_qa"]
            collection.update({"item_id": item["item_id"]},
                              {"$addToSet": {"seller_qa": {"$each": item["seller_qa"]}}},
                              upsert=True)

        elif "item_info" in item:
            collection = self.db["item_info"]
            collection.insert(item,check_keys=False)
            pass
        return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client["JD"]

    def close_spider(self, spider):
        self.client.close()
'''
        elif "buyer_makeup" in item:
            collection = self.db["buyer_qa"]
            collection.update({"item_id": item["item_id"]},
                              {"$addToSet": {"buyer_qa."+str(item["question_id"])+".answer": {"$each":item["buyer_makeup"] }}},
                              upsert=True)

            collection.update({"item_id": item["item_id"]},
                              {"$inc": {"buyer_qa."+str(item["question_id"])+".cnt":1}},
                              upsert=True)
'''
