import web_crawler
from threading import Thread
from multiprocessing import Process

if __name__ == '__main__':
    novel_urls = ['http://www.quannovel.com/read/640/', 'http://www.quannovel.com/read/638/',
                  'http://www.quannovel.com/read/666/', 'http://www.quannovel.com/read/724/',
                  'http://www.quannovel.com/read/635/', 'http://www.quannovel.com/read/628/',
                  'http://www.quannovel.com/read/741/', 'http://www.quannovel.com/read/623/']
    spider = web_crawler.NovelSpider()
    for i in range(8):
        # t = Thread(target=spider.get_novel, args=[novel_urls[i], i + 1])
        # t.start()

        # p = Process(target=spider.get_novel, args=(novel_urls[i], i + 1))
        # p.run()

        spider.get_novel(novel_urls[i], i + 1)



