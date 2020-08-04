import json
from espnet.utils.training.batchfy import make_batchset
from espnet.utils.dataset import TransformDataset
from espnet.asr.pytorch_backend.asr import CustomConverter
from espnet.utils.io_utils import LoadInputsAndTargets
import numpy as np
import itertools 
from tqdm import tqdm

def data_prepare(train_feature):

    converter = CustomConverter(subsampling_factor=1)
    train = make_batchset(train_feature,batch_size=len(train_feature))
    name=[train[0][i][0] for i in range(len(train_feature))]
    load_tr = LoadInputsAndTargets(
        mode="asr",
        load_output=True,
        preprocess_conf=None,
        preprocess_args={"train": True},  # Switch the mode of preprocessing
        )
    dataset = TransformDataset(train, lambda data: converter([load_tr(data)]))
    return dataset, name


def savetodic(jsonpath,dic):
    with open(jsonpath, "rb") as f:
        train_feature = json.load(f)["utts"]
    dataset, name=data_prepare(train_feature)

    for i in tqdm(range(len(name))):
        ilen = dataset[0][1][i]
        y = dataset[0][2][i]
        dic[name[i]]=[ilen,y]
    
    return dic

if __name__ == "__main__":
    dic={}
    jsonpath1='./data_test.json'
    jsonpath2='./data_train_dev.json'
    jsonpath3='./data_train_nodev.json'

    dic=savetodic(jsonpath1,dic)
    dic=savetodic(jsonpath2,dic)
    dic=savetodic(jsonpath3,dic)

    np.save('file_y.npy', dic) 
   

