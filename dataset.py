from datasets import load_dataset
from transformers import BertTokenizer
import torch
from torch.utils.data import Dataset
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')


class TCDataset(Dataset):
    def __init__(self, src_file, trg_file, transform=None):
        self.src_data = self.yield_data(src_file)
        self.trg_data = self.yield_data(trg_file)
        self.transform = transform

    def __len__(self):
        return len(self.src_data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        sample = {"src": self.src_data[idx], "trg": self.trg_data[idx]}
        if self.transform:
            sample = self.transform(sample)
        return sample

    def yield_data(self, path):
        lines = []
        with open(path, 'r') as f:
            for line in f:
                lines.append(line)
        return lines                



dataset = TCDataset("temp_text.txt", "temp_text2.txt")
print(dataset[[0,1]])












#train_data = load_dataset('text', data_files={'train': ['temp_text.txt', 'temp_text2.txt']}, features = datasets.Features({'src'}))
# valid_data = load_dataset('json', data_files='train.json')

#print('a',train_data)

# batch_size=4
# encoder_max_length=128
# decoder_max_length=128
# def process_data_to_model_inputs(batch):
#   # tokenize the inputs and labels
#   inputs = tokenizer(batch["src"], padding="max_length", truncation=True, max_length=encoder_max_length)
#   outputs = tokenizer(batch["trg"], padding="max_length", truncation=True, max_length=decoder_max_length)

#   batch["input_ids"] = inputs.input_ids
#   batch["attention_mask"] = inputs.attention_mask
#   batch["decoder_input_ids"] = outputs.input_ids
#   batch["decoder_attention_mask"] = outputs.attention_mask
#   batch["labels"] = outputs.input_ids.copy()

#   # because BERT automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`. 
#   # We have to make sure that the PAD token is ignored
#   batch["labels"] = [[-100 if token == tokenizer.pad_token_id else token for token in labels] for labels in batch["labels"]]

#   return batch


# train_data = train_data.map(
#     process_data_to_model_inputs, 
#     batched=True, 
#     batch_size=batch_size, 
#     remove_columns=["src", "trg"]
# )
# train_data.set_format(
#     type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
# )

# valid_data = train_data.map(
#     process_data_to_model_inputs, 
#     batched=True, 
#     batch_size=batch_size, 
#     #remove_columns=["src", "trg"]
# )
# valid_data.set_format(
#     type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
# )

# print(train_data)