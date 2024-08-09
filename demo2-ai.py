from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load GPT-2 tokenizer and model
gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')

# Define input text
input_text = "Your input text here"

# Tokenize input text
input_ids = gpt2_tokenizer.encode(input_text, return_tensors='pt')

# Create attention mask (1s for actual tokens, no padding tokens in this example)
attention_mask = torch.ones_like(input_ids)

# Generate text
output = gpt2_model.generate(
    input_ids=input_ids,
    attention_mask=attention_mask,  # Pass the attention mask
    max_length=50,
    num_return_sequences=1,
    pad_token_id=gpt2_tokenizer.eos_token_id  # Use EOS token ID as pad_token_id
)

# Decode the generated text
generated_text = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)

print(generated_text)
