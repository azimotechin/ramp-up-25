import socket
def get_domain(ip_address):
	return socket.gethostbyaddr(ip_address)[0]