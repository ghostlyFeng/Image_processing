import json
import glob
import numpy as np
import pickle
from PIL import Image

def trans_pickle(json_path):
    for json_data in json_path:
        f = open(json_data,'r')
        r_json = json.load(f)
        name =json_data.replace('jsons',"images").replace('json','jpeg')
        image=Image.open(name)
        coord = []
        for i in r_json:
            if i['remark']!='/':
                label = i['remark']
            else:
                x0,y0,x1,y1 = map(int,[i['x1'],i['y1'],i['x2'],i['y2']])
                coord.append([x0,y0,x1,y1])
        if len(label)==len(coord):
            coord = np.array(coord)
            pickle_name = json_data.replace('jsons',"dataset").replace('json','pickle')
            print(pickle_name)
            with open(pickle_name,'wb') as f:
                f.write(pickle.dumps((image,coord,label)))
        else:
            print(json_data)
json_path = glob.glob("jsons/*.json")
trans_pickle(json_path)