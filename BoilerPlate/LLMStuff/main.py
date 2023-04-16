import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Load the Dolly-v2-12b model and tokenizer
model_name = "databricks/dolly-v2-12b"
tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Define the instruction generation pipeline
class InstructionTextGenerationPipeline(pipeline.Pipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, instructions: str, **kwargs):
        # Tokenize the input instructions
        inputs = self.tokenizer(instructions, return_tensors="pt", truncation=True, max_length=512)

        # Generate text based on the instructions
        outputs = self.model.generate(
            input_ids=inputs.input_ids.to(self.device),
            attention_mask=inputs.attention_mask.to(self.device),
            **kwargs,
        )

        # Decode the generated text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return generated_text

# Create the instruction generation pipeline
generate_text = InstructionTextGenerationPipeline(model=model, tokenizer=tokenizer, device=0)

# Generate text based on input instructions
instructions = "Explain to me the difference between nuclear fission and fusion."
generated_text = generate_text(instructions)

print(generated_text)