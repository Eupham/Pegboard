from transformers import pipeline

# Define the model name
model_name = "OpenAssistant/stablelm-7b-sft-v7-epoch-3"

# Create the pipeline for text generation
chatbot = pipeline("text-generation", model=model_name, tokenizer=model_name)

# Define the prompt
prompt = "Hello, how are you today?"

# Generate the response
response = chatbot(prompt, max_length=50, do_sample=True)

# Print the response
print(response[0]['generated_text'])
