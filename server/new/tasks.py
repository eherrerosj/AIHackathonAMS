import time
import json
import newspaper
import pandas
import numpy
import tldextract


def get_content(url):
   a = Article(url, language='en')
   a.download()
   a.parse()
   return u''.join(a.text).encode('utf-8').strip()

def check_url(js, model):

    url = js['url']

    # Commented for now TODO do something here
    # content = get_content(url)
    # content = url

    confidence = model.predict(js)


    res = json.dumps({
        'id': js['id'],
        'fake': True if confidence > 0.5 else False,
        'confidence': confidence
    })

    return res # Dummy return val until connection to model is established