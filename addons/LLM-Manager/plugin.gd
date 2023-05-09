@tool
extends EditorPlugin


func _enter_tree():
	add_custom_type("LLMManager","Node",preload("LLMManager.gd"),preload("icon.png"))
	# Initialization of the plugin goes here.
	pass


func _exit_tree():
	remove_custom_type("LLMManager")
	# Clean-up of the plugin goes here.
	pass
