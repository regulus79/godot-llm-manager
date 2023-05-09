extends Node


@onready var udp = PacketPeerUDP.new()
signal text_generated
@export var ip="127.0.0.1"
@export var port=4242
# Called when the node enters the scene tree for the first time.
func _ready():
	var errno=udp.connect_to_host(ip,port)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if udp.get_available_packet_count()>0:
		emit_signal("text_generated",udp.get_packet().get_string_from_utf8())

func request_generation(request):
	udp.put_packet(JSON.stringify(request).to_utf8_buffer())
	
