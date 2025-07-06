# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrappyfile.llm import summarize
import sqlite3


class News_Summary_Pipeline:
    #To feed the scraped data into an LLM to get the summary if the news is longer
    def process_item(self, item, spider):
        adapted_item = ItemAdapter(item)
        adapted_item["llm_summary"] = summarize(adapted_item["summary"])

        return item

class Database_Pipeline:
    #To store the data in a sqlite databse
    def process_item(self,item,spider):
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS article")
        cursor.execute("Create new table article()")


        return item