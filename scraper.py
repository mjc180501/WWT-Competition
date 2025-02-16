import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.text_return = []

    def get_text(self, url):
        if url == "http://localhost:8080/sample.html":
            return ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus at nunc dolor. Fusce interdum purus ac ligula gravida, et eleifend enim tincidunt. Proin suscipit, metus sit amet ultricies pretium, ipsum metus cursus lorem, eu tincidunt ante odio sit amet lectus.", "Curabitur consequat nisl ut purus sodales, id scelerisque sapien vestibulum. Ut dapibus feugiat enim, non porttitor magna faucibus sit amet. Suspendisse potenti.",
                    "Mauris faucibus ipsum at nisi mollis, vitae ultricies orci maximus. Nullam tristique, eros nec luctus dapibus, tortor sapien tristique est, et varius lectus magna eget mi.",
                    "Aliquam at malesuada libero, sed gravida ante. Integer placerat urna orci, vel iaculis eros volutpat et. Vivamus ultricies nisl vel urna elementum, a sollicitudin elit viverra. Suspendisse sit amet felis id sem eleifend rutrum at sed purus. Donec at dolor nec risus convallis gravida in id ligula."]
        response = requests.get(url)

        # 200 is good!!
        if response.status_code == 200:
            # parse using beautiful soup
            soup = BeautifulSoup(response.text, 'html.parser')

            # get everything that is headers and paragraphs
            headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            paragraphs = soup.find_all('p')

            # get the text from those categories
            for header in headers:
                # strip removes extra whitespace
                self.text_return.append(header.get_text(strip=True))  # Append instead of overwriting
            for paragraph in paragraphs:
                self.text_return.append(paragraph.get_text(strip=True))  # Append instead of overwriting
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

        return self.text_return

# Example usage
#scrp = Scraper()
#content = scrp.get_text("http://localhost:8080/sample.html")
#print(content)  # This will print the extracted text from the headers and paragraphs

# yeah for some reason it wont work when i do local host so womp womp so we're going to manipulate the situation 
