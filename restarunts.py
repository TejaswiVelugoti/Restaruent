from os import stat
import requests
from lxml import html
from urllib.parse import urljoin

state_urls = []
city_urls = []
base_url = "https://locations.villaitaliankitchen.com/US.html"
domain = "https://locations.villaitaliankitchen.com/"
def get_restaurent_details(state):
    output = []
    for st in state_urls:
        st_res = requests.get(st['url'])
        st_tree = html.fromstring(st_res.content)
        if '(1)' in st['count'] and state in st['state']:
            city = "".join(st_tree.xpath("//section[@id='location-info']//span[@class='c-address-city']//text()"))
            adress = "".join(st_tree.xpath("//section[@id='location-info']//address//text()"))
            google_maplink = "".join(st_tree.xpath("//section[@id='location-info']//a[@data-ga-category='Get Directions']/@href"))
            output.append({"state":state, "city":city, "adress":adress, "google_maplink":google_maplink})
        elif state in st['state']:
            if st_tree.xpath("//a[@class='c-directory-list-content-item-link']/@href"):
              city_urls = st_tree.xpath("//a[@class='c-directory-list-content-item-link']/@href")
              for ct in city_urls:
                city_base = urljoin(domain, ct)
                ct_res = requests.get(city_base)
                ct_tree = html.fromstring(ct_res.content)
                if ct_tree.xpath("//div[@class='c-location-grid-item']"):
                    for c in ct_tree.xpath("//div[@class='c-location-grid-item']"):
                        city = "".join(c.xpath(".//span[@class='c-address-city']//text()"))
                        adress = "".join(c.xpath(".//address//text()"))
                        google_maplink = "".join(c.xpath(".//a[@data-ga-category='Get Directions']/@href"))
                        output.append({"state":state, "city":city, "adress":adress, "google_maplink":google_maplink})
                else:
                    city = "".join(ct_tree.xpath("//section[@id='location-info']//span[@class='c-address-city']//text()"))
                    adress = "".join(ct_tree.xpath("//section[@id='location-info']//address//text()"))
                    google_maplink = "".join(ct_tree.xpath("//section[@id='location-info']//a[@data-ga-category='Get Directions']/@href"))
                    output.append({"state":state, "city":city, "adress":adress, "google_maplink":google_maplink})
            else:
              for s in st_tree.xpath("//div[@class='c-location-grid-item']"):
                city = "".join(s.xpath(".//span[@class='c-address-city']//text()"))
                adress = "".join(s.xpath(".//address//text()"))
                google_maplink = "".join(s.xpath(".//a[@data-ga-category='Get Directions']/@href"))
                output.append({"state":state, "city":city, "adress":adress, "google_maplink":google_maplink})
    return output

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
res = requests.get(base_url)
tree = html.fromstring(res.content)
for i in tree.xpath("//a[@class='c-directory-list-content-item-link']"):
    state_urls.append({"state": "".join(i.xpath("./@title")), "url": domain + "".join(i.xpath("./@href")), "count": "".join(i.xpath("./span[contains(@class, 'count')]/text()"))})
    if not '(1)' in "".join(i.xpath("./span[contains(@class, 'count')]/text()")):
      sub_url = domain + "".join(i.xpath("./@href"))
      sub_res = requests.get(sub_url)
      sub_tree = html.fromstring(sub_res.content)
      if sub_tree.xpath("//a[@class='c-directory-list-content-item-link']"):
        for s in sub_tree.xpath("//a[@class='c-directory-list-content-item-link']"):
          state_urls.append({"state": "".join(s.xpath("./@title")), "url": domain + "".join(s.xpath("./@href")), "count": "".join(s.xpath("./span[contains(@class, 'count')]/text()"))})
result = get_restaurent_details(input("Enter the state name: "))
for r in result:
  my_lis = list(r.values())
  print(my_lis)