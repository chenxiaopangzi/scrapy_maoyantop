# -*- coding: utf-8 -*-
import scrapy


class MaoyanSpider(scrapy.Spider):
    name = "maoyan"
    allowed_domains = ["maoyan.com/board/4?"]
    start_urls = ['http://maoyan.com/board/4?']

    def parse(self, response):
        htmls = response.css('.board-wrapper dd')

        for html in htmls:
            ranking = html.css('i.board-index::text').extract_first()
            img = html.css('img.board-img::attr(data-src)').extract_first()
            title = html.css('p.name a::text').extract_first()
            star = html.css('p.star::text').extract_first().strip().replace('主演：', '')
            releasetime = html.css('p.releasetime::text').extract_first()
            scores = html.css('p.score i::text').extract()
            score = scores[0] + scores[1]

            with open('猫眼top100榜.txt', 'a+') as f:
                f.write('排名：' + ranking + '\n')
                f.write('电影名称：' + title + '\n')
                f.write('图片：' + img + '\n')
                f.write('主演：' + star + '\n')
                f.write('上映时间：' + releasetime + '\n')
                f.write('评分：' + score)
                f.write('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

        next_page = response.css('ul.list-pager li:last-child a::attr(href)').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
            print('正在抓取第' + next_page + '页')
