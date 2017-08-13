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
            db = self.client["JD"]
            collection = db["buyer_qa"]
            collection.insert_one(item)
            """
            print("buyer_qa pipe here")
            f_name = "./data/buyer_qa/" + str(item["item_id"]) + "-" + str(item["page_number"]) + " buyer_qa.json"
            qa_res = str(json.dumps(item,indent=4,ensure_ascii=False))
            with open(f_name,"a",encoding="utf-8") as fp:
                fp.write(qa_res)
            """

        elif "buyer_makeup" in item:
            pass

        elif "seller_qa" in item:
            pass

        elif "" in item:
            pass
        return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost', 27017)

    def close_spider(self, spider):
        self.client.close()
