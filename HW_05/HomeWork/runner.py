from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.book_worm import BookWormSpider


if __name__ == '__main__':
    configure_logging()
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    open('scrapy_result.json', 'w').close()
    # создание процесса
    process = CrawlerProcess(get_project_settings())
    process.crawl(BookWormSpider)
    process.start()
