import scrapy

# process item info from HTML here
def parse_info(response):
    info = response.xpath('body//div[@class="w"][6]//div[@class="detail"]//div[@class="ETab"]//div[@class="tab-con"]//div[@data-tab="item"][2]//div[@class="Ptable"]/div').extract()
    print(info)
    
