from transformers import EncoderDecoderModel, BertTokenizer
import torch
from tqdm import tqdm
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = EncoderDecoderModel.from_pretrained("checkpoint-100000")

with open ("src_train.txt", 'r') as f, open("result.txt",'w') as f2:
    for line in tqdm(f):
        input_ids = torch.tensor(tokenizer.encode(line)).unsqueeze(0) 
        generated = model.generate(input_ids, decoder_start_token_id=model.config.decoder.pad_token_id)
        f2.write(str(tokenizer.decode(generated[0])) + "\n")


