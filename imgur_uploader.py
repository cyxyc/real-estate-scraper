from os import path
from imgurpython import ImgurClient
import pandas as pd

df = pd.read_csv('df2.csv')

client_id = '7c437cedc06d28a'
client_secret = '170eaa169865ce4f60cb70f0f8aa31b70788b69e'

client = ImgurClient(client_id, client_secret)

path = 'hjk.png'
image = client.upload_from_path(path)

print("Image was posted!")
print("You can find it here: {0}".format(image['link']))

