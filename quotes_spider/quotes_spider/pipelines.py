# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Ex: The price of an item does not contain the taxes. Here you can get the value apply the taxes and return the item
class QuotesSpiderPipeline:
    def process_item(self, item, spider):
        if item['author']:
            item['author'] = item['author'][0].upper()
        return item
