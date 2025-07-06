# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrappyfile.llm import summarize


class News_Summary_Pipeline:
    def process_item(self, item, spider):
        adapted_item = ItemAdapter(item)
        adapted_item["llm_summary"] = summarize(adapted_item["summary"])

        return item

class Database_Pipeline:
    def process_item(self,item,spider):

        return item