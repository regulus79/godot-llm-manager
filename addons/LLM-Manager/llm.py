import socket
import json
from llm_manager_model import generate

print("Loaded model.")

HOST="127.0.0.1"
PORT=4242

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))

print("Setup server. Listening...")

while True:
    message, addr = s.recvfrom(1024)
    
    generation_args=json.loads(message.decode("utf-8"))
    if not "gradual_return" in generation_args:
        generation_args["gradual_return"]=False
        
    print(generation_args)

    for i in generate(**generation_args):
        print(addr,i)
        s.sendto(i.encode("utf-8"),addr)
    if generation_args["gradual_return"]:
        s.sendto("<eos>".encode("utf-8"),addr)
