import pyshark

cap = pyshark.FileCapture('flag.pcap',display_filter="icmp")
codes = []

for c in cap:
	for pkt in c:
		if pkt.layer_name == 'icmp':
			print(pkt.type)
		if pkt.layer_name == 'ip':
			print(pkt.ttl)
			codes.append(pkt.ttl,)
print(codes)
with open('flag2.txt','w') as f:
	for k in codes:
		s=hex(int(k))[2:]
		if len(s) ==1:
			s='0'+s
		f.write(s)
print(123)