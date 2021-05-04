from transformers import EncoderDecoderModel, BertTokenizer
import torch
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
# model = EncoderDecoderModel.from_encoder_decoder_pretrained('bert-base-multilingual-cased', 'bert-base-multilingual-cased') # initialize Bert2Bert from pre-trained checkpoints
# # forward
input_ids = torch.tensor(tokenizer.encode("Xin chaof casc bạn", add_special_tokens=True)).unsqueeze(0)  # Batch size 1
# outputs = model(input_ids=input_ids, decoder_input_ids=input_ids)
# # training
# outputs = model(input_ids=input_ids, decoder_input_ids=input_ids, labels=input_ids)
# loss, logits = outputs.loss, outputs.logits
# # save and load from pretrained
# model.save_pretrained("bert2bert")
model = EncoderDecoderModel.from_pretrained("checkpoint-70500")
# generation
generated = model.generate(input_ids, decoder_start_token_id=model.config.decoder.pad_token_id)
print(generated)





















# from transformers import EncoderDecoderModel, BertTokenizer, EncoderDecoderConfig
# import torch

# tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
# encoder_decoder_config = EncoderDecoderConfig.from_pretrained('checkpoint-70500/config.json')
# model = EncoderDecoderModel.from_pretrained("checkpoint-70500/pytorch_model.bin", config=encoder_decoder_config)


# input_ids = torch.tensor(tokenizer.encode("Hello, my dog is cute", add_special_tokens=True)).unsqueeze(0)  # Batch size 1
# outputs = model(input_ids=input_ids, decoder_input_ids=input_ids)

# # training
# outputs = model(input_ids=input_ids, decoder_input_ids=input_ids, labels=input_ids)
# loss, logits = outputs.loss, outputs.logits


# # save and load from pretrained
# model.save_pretrained("bert2bert")
# model = EncoderDecoderModel.from_pretrained("bert2bert")

# # forward
# #input_ids = torch.tensor(tokenizer.encode("Vậy mà tình trạng hiện nay lại là số ít cần nhưng số đông chưa vội.", add_special_tokens=True)).unsqueeze(0)  # Batch size 1
# #outputs = model(input_ids=input_ids, decoder_input_ids=input_ids)

# # generation
# generated = model.generate(input_ids, decoder_start_token_id=model.config.decoder.pad_token_id)