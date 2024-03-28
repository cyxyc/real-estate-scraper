from os import path
from imgurpython import ImgurClient
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

#TODO: propojeni imguru a srealit? - pockat co ukaze praxe. pokud bude fungovat rozdelene, tak nechat. 
#nejlepsi asi bude pak cely tenhle download z srealit a upload na imgur dat dohromady (scraper si bude volat tuhle funkci nebo to bude primo v nem)
#scraper by pak krome img_urls (z srealit) vracel i imgur_urls (z imgur) (sreality URL vlastne ani nepotrebuju)
#nezapomenout pak predelat analytics.ipynb aby se to korespondovalo s imgurem
#-nebo ne. nedelat to. pokud bych to udelal tak by se to pak hrozne blbe nebugovalo. nechat to rozdelene jako jednotlive funkcni celky.
#udelat to jen v pripade ze bych se bal ze na API dostanu too many requests a budu muset cekat nez se to vsechno stahne (ten imgur by to zpomalil)

df = pd.read_csv('df_imgs.csv')

client_id = '7c437cedc06d28a'
client_secret = '170eaa169865ce4f60cb70f0f8aa31b70788b69e'

client = ImgurClient(client_id, client_secret)

def upload_image_from_url(url):
    response = requests.get(url)
    print(response)
    img = Image.open(BytesIO(response.content))
    img.save('temp.png')
    result = client.upload_from_path('temp.png')
    print(result["link"])
    return result['link']

df['imgur_url'] = df['photo_URLs'].apply(upload_image_from_url)
df.to_csv('df_imgs_with_imgur.csv', index=True)