import scrapy
import types
import json

# process item info from HTML here
def parse_info(response):
    path = 'body//div[@class="w"][6]//div[@class="detail"]//div[@class="ETab"]//div[@class="tab-con"]//div[@data-tab="item"][2]//div[@class="Ptable"]/div'
    infos = response.xpath(path)
    count = 1
    reDict = {}
    for info in infos:
        secPath = path + '[' + str(count) + ']'
        secInfo = response.xpath(secPath+'/*/text()').extract_first()
        #print(secInfo)
        count += 1
        thirdPath = secPath + '/dl/*/text()'
        thirdInfo = response.xpath(thirdPath).extract()
        num = 0
        aDict = {}
        for tInfo in thirdInfo:
            if '\n' not in tInfo:                    
                if num == 0:
                    name = tInfo
                    string = tInfo + ':'
                    num = 1
                else:
                    aDict[name] = tInfo
                    string = tInfo
                    num = 0
                #print(string)
        #print(aDict)
        reDict[secInfo] = aDict
    # print(json.dumps(reDict,indent=4,ensure_ascii=False))
    return reDict
    
