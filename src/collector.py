import sys
import os
from scapy.all import sniff, wrpcap

def collect_packets(interface, duration_seconds, filepath):
    try:
        packets = sniff(iface=interface, timeout=duration_seconds) # internally handles KeyboardInterrupt as early successfull exit
        
        if len(packets) > 0:
            wrpcap(filepath, packets)
            return len(packets)
        else:
            return 0

    except KeyboardInterrupt:
        raise
    except Exception:
        return 0