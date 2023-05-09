# godot-llm-manager
Harnessing AI in Godot by communicating with a python script running a model from Huggingface.

This project is WIP! It may contain bugs.

## How to use:
Step 0.
Set the model you want to use in the model_config.cfg file. The model must be available on Huggingface, and should be in the format of "organization/modelname", for example: "facebook/opt-350m"

Step 1.
Run the python script called ```llm.py```. This loads the model and starts up the UDP server. In later versions it is planned to have Godot automatically run it, but that is WIP.

Step 2.
Start Godot, and enable this addon.

Step 3.
Add an LLMManager node.

Step 4.
Connect the ```text_generated``` signal from the LLMManager to your script. This signal is called when the python script sends data from the LLM. When gradual_return=true, then it will send "<eos>" when it is finished generating. Otherwise, it will just send the generated text.
For example:
```gdscript
func _on_llm_manager_text_generated(text):
  #If finished with gradual output
  if text=="<eos>":
    #Done generating
  else:
    #Do stuff with the text
```

Step 5.
Call the "request_generation(request)" function on the LLMManager node. 
The argument, "request" is a dictionary containing the following optional parameters:
```gdscript
var request={
	init_prompt="The text to be sent to the LLM",
	temperature=0.5,
	punish_repetition=0.1, # Still WIP
	max_length=100, # Maximum number of tokens to be generated
	max_history=100, # Maximum history (anything longer will be clipped to the most recent N tokens)
	delimiter="\n", # Tokens signaling generation to forcefully stop
	return_only_new=true, #Only return the new tokens generted, else the entire prompt with the new tokens (only matters when gradual_return=false).
	gradual_return=true, # Return in a pipeline-ish manner, or all at once.
}
```
