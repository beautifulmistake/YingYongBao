# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from yingyongbao.utils import get_db
mongo_db = get_db()


class YingyongbaoPipeline(object):
    # 创建文件的方法
    def open_spider(self,spider):
        """
        在当前目录下创建文件，记录采集的数据
        :param spider:
        :return:
        """
        self.file = open('./应用宝采集测试数据.txt', 'a+', encoding='utf-8', errors="ignore")   # 创建文件
    def process_item(self, item, spider):
        keyword = item["keyword"]    # 搜索关键字
        print("查看搜索关键字=================：", keyword)
        appName = item["appName"]  # APP名称
        print("获取APP名称====================：", appName)
        description = item["description"]  # 应用信息
        print("获取APP应用信息================：", description)
        appPublishTime = item["appPublishTime"]  # 上架时间，将时间转换显示格式
        print("获取APP上架时间================：", appPublishTime)
        authorName = item["authorName"]  # 开发商
        print("获取APP开发商==================：", authorName)
        appDownCount = item["appDownCount"]  # 下载量
        print("获取APP下载量==================：", appDownCount)
        iconUrl = item["iconUrl"]  # 图片地址
        print("获取APP图片====================：", iconUrl)
        detail_page_url = item["detail_page_url"]  # 详情页的链接，需要做拼接获取完整
        print("获取详情页链接=================：", detail_page_url)
        categoryName = item["categoryName"]  # APP种类
        print("获取APP种类====================：", categoryName)
        fileSize = item["fileSize"]  # APP大小
        print("获取APP大小====================：", fileSize)
        versionName = item["versionName"]  # 版本号,需要在前面拼接一个V
        print("获取APP版本号==================：", versionName)
        averageRating = item["averageRating"]  # 评分，需要对数据进行取舍
        print("获取APP评分====================：", averageRating)
        commentNum = item["commentNum"]  # APP评论数
        print("获取APP评论数==================：", commentNum)
        # 将采集的目标字段整理成统一格式，定义变量接收拼接的结果
        result_content = ""
        result_content = result_content.join(
            keyword + "ÿ" + appName + "ÿ" + description + "ÿ" + appPublishTime + "ÿ" + authorName + "ÿ" + str(appDownCount) + "ÿ" +
            iconUrl + "ÿ" + detail_page_url + "ÿ" + categoryName + "ÿ" + fileSize + "ÿ" +
            versionName + "ÿ" + averageRating + "ÿ" + commentNum + "\n"
        )
        # 将采集的数据写入文件
        self.file.write(result_content)
        self.file.flush()
        return item
    # 关闭文件的方法
    def close_spider(self,spider):
        """
        将采集的数据写入文件完成后，关闭文件
        :param spider:
        :return:
        """
        # 关闭文件
        self.file.close()


class ResultToMongoPipeline(object):
    """抓取结果导入 mongo"""

    def __init__(self, settings):
        self.collections_name = settings.get('RESULT_COLLECTIONS_NAME')

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_item(self, item, spider):
        mongo_db[self.collections_name].insert(item)
        return item
