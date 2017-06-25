import pandas as pd
import numpy
import os
import tldextract

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, 'data')


class Model(object):

    def __init__(self):
        
        bs = pd.read_json(data_dir + "/sources_credibility.json").T.reset_index()
        bs = bs.rename(columns={"index": "site_url", "2nd type": "type2", "3rd type": "type3"})
        bs["type"] = bs["type"].apply(lambda x: x.strip())
        bs["type2"] = bs["type2"].apply(lambda x: x.strip())
        bs["type3"] = bs["type3"].apply(lambda x: x.strip())

        bs["type_"] = bs.apply(lambda x: "0" if (x["type"]=="credible" or x["type2"]=="credible" or x["type3"]=="credible") else 0, axis=1)
        bs["type_"] = bs.apply(lambda x: "0" if (x["type"]=="state" or x["type2"]=="state" or x["type3"]=="state") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.1" if (x["type"]=="political" or x["type2"]=="political" or x["type3"]=="political") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.5" if (x["type"]=="satire" or x["type2"]=="satire" or x["type3"]=="satire") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.5" if (x["type"]=="unknown" or x["type2"]=="unknown" or x["type3"]=="unknown") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.7" if (x["type"]=="bias" or x["type2"]=="bias" or x["type3"]=="bias") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.7" if (x["type"]=="bais" or x["type2"]=="bais" or x["type3"]=="bais") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.8" if (x["type"]=="junksci" or x["type2"]=="junksci" or x["type3"]=="junksci") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.8" if (x["type"]=="hate" or x["type2"]=="hate" or x["type3"]=="hate") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.8" if (x["type"]=="clickbait" or x["type2"]=="clickbait" or x["type3"]=="clickbait") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.9" if (x["type"]=="conspiracy" or x["type2"]=="conspiracy" or x["type3"]=="conspiracy") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "0.9" if (x["type"]=="rumor" or x["type2"]=="rumor" or x["type3"]=="rumor") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "1" if (x["type"]=="unreliable" or x["type2"]=="unreliable" or x["type3"]=="unreliable") else x["type_"], axis=1)
        bs["type_"] = bs.apply(lambda x: "1" if (x["type"]=="fake" or x["type2"]=="fake" or x["type3"]=="fake") else x["type_"], axis=1)

        bs["site_url"] = bs["site_url"].apply(lambda x: x.replace(".com", "").replace(".net", "").replace(".info", "").replace(".tv", "").replace(".org", ""))
        bs["site_url"] = bs["site_url"].apply(lambda x: x.replace(".co.uk", "").replace(".wordpress", "").replace(".press", "").replace(".news", "").replace(".biz", ""))

        bs.drop(["type"], axis=1, inplace=True)
        bs = bs.rename(columns={"type_": "type"})
        bs = bs[["site_url", "type"]]

        self.bs = bs
    
    def predict(self, js):
        
        url = js['url']
        
        result = self.bs[self.bs["site_url"] == tldextract.extract(url).domain]
        if len(result) == 0:
            result = 0
        else:
            result = float(result['type'].values[0])
        
        return result