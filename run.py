from transformers import EncoderDecoderModel, BertTokenizer, Seq2SeqTrainer, Seq2SeqTrainingArguments
import torch
from torch.utils.data import Dataset, DataLoader

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
tokenizer.bos_token = tokenizer.cls_token
tokenizer.eos_token = tokenizer.sep_token

batch_size=4  # change to 16 for full training
encoder_max_length=512
decoder_max_length=512

mytestdata = {
    "src": ["xin chafo viet nam", "xin chafo casc ban"],
    "trg": ["xin chào việt nam ", "xin chào các bạn "]
}


def process_data_to_model_inputs(batch):
  # tokenize the inputs and labels
  inputs = tokenizer(batch["src"], padding="max_length", truncation=True, max_length=encoder_max_length)
  outputs = tokenizer(batch["trg"], padding="max_length", truncation=True, max_length=decoder_max_length)

  batch["input_ids"] = torch.IntTensor(inputs.input_ids)
  batch["attention_mask"] = torch.IntTensor(inputs.attention_mask)
  batch["decoder_input_ids"] = torch.IntTensor(outputs.input_ids)
  batch["decoder_attention_mask"] = torch.IntTensor(outputs.attention_mask)
  batch["labels"] = torch.IntTensor(outputs.input_ids.copy())

  # because BERT automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`. 
  # We have to make sure that the PAD token is ignored
  batch["labels"] = torch.IntTensor([[-100 if token == tokenizer.pad_token_id else token for token in labels] for labels in batch["labels"]])

  batch.pop('src', None)
  batch.pop('trg', None)

  return batch

temp = process_data_to_model_inputs(mytestdata)


class CustomImageDataset(Dataset):
    def __init__(self):
        self.data = temp

    def __len__(self):
        return len(self.data['input_ids'])

    def __getitem__(self, idx):
        return self.data["input_ids"][idx],  self.data["labels"][idx]


bert2bert = EncoderDecoderModel.from_encoder_decoder_pretrained('bert-base-multilingual-cased', 'bert-base-multilingual-cased') # initialize Bert2Bert from pre-trained checkpoints



# set special tokens
bert2bert.config.decoder_start_token_id = tokenizer.bos_token_id
bert2bert.config.eos_token_id = tokenizer.eos_token_id
bert2bert.config.pad_token_id = tokenizer.pad_token_id

# sensible parameters for beam search
bert2bert.config.vocab_size = bert2bert.config.decoder.vocab_size
bert2bert.config.max_length = 142
bert2bert.config.min_length = 56
bert2bert.config.no_repeat_ngram_size = 3
bert2bert.config.early_stopping = True
bert2bert.config.length_penalty = 2.0
bert2bert.config.num_beams = 4



training_args = Seq2SeqTrainingArguments(
    output_dir="./",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    predict_with_generate=True,
    do_train=True,
    do_eval=True,
    logging_steps=2,  # set to 1000 for full training
    save_steps=16,  # set to 500 for full training
    eval_steps=4,  # set to 8000 for full training
    warmup_steps=1,  # set to 2000 for full training
    max_steps=16, # delete for full training
    overwrite_output_dir=True,
)
from datasets import Dataset
dataset = Dataset.from_dict(temp)

#train_data = CustomImageDataset()



trainer = Seq2SeqTrainer(
    model=bert2bert,
    args=training_args,
    #compute_metrics=compute_metrics,
    train_dataset=dataset,
    #eval_dataset=val_data,
)

trainer.train()