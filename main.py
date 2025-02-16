from scraper import Scraper
from explicitcontent import predict_nsfw

scrp = Scraper()
content = scrp.get_text("http://localhost:8080/sample.html")
print(content)
content_string = []
for elem in content:
    split = elem.split(" ")
    content_string.append(split)

print(content_string)
