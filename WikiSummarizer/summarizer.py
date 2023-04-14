#Citing the current model
# @misc {peter_szemraj_2022,
#     author       = { {Peter Szemraj} },
#     title        = { long-t5-tglobal-base-16384-book-summary (Revision 4b12bce) },
#     year         = 2022,
#     url          = { https://huggingface.co/pszemraj/long-t5-tglobal-base-16384-book-summary },
#     doi          = { 10.57967/hf/0100 },
#     publisher    = { Hugging Face }
# }

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model_name = "pszemraj/long-t5-tglobal-base-16384-book-summary"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

summarizer = pipeline(
    "summarization",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
)

def summarize_text(text, max_length=100):
    result = summarizer(text, max_length=max_length, min_length=30, do_sample=False, num_beams=4)
    summary = result[0]["summary_text"]
    return summary

input_text = """Your input text here..."""
summary = summarize_text(input_text)
print(summary)
