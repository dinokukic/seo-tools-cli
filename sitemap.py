from lxml import etree
import requests

r = requests.get("https://www.lano.io/sitemap-0.xml")

root = etree.fromstring(r.content)

children = root.getchildren()

print(children)