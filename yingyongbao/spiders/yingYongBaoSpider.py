from urllib import parse
import json
import re
import time
import redis
import scrapy
from scrapy_redis.spiders import RedisSpider

from yingyongbao.items import YingyongbaoItem
# 全局的变量，用于设定默认值，便于后期需求变更时代码的修改


default_value = "null"
"""
此爬虫根据提供的关键字进行爬取应用宝上相关信息
"""
# 定义自己的爬虫类
class YingYongBaoSpider(RedisSpider):
    # 为爬虫命名
    name = "yingyongbaoSipder"
    redis_key = "yingyongbaoSpider:start_urls"
    # 初始化函数
    def __init__(self):
        # 定义全局变量统计采集完成关键字的数量
        self.finshed = 0
        # 定义全局变量统计无采集结果关键字数量
        self.noResult = 0
        # 与获取的关键字做拼接获取初次请求的url
        self.base_url = "https://sj.qq.com/myapp/searchAjax.htm"
        self.detailPageUrl = "https://sj.qq.com/myapp/detail.htm?apkName={0}"
        self.headers = {
            'Referer':'https://sj.qq.com/myapp/search.htm?kw=%E9%80%B8%E6%B0%A7',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
        }
    # 根据关键字构造初始请求
    def start_requests(self):
        """
        从redis 中读取关键字，然后与self.base_url做拼接获取请求页面
        注意分析Ajax请求时是POST请求
        :return:
        """
        connect = redis.Redis(host='127.0.0.1', port=6379, db=4, password='pengfeiQDS')   # 获取redis数据库连接对象
        keyword_total = connect.dbsize()    # 获取redis数据库关键字总数量
        # 遍历获取每一个关键字
        for index in range(500001,620001):
        #for index in range(50001,keyword_total+1):
            print("查看关键字：",index)
            keyword = connect.get(str(index)).decode('utf-8')   # 使用get方法获取关键字
            #print("查看获取的关键字：",keyword)
            formdata = {
                'kw': parse.quote(keyword),
                'pns': '',
                'sid': ''
            }
            # 将拼接之后的url加入到爬取队列之中,将关键字传递到解析函数（爬取失败或完成后写入文件使用）
            yield scrapy.FormRequest(url=self.base_url, callback=self.get_page, formdata=formdata, meta={'keyword': keyword}, method="POST")
    # 解析页面函数
    def get_page(self,response):
        """
        解析响应的页面，获取包含数据的json
        :param response:
        :return:
        """
        # 判断状态码
        if response.status == 200:

            # 一下为测试代码
            # print("查看当前的关键字：",response.meta['keyword'])
            # content = json.loads(response.text)
            # print("查看获取的内容：",content)
            # appDetails = content["obj"]["appDetails"]
            # print("获取APP详情：",appDetails)
            # for i in appDetails:
            #     print(i)

            print("查看当前页的请求：", response.url)
            keyword = parse.unquote(response.meta['keyword'])  # 获取当前采集的关键字
            print("查看当前搜索关键字：", keyword)
            pattern = re.compile(r'"obj":(.*?)"pageContext"')  # 匹配规则
            json_result = re.search(pattern, response.text).group(1)[:-1]  # 匹配出包含目标字段的json串,去除最后的逗号
            print("匹配出的结果：", json_result)  # 查看获取的内容
            result = json.loads(json_result)  # 将字符串转换成字典形式
            print("转换成字典后的结果：", result)
            # 获取判断是否有下一页的依据
            hasNext = result.get("hasNext")
            print("查看是否有下一页：", hasNext)
            # 获取拼接动态请求的字段
            pageNumberStack = result.get("pageNumberStack")
            print("查看动态请求：", pageNumberStack)
            appDetails = result.get("appDetails")  # 获取包含目标字段的列表
            for appDetail in appDetails:  # 遍历列表获取每一条信息
                item = YingyongbaoItem()
                appName = appDetail.get("appName")  # APP名称
                print("获取APP名称====================：", appName)
                description = appDetail.get('description').strip()  # 应用信息
                print("获取APP应用信息================：", description)
                appPublishTime = appDetail.get("apkPublishTime")  # 上架时间，将时间转换显示格式
                print("获取APP上架时间================：", appPublishTime)
                authorName = appDetail.get("authorName")  # 开发商
                print("获取APP开发商==================：", authorName)
                appDownCount = appDetail.get("appDownCount")  # 下载量
                print("获取APP下载量==================：", appDownCount)
                iconUrl = appDetail.get("iconUrl")  # 图片地址
                print("获取APP图片====================：", iconUrl)
                detail_page_url = appDetail.get("pkgName")  # 详情页的链接，需要做拼接获取完整
                print("获取详情页链接=================：", detail_page_url)
                categoryName = appDetail.get("categoryName")  # APP种类
                print("获取APP种类====================：", categoryName)
                fileSize = appDetail.get("fileSize")  # APP大小
                print("获取APP大======================：", fileSize)
                versionName = appDetail.get("versionName")  # 版本号,需要在前面拼接一个V
                print("获取APP版本号==================：", versionName)
                averageRating = appDetail.get("averageRating")  # 评分，需要对数据进行取舍
                print("获取APP评分====================：", averageRating)
                # 判断是否为空，为空则赋值为默认值，防止某条数据的丢失
                item["keyword"] = keyword.strip()  # 搜索关键字
                item["appName"] = appName if appName else default_value  # APP名称
                item["description"] = "".join((description.split())) if description else default_value    # 应用信息
                item["appPublishTime"] = time.strftime("%Y-%m-%d", time.localtime(appPublishTime)) if appPublishTime else default_value    # 上架时间
                item["authorName"] = authorName if authorName else default_value    # 开发者
                item["appDownCount"] = appDownCount if appDownCount else default_value  # APP下载量
                item["iconUrl"] = iconUrl if iconUrl else default_value  # APP图片链接
                item["detail_page_url"] = self.detailPageUrl.format(detail_page_url) if detail_page_url else default_value  # 详情页链接
                item["categoryName"] = categoryName if categoryName else default_value  # APP种类
                item["fileSize"] = '%.2f' % (fileSize / 1024 / 1024) + "M" if fileSize else default_value   # APP大小
                item["versionName"] = "V" + versionName if versionName else default_value   # APP版本号
                item["averageRating"] = '%.1f' % averageRating if averageRating else default_value  # APP评分
                # 腾讯应用宝中无评论数，故用默认值代替
                item['commentNum'] = default_value
                yield item
            # 判断是否有下一个请求,解决某个关键字的循环爬取
            if hasNext == 1:  # 如果是“1”代表有下一个请求
                """
                说明：有时从json中解析出来的和页面中显示的最后一次请求的
                pageNumberStack，hasNext 的值不一样，会报一个错，经测试很少出现
                未找到是何原因，此时暂不做处理
                """
                print("进入判断语句")
                # 构造下一个Ajax的请求
                formdata = {
                    'kw': parse.quote(keyword),
                    'pns': pageNumberStack,
                    'sid': '0'
                }
                # 构造请求继续解析,此处在处理某关键字的循环爬取时需要将关键字再重新当作参数传递回去，否则循环报错
                yield scrapy.FormRequest(url=self.base_url, callback=self.get_page, formdata=formdata, method="POST", meta={'keyword': keyword})
            elif hasNext == 0:
                # 完成该关键字的搜索
                self.finshed += 1
                print("当前已经完成%s个关键字"%self.finshed)
                with open('./完成搜索关键字.txt', 'a+', encoding='utf-8') as f:
                    f.write(keyword+"\n")
