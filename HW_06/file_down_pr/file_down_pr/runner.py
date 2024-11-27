from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.img_spider import ImgSpiderSpider


if __name__ == '__main__':
    configure_logging()
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    # open('scrapy_result.csv', 'w').close()
    process = CrawlerProcess(get_project_settings())
    query = input('введите категорию картинок: ')
    process.crawl(ImgSpiderSpider, query=query)
    process.start()
