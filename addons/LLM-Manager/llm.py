import socket
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import torch.nn.functional as F

device="cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained("facebook/opt-350m")
model.to(device)
tokenizer = AutoTokenizer.from_pretrained("facebook/opt-350m")

def generate(kwargs):
    max_new_tokens=kwargs["max_new_tokens"] if "max_new_tokens" in kwargs else 10
    

    for i in kwargs:
        if isinstance(kwargs[i], str):
            tokens=tokenizer(kwargs[i],return_tensors="pt").input_ids
            print(tokens)
            kwargs[i] = tokens
    print(kwargs)
    try:
        if "gradual_return" in kwargs and kwargs["gradual_return"]==True:
            print("yes gradual return")
            kwargs["max_new_tokens"]=1
            del kwargs["gradual_return"]
            for i in range(max_new_tokens):
                print(i)
                new_token=model.generate(**kwargs)[0][-1]
                if new_token.item() == kwargs["eos_token_id"]:
                    print("delimiter reached")
                    break
                tmp_input_ids=kwargs["input_ids"].squeeze(0).tolist()
                tmp_input_ids.append(new_token)
                kwargs["input_ids"]=torch.tensor(tmp_input_ids).unsqueeze(0)
                yield tokenizer.decode(new_token,skip_special_tokens=True)
        else:
            print("no gradual return")
            del kwargs["gradual_return"]
            original_length=len(kwargs["input_ids"][0])
            outputs=model.generate(**kwargs)
            print(outputs)
            print(outputs[0][original_length:])
            yield tokenizer.decode(outputs[0][original_length:],skip_special_tokens=True)
    except Exception as e:
        print(e)

print("Loaded model.")

HOST="127.0.0.1"
PORT=4242

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))

print("Setup server. Listening...")

while True:
    message, addr = s.recvfrom(1024)
    
    generation_args=json.loads(message.decode("utf-8"))
    print(generation_args)

    for i in generate(generation_args):
        print(addr,i)
        s.sendto(i.encode("utf-8"),addr)
    s.sendto("<eos>".encode("utf-8"),addr)
