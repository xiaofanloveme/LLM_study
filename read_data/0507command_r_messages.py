from transformers import AutoTokenizer, AutoModelForCausalLM

#model_id = "CohereForAI/c4ai-command-r-v01"
model_id = "/mnt/geogpt-gpfs/llm-course/public/models/command-r-v01"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Format message with the command-r chat template
# messages = [{"role": "user", "content": "Hello, how are you?"}]

# 准备多个用户消息
user_messages = [
    {"role": "user", "content": "Hello, please introduce yourself."},
    {"role": "user", "content": "What is your favorite color?"},
    {"role": "user", "content": "Can you tell me a joke?"},
    # 添加更多的用户消息...
]

# 格式化消息并批量生成回复
for message in user_messages:
    input_ids = tokenizer.apply_chat_template([message], tokenize=True, add_generation_prompt=True, return_tensors="pt")
    gen_tokens = model.generate(
        input_ids, 
        max_new_tokens=100, 
        do_sample=True, 
        temperature=0.3,
    )
    gen_text = tokenizer.decode(gen_tokens[0], skip_special_tokens=True)
    print("User message:", message["content"])
    print("Model response tokens:", gen_tokens[0])
    print("Model response:", gen_text)
    print()