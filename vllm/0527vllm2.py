from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import json
import os
#import torch
import time
from vllm import LLM, SamplingParams
os.environ["CUDA_VISIBLE_DEVICES"] = "4,5,6,7"
#model_id = "/mnt/geogpt-gpfs/llm-course/public/models/command-r-plus"
model_id = "/mnt/geogpt-gpfs/llm-course/public/models/Qwen-7B" 
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code = True)

user_messages_file = "user_messages2.json"


sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
start_time = time.time()
llm = LLM(model = model_id, trust_remote_code = True, gpu_memory_utilization = 0.9)

output_file_path = "generated_messages_0524_vllm.json"

prompts = user_messages_file
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

#f.write(json.dumps(data_to_save, ensure_ascii = False) + "\n")
end_time = time.time()
execution_time = (end_time - start_time)/60

print(f"Script execution time: {execution_time:.2f} minutes")
print("Program Done !")