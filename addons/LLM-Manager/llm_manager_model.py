from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import torch.nn.functional as F
import configparser

parser=configparser.ConfigParser()
parser.read("model.cfg")
model_name=parser["model"]["name"]
print(f"Using model: {model_name}")

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def generate(init_prompt="",max_history=100,delimiter=None,max_length=10,temperature=0,punish_repetition=0,return_only_new=True,gradual_return=False):
    inputs = tokenizer(init_prompt, return_tensors="pt")

    totaltokens=[]
    new_tokens=[]
    for i in inputs.input_ids.squeeze(0):
        totaltokens.append(i.item())
    
    delimiter_tokens=tokenizer(delimiter, return_tensors="pt").input_ids if delimiter else []
    #print(delimiter_tokens)

    for i in range(max_length):
        tokens=totaltokens[-max_history:]
        with torch.no_grad():
            logits=model(input_ids=torch.tensor([tokens,])).logits.squeeze(0)[-1]
        predicted_class_id=None
        
        #repetition penalty is WIP 
        if punish_repetition!=0:
            for i in set(new_tokens):
                #print("test",i,logits[i],logits[i+1],(punish_repetition**tokens.count(i)))
                logits[i]-=punish_repetition*tokens.count(i)
        if temperature==0:
            predicted_class_id=logits.argmax().item()
        else:
            logits=F.softmax(logits/temperature, dim=-1)
            predicted_class_id=torch.multinomial(logits,1).item()
        
        #print(i,predicted_class_id)
        
        if predicted_class_id in delimiter_tokens:
            print("delimiter reached")
            break
        
        if gradual_return:
            yield tokenizer.decode(predicted_class_id)

        totaltokens.append(predicted_class_id)
        new_tokens.append(predicted_class_id)

    if not gradual_return:
        if return_only_new:
            yield tokenizer.decode(new_tokens)
        else:
            yield tokenizer.decode(totaltokens)
