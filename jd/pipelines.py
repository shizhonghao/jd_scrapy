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
            collection = self.db["buyer_qa"]
            for question in item["buyer_qa"]:
                collection.update({"item_id":item["item_id"]},
                                  {"$set": {"buyer_qa."+str(question["question_id"]):question}},
                                  upsert=True)

        elif "buyer_makeup" in item:
            collection = self.db["buyer_qa"]
            collection.update({"item_id": item["item_id"]},
                              {"$addToSet": {"buyer_qa."+str(item["question_id"])+".answer": {"$each":item["buyer_makeup"] }}},
                              upsert=True)
            """
            collection.update({"item_id": item["item_id"]},
                              {"$inc": {"buyer_qa."+str(item["question_id"])+".cnt":1}},
                              upsert=True)
            """
            
        elif "seller_qa" in item:
            collection = self.db["seller_qa"]
            collection.update({"item_id": item["item_id"]},
                              {"$addToSet": {"seller_qa": {"$each": item["seller_qa"]}}},
                              upsert=True)

        elif "item_info" in item:
            collection = self.db["item_info"]
            collection.insert_one(item)
            pass
        return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client["JD"]

    def close_spider(self, spider):
        self.client.close()
