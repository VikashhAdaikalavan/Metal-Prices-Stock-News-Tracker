import scrapy

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
    "https://www.indiatoday.in/states/tamil-nadu",  # Tamil Nadu state news
    "https://www.indiatoday.in/states/telangana"    # Telangana state news
    ]

    def parse(self, response):
        
        for article in response.css("div.B1S3_content__wrap__9mSB6"):
            
            title= article.css("h2 a::text").get()
            relative_url = article.css("h2 a::attr(href)").get()
            full_url = response.urljoin(relative_url)
            summary = article.css("div.B1S3_story__shortcont__inicf p::text").get()

            if title == None:
                break


            yield {
                "title": title,
                "url": full_url,
                "summary": summary
            }

        yield{
            "title": "break"
        }
            

