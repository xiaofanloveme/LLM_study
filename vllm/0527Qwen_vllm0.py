from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import os
#import torch
import time
from vllm import LLM, SamplingParams
os.environ["CUDA_VISIBLE_DEVICES"] = "4,5,6,7"
#model_id = "/mnt/geogpt-gpfs/llm-course/public/models/command-r-plus"
model_id = "/mnt/geogpt-gpfs/llm-course/public/models/Qwen-7B" 
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code = True)
with open('user_messages2.json', 'r') as file:
    data = json.load(file)
    prompts = data['prompts']

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, min_tokens = 50, max_tokens = 400)

start_time = time.time()
total_tokens = 0

llm = LLM(model = model_id, trust_remote_code = True, gpu_memory_utilization = 0.9)
outputs = llm.generate(prompts, sampling_params)
output_file_path = "generated_messages0527_Qwen7B.json"

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    
    gen_tokens_encoded = tokenizer.encode(generated_text, add_special_tokens=False)
    token_count = len(gen_tokens_encoded)
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}, Generated tokens: {token_count!r}")
    total_tokens += token_count
    data_to_save = {"user_message": prompt, "model_response": generated_text, "token_count": token_count}
    f.write(json.dumps(data_to_save, ensure_ascii = False) + "\n")


end_time = time.time()
execution_time = (end_time - start_time)/60
s = total_tokens/(end_time - start_time)
print(f"Script execution time: {execution_time:.2f} minutes")
print(f"Total number of tokens: {total_tokens}")
print(f"tokens response per second: {s}")
print("Program Done !")