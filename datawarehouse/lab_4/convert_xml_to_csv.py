import xmltodict
import pandas as pd

with open('products.xml') as xml_file:
    data = xmltodict.parse(xml_file.read())
    products = data['products']['product']
    df = pd.DataFrame(products)
    df.to_csv('products.csv', index=False)