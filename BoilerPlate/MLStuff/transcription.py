from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import torch
 
# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
     
# load dummy dataset and read soundfiles
ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")

# print number of files in the dataset
print(f"Number of files in dataset: {len(ds)}")

# process each audio file in the dataset
for i in range(len(ds)):
    # tokenize
    input_values = processor(ds[i]["audio"]["array"], return_tensors="pt", padding="longest").input_values

    # retrieve logits
    logits = model(input_values).logits

    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    
    # print transcription
    print(transcription)
