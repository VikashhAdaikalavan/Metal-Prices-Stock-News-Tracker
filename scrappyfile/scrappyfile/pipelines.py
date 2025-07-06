# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrappyfile.llm import summarize
import sqlite3
import os


class News_Summary_Pipeline:
    #To feed the scraped data into an LLM to get the summary if the news is longer
    def process_item(self, item, spider):
        adapted_item = ItemAdapter(item)
        adapted_item["llm_summary"] = summarize(adapted_item["summary"])

        return item

class Database_Pipeline:
    def open_spider(self,spider):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #I wanted to store the database in the directory where scrapy.cfg is stored
        db_path = os.path.join(base_dir, 'news.db')
        
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS articles")
        self.cursor.execute("""CREATE TABLE articles (topic TEXT,title TEXT,url TEXT UNIQUE,summary TEXT,llm_summary TEXT)""")

    #To store the data in a sqlite databse
    def process_item(self,item,spider):
        adapted_item = ItemAdapter(item)
        try:
            self.cursor.execute("INSERT INTO articles values(?,?,?,?,?)",(adapted_item.get('topic'),adapted_item.get('title'),adapted_item.get('url'),adapted_item.get('summary'),adapted_item.get('llm_summary')))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Duplicate Entry")

        return item
    def close_spider(self,spider):
        self.connection.close()