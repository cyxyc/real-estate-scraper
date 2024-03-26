
from imgurpython import ImgurClient
import csv
import ast

client_id = 'your-client-id'
client_secret = 'your-client-secret'

client = ImgurClient(client_id, client_secret)

with open('df2.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        image_urls = ast.literal_eval(row[5])  # Parse the string of image URLs into a list
        for url in image_urls:
            response = client.upload_from_url(url, config=None, anon=True)
            print('Imgur URL: ', response['link'])