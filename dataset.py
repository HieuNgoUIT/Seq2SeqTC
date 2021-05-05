#from datasets import load_dataset
from transformers import BertTokenizer
import torch
from torch.utils.data import Dataset
import numpy as np
import pandas as pd
import json
from tqdm import tqdm
class TCDataset(Dataset):
    def __init__(self, src_file, trg_file):
        self.data = self.create_data(src_file, trg_file)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

    def __len__(self):
        return len(self.src_data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        sample = self.process_data_to_model_inputs(self.data.iloc[idx,:])
        return sample



    def create_data(self, src_file, trg_file):
        src = []
        trg = []
        with open(src_file, 'r') as f:
            for line in f:
                src.append(line.strip())
        with open(trg_file, 'r') as f:
            for line in f:
                trg.append(line.strip())
        return pd.Series({"src" : src, "trg": trg})

def process_data_to_model_inputs(tokenizer, src_list, trg_list):
    # tokenize the inputs and labels
    inputs = tokenizer(src_list, padding="max_length", truncation=True, max_length=512)
    outputs = tokenizer(trg_list, padding="max_length", truncation=True, max_length=512)

    result = {}
    result["input_ids"] = inputs.input_ids
    result["attention_mask"] = inputs.attention_mask
    result["decoder_input_ids"] = outputs.input_ids
    result["decoder_attention_mask"] = outputs.attention_mask
    result["labels"] = outputs.input_ids.copy()

    # because BERT automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`.
    # We have to make sure that the PAD token is ignored
    result["labels"] = [-100 if token == tokenizer.pad_token_id else token for token in result["labels"]]
    return result

def tokenize_txt_to_csv(src_path, trg_path, output_json):
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    src = []
    with open(src_path, 'r') as f:
        for line in f:
            src.append(line.strip())
    trg = []
    with open(trg_path, 'r') as f:
        for line in f:
            trg.append(line.strip())
    with open(output_json, 'w') as fp:
        for s, t in tqdm(zip(src,trg)):
            json_object = process_data_to_model_inputs(tokenizer, s, t)
            temp = str(json_object).replace("\'","\"") + "\n"
            fp.write(temp)

tokenize_txt_to_csv("src_valid.txt", "trg_valid.txt", "train.json")


