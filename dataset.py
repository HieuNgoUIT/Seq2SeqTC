#from datasets import load_dataset
from transformers import BertTokenizer
import torch
from torch.utils.data import Dataset
import numpy as np
import pandas as pd
import json
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

#dataset = TCDataset("temp_text.txt", "temp_text2.txt")
#print(dataset[[1,2]])


def process_data_to_model_inputs(tokenizer, src_list, trg_list):
    # tokenize the inputs and labels
    inputs = tokenizer(src_list, padding="max_length", truncation=True, max_length=128)
    outputs = tokenizer(trg_list, padding="max_length", truncation=True, max_length=128)

    result = {}
    result["input_ids"] = inputs.input_ids
    result["attention_mask"] = inputs.attention_mask
    result["decoder_input_ids"] = outputs.input_ids
    result["decoder_attention_mask"] = outputs.attention_mask
    result["labels"] = outputs.input_ids.copy()

    # because BERT automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`.
    # We have to make sure that the PAD token is ignored
    result["labels"] = [[-100 if token == tokenizer.pad_token_id else token for token in labels] for labels in
                       result["labels"]]
    return result

def tokenize_txt_to_csv(path):
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    src = []
    with open(path, 'r') as f:
        for line in f:
            src.append(line.strip())
    trg = []
    with open(path, 'r') as f:
        for line in f:
            trg.append(line.strip())
    result = process_data_to_model_inputs(tokenizer, src, trg)
    with open('result.json', 'w') as fp:
        json.dump(result, fp)
    #pd.DataFrame(result).to_csv("test.csv", index=False)

tokenize_txt_to_csv("temp_text.txt")


#
# tokenizer.bos_token = tokenizer.cls_token
# tokenizer.eos_token = tokenizer.sep_token
# batch_size=2  # change to 16 for full training
# encoder_max_length=512
# decoder_max_length=512
#
#
#
# bert2bert = EncoderDecoderModel.from_encoder_decoder_pretrained('bert-base-multilingual-cased', 'bert-base-multilingual-cased') # initialize Bert2Bert from pre-trained checkpoints
#
#
# # set special tokens
# bert2bert.config.decoder_start_token_id = tokenizer.bos_token_id
# bert2bert.config.eos_token_id = tokenizer.eos_token_id
# bert2bert.config.pad_token_id = tokenizer.pad_token_id
#
# # sensible parameters for beam search
# bert2bert.config.vocab_size = bert2bert.config.decoder.vocab_size
# bert2bert.config.early_stopping = True
#
#
# training_args = Seq2SeqTrainingArguments(
#     output_dir="./",
#     per_device_train_batch_size=batch_size,
#     per_device_eval_batch_size=batch_size,
#     predict_with_generate=True,
#     do_train=True,
#     do_eval=True,
#     logging_steps=1000,  # set to 1000 for full training
#     save_steps=500,  # set to 500 for full training
#     eval_steps=8000,  # set to 8000 for full training
#     warmup_steps=2000,  # set to 2000 for full training
#     overwrite_output_dir=True,
# )
#
# trainer = Seq2SeqTrainer(
#     model=bert2bert,
#     args=training_args,
#     #compute_metrics=metric,
#     train_dataset=dataset,
#     #eval_dataset=valid_data,
# )
#
# trainer.train()
#
