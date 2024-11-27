# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
# from pprint import pprint
import os


class FileDownPrPipeline:
    def process_item(self, item, spider):
        return item


class PhotosPipeline(ImagesPipeline):

    # запрос для скачивания картинки
    def get_media_requests(self, item, info):
        if item['photos']:
            try:
                yield scrapy.Request(item['photos'])
                # print('скачивание успешно')
            except Exception as e:
                print(e)

    # конкретизируем url и локальные пути
    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1]['path'] for itm in results if itm[0]]
            item['url'] = [itm[1]['url'] for itm in results if itm[0]]
        return item

    # создаем уникальные имена для сохранения файлов и указываем путь
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        return f"/photos_01/{item['name']}-{image_guid}.jpg"
