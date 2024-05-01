import pandas 
import pyshark
# from scapy.all import sniff, IP, ICMP, UDP, TCP

# TOO SLOW.
# def pcap_parser(pcap_file_name) -> pandas.DataFrame:
#     read_pcap = sniff(offline=pcap_file_name)
    
#     ip_src = []
#     ip_dst = []
#     bytecount = []
#     ports = []
#     protocols = []
    
#     for packet in read_pcap:
        
#         # IP src & dest column
#         if packet.haslayer(IP) :
#             ip_src.append(packet[IP].src)
#             ip_dst.append(packet[IP].dst)
            
#         # Protocol column
#         if packet.haslayer(TCP):
#             protocols.append("TCP")
#             ports.append(packet[TCP].sport)
#         elif packet.haslayer(UDP):
#             protocols.append("UDP")
#             ports.append(packet[UDP].sport)
#         elif packet.haslayer(ICMP) :
#             protocols.append("ICMP")
#             ports.append(packet[ICMP].sport)
        
#     data = {
#         'src' : ip_src,
#         'dst' : ip_dst,
#         'port_no' : ports,
#         'Protocol' : protocols
#     }
#     df = pandas.DataFrame(data)
#     return df


[TODO]
#.delta -> duration.
#.length
#.no
#ip.src
#ip.dst
#ip.ttl
#ip.srchost
#ip.proto.showname_value.split('(').strip()
#packet[packet.transport_layer].sport
def pcap_dataframe(in_pcap) -> pandas.DataFrame:
    counter = 0
    packets = pyshark.FileCapture(in_pcap)
    
    for packet in packets :
        if counter == 500 :
            break
        
    packets.close()
    
    
    
pcap_dataframe('attack_ddos.pcap')

