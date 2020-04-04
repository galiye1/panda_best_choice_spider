# -*- coding: utf-8 -*-

import os
import time

import scrapy
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from lxml import etree

from panda_best_choice.items import PandaBestChoiceItem


class PandaSpider(RedisSpider):
    name = 'panda'
    allowed_domains = ['xiongmaoyouxuan.com']

    redis_key = "panda:start_urls"

    def parse(self, response):
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + '\chromedriver.exe')
        self.driver.get('http://www.xiongmaoyouxuan.com/#/tab/5')
        # 处理chrome版本与webdriver版本兼容问题
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            pass

        self.driver.maximize_window()# chrome窗口最大化
        time.sleep(3)
        i = 0
        # 无限制爬取网页内容，直到没有合适的可爬取内容
        while True:
            if i % 4 == 0:           # 每取4个元素（也就是1行），滚动条往下拉一次
                self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
                time.sleep(1)
            # 由于查看更多按钮全局只需要点击一次，所以先点击按钮
            if i == 0:
                more_btn = self.driver.find_element_by_class_name('items-more-btn')
                more_btn.click()
                time.sleep(1)
            # 详细内容无链接，因此通过点击事件跳转网页
            try:
                i += 1
                div = self.driver.find_element_by_xpath("//ul[@class='base-commodity-list commodity-list']/li[%d]" % i)
                div.click()
            except:
                break
            item = self.switch()
            yield item

    # 解析页面源码，爬取需要的数据
    def switch(self):
        self.driver.switch_to.window(self.driver.window_handles[1]) # 切换到新窗口
        time.sleep(2)
        source = self.driver.page_source
        html = etree.HTML(source)
        title = html.xpath("//h1[@class='cmd-title']/text()")[0].strip()
        original_price = html.xpath("//p[@class='original-price']/i/text()")[0].replace('原价', '').strip()
        last_price = html.xpath("//div[@class='last-price']/span[@class='price']/text()")[0]
        coupon = html.xpath("//div[@class='last-price']/span[@class='coupon-info']/text()")[0]
        sale_num = html.xpath("//div[@class='last-price']/span[@class='sale-num']/text()")[0]
        expire_date = html.xpath("//p[@class='expire-date']/span/text()")[0].replace('优惠有效期：', '').strip()
        item = PandaBestChoiceItem(
            title=title,
            original_price=original_price,
            coupon=coupon,
            sale_num=sale_num,
            expire_date=expire_date
        )
        self.driver.close()                                         # 关闭新窗口
        self.driver.switch_to.window(self.driver.window_handles[0]) # 切换到原窗口
        return item