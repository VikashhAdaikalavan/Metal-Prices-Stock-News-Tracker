import scrapy
import time

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    start_urls = [
    "https://www.indiatoday.in/world/all",              # International
    "https://www.indiatoday.in/india",              # National news
    "https://www.indiatoday.in/technology",         # Tech
    "https://www.indiatoday.in/education-today",    # Education
    "https://www.indiatoday.in/business",           # Business
    "https://www.indiatoday.in/sports",             # Sports
    "https://www.indiatoday.in/movies",   # Entertainment
    "https://www.indiatoday.in/science",            # Science
    "https://www.indiatoday.in/lifestyle",          # Lifestyle
    "https://www.indiatoday.in/auto",               # Auto
    ]


    custom_settings = {'ITEM_PIPELINES': {'scrappyfile.pipelines.News_Summary_Pipeline':300}}
    
    def parse(self, response):

        topics = ['World','India','Technology','education-today','business','sports','movies','science','lifestyle','auto','tamilnadu','telengana']
        
        for article in response.css("div.B1S3_content__wrap__9mSB6"):
            
            topic = response.url.split("/")[-1]
            if topic  == "all":
                topic = "world" 

            title= article.css("h2 a::text").get()
            relative_url = article.css("h2 a::attr(href)").get()

            if title == None:
                title= article.css("h3 a::text").get()
                relative_url = article.css("h3 a::attr(href)").get()

            full_url = response.urljoin(relative_url)
            summary = article.css("div.B1S3_story__shortcont__inicf p::text").get()

            if title == None:
                break


            yield {
                "topic":topic,
                "title": title,
                "url": full_url,
                "summary": summary
            }
        
            

