from transformers import EncoderDecoderModel, BertTokenizer, Seq2SeqTrainer, Seq2SeqTrainingArguments
import torch
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset, Features, Value, ClassLabel, Sequence
#from datasets import load_metric

#metric = load_metric('glue')

# _features = Features(
#     {
#         "input_ids": Value("int64"),
#         "attention_mask": Value("int64"),
#         "decoder_input_ids": Value("int64"),
#         "decoder_attention_mask": Value("int64"),
#         "labels": Value("int64"),
#     }
# )
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

train_data = load_dataset('json', data_files='train.json', split="train")
#valid_data = load_dataset('json', data_files='valid.json', split="vali")
train_data.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)
#valid_data.set_format(
#    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
#)

batch_size=4  # change to 16 for full training
bert2bert = EncoderDecoderModel.from_encoder_decoder_pretrained('bert-base-multilingual-cased', 'bert-base-multilingual-cased') # initialize Bert2Bert from pre-trained checkpoints

bert2bert.config.decoder_start_token_id = tokenizer.bos_token_id
bert2bert.config.eos_token_id = tokenizer.eos_token_id
bert2bert.config.pad_token_id = tokenizer.pad_token_id

bert2bert.config.vocab_size = bert2bert.config.decoder.vocab_size
bert2bert.config.early_stopping = True

training_args = Seq2SeqTrainingArguments(
    output_dir="./",
    per_device_train_batch_size=batch_size,
    #per_device_eval_batch_size=batch_size,
    predict_with_generate=True,
    do_train=True,
    #do_eval=True,
    logging_steps=1000,  # set to 1000 for full training
    save_steps=500,  # set to 500 for full training
    eval_steps=8000,  # set to 8000 for full training
    warmup_steps=2000,  # set to 2000 for full training
    overwrite_output_dir=True,
)

trainer = Seq2SeqTrainer(
    model=bert2bert,
    args=training_args,
    #compute_metrics=metric,
    train_dataset=train_data,
    #eval_dataset=valid_data,
)

trainer.train()