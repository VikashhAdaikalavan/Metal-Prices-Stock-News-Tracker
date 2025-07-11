import sqlite3
import os
import html

# Reading database

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir,'news.db')

with open (os.path.join(base_dir, "dashboard.html"),'r',encoding="utf-8") as f:
    html_content = f.read()

try:
    connection = sqlite3.connect(data_path)
    cursor = connection.cursor()
except:
    print("Connection failed")

cursor.execute("SELECT * FROM articles LIMIT 70 ")
data = cursor.fetchall()
connection.close()

insert_html = f""" 
const News = [
"""
for topic, title, url,summary, llm_summary in data:

    llm_summary = llm_summary.strip()
    llm_summary = llm_summary[0].upper() + llm_summary[1:]


    insert_html += f"""
    
    {{
        topic : "{html.escape(topic).capitalize()}",
        title:"{html.escape(title).capitalize()}",
        llm_summary:"{html.escape(llm_summary)}",
        url:"{html.escape(url)}"
    }},
    
    """
if insert_html.strip().endswith(','):
    insert_html = insert_html.rstrip(', \n')

insert_html += '\n];'



start_marker = "// START LOOP HERE "
end_marker = "// END LOOP HERE "
start_index = html_content.find(start_marker) + len(start_marker)
end_index = html_content.find(end_marker)
final_html = html_content[:start_index] + insert_html + html_content[end_index:]


with open (os.path.join(base_dir, "dashboard.html"),'w',encoding="utf-8") as f:
    f.write(final_html)









