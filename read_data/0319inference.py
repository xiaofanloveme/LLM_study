from hf_olmo import * # registers the Auto* classes

from transformers import AutoModelForCausalLM, AutoTokenizer

#olmo = AutoModelForCausalLM.from_pretrained("allenai/OLMo-7B")
#tokenizer = AutoTokenizer.from_pretrained("allenai/OLMo-7B")
olmo = AutoModelForCausalLM.from_pretrained("/home/wrf1/OLMo/save_sft/step157-unsharded")
tokenizer = AutoTokenizer.from_pretrained("/home/wrf1/OLMo/save_sft/step157-unsharded")

#message = ["Language modeling is "]
message = ["New york is a big city "]
inputs = tokenizer(message, return_tensors='pt', return_token_type_ids=False)
response = olmo.generate(**inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
print(tokenizer.batch_decode(response, skip_special_tokens=True)[0])