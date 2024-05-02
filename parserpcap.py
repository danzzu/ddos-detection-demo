import numpy 
import pandas
import pyshark

"""pcap_dataframe
    
    The following function will parse the file with extension .pcap into Panda DataFrame.
    With the help of PyShark, we can dissect the packet's frame information for :
        Time Stamp
        Source IP Address
        Destination IP Address
        Size of the Packet
        Protocols
        
    Only use with IPv4 pcap files, otherwise source or destination will not be found.
    
"""
def pcap_dataframe(in_pcap, limit=None) -> pandas.DataFrame:
    # If specified limits to stop at certain amount of packets.
    counter = 0
    # Import pcap to read all packets
    packets = pyshark.FileCapture(in_pcap)
    
    # The columns     
    source = []
    destination = []
    lengths = []
    protocols = []
    duration_nsec = []
    duration_sec = []
    
    for packet in packets :
        # Limit specified then we're only noted down this amount of packets
        if limit is not None and counter == limit :
            break;
        
        #Source IP Addresses
        source.append(packet.ip.src)
        
        # Destination IP Addresses
        destination.append(packet.ip.dst)
        
        # Bytes of packet is represented by lengths
        lengths.append(packet.length)
        
        # Convert the time delta to nanosecond. 
        time_delta_sec = int(float(packet.frame_info.time_delta))
        duration_sec.append(time_delta_sec)
        time_delta_nsec = int((float(packet.frame_info.time_delta) - time_delta_sec) * 1e+9)
        duration_nsec.append(time_delta_nsec)
        
        # The protocol of the packet ICMP/UDP/TCP
        protocols.append(str(packet.ip.proto.showname_value.split('(')[0]).strip())
        
        #Increment for packet counts
        counter += 1
    packets.close()
    
    duration_nsec = numpy.array(duration_nsec)
    
    # All traffics in Dictionary
    traffics = {
        "src" : source,
        "dst" : destination,
        "bytes" : lengths,
        "dur_nsec" : duration_nsec,
        "Protocol" : protocols
    }
    
    # Return the Panda DataFrame of the Traffic.
    return pandas.DataFrame(traffics)


# # Pcap file name
# pcap_file = 'home_traffic.pcap'
# # Read the pcap file and put it into a DataFrame
# pcap_data = pcap_dataframe(pcap_file, limit=100)
# print(pcap_data.head())

