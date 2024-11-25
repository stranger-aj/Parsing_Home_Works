# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class HomeworkPipeline:
    def process_item(self, item, spider):
        # book_dict = {}
        # book_dict['name'] = item.get('name')
        # book_dict['cost'] = float(item.get('cost'))
        # book_dict['url'] = item.get('url')
        # book_dict['rate'] = float(item.get('rate'))
        # book_dict['description'] = ' '.join(
        #     ' '.join(item.get('description')[1:]).split())

        # keys = book_dict.keys()
        # with open('data_result.csv', 'a', newline='', encoding="UTF-8") as output_file:
        #     dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        #     # dict_writer.writeheader()
        #     dict_writer.writerow(book_dict)
        pass
        # print("book_dict= ", book_dict)
