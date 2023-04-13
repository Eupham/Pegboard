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

def summarize(text, max_length=100):
    result = summarizer(text, max_length=max_length, min_length=30, do_sample=False, num_beams=4)
    summary = result[0]["summary_text"]
    return summary

# Example usage:
web_scrape = "Your web scrape text here..."
summary = summarize(web_scrape)
print(summary)
