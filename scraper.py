from requests_html import HTMLSession

class Scraper:
    def __init__(self):
        pass
    def get_lucky(self):
        result = []
        s = HTMLSession()
        r = s.get("https://www.luck-d.com/")
        cards = r.html.find("div.gallery_cell_layer", )
        for c in cards:
            img = c.find("img", first=True).attrs["src"]
            link = ""
            links = list(c.absolute_links)
            if links != []:
                link = list(c.absolute_links)[0]
            data = {
                "img": img,
                "content": c.text.replace("\n", " "),
                "link": link
            }
            result.append(data)
        return result

    def get_shoe_prize(self):
        result = []
        url = "https://www.shoeprize.com/today/?filter={%22excludeKor%22:0,%22includeKor%22:1,%22excludeEnd%22:1}"
        s = HTMLSession()
        r = s.get(url)
        r.html.render(timeout=20) 
        cards = r.html.find("div.product_list_area", )
        box = list(cards)[1]
        arr = box.find("li")
        for a in arr:
            text = a.text.replace("\n", " ")
            links = list(a.absolute_links)
            img = a.find("img", first=True).attrs["data-src"]
            link = ""
            if links != []:
                link = links[0]
            data = {
                "img": img,
                "content": text,
                "link": link
            }
            result.append(data)
        return result