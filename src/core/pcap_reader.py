import os

from scapy.utils import PcapReader
from scapy.layers.inet import IP, TCP, UDP
from collections import deque

from .features import calculate_features


def extract_packet_values(pkt):
    """
    Extracts useful values from scapy object.
    :param pkt: scapy packet
    :return: dictionary with values
    """
    return {
        'time': float(pkt.time),
        'length': len(pkt),
        'is_tcp': pkt.haslayer(TCP),
        'is_udp': pkt.haslayer(UDP),
        'src_ip': pkt[IP].src,
        'dst_ip': pkt[IP].dst
    }

def is_unicast_with_target_ip(pkt, target_ip):
    """
    Checks if a packet is a unicast packet with a target IP.
    :param pkt: scapy packet
    :param target_ip: target IP
    :return: True if packet is a unicast packet with target IP
    """
    if pkt.haslayer(IP):
        src = pkt[IP].src
        dst = pkt[IP].dst

        if src == target_ip or dst == target_ip:
            if not (dst.endswith(".255") or dst.startswith(("224.", "239."))):
                return True

    return False


def extract_features_from_pcap(filepath, target_ip, progress_callback=None):
    """
    Extracts features from a pcap file.
    Uses 20s sliding window with 5s step. Buffer represents the window. When it gets full
    features are calculated and window slides by one step.
    :param filepath: filepath of pcap file
    :param target_ip: target IP
    :return: list of features
    :param progress_callback: callback function, takes in % (int)
    """

    file_size = os.path.getsize(filepath)

    buffer = deque()
    window_start_time = None
    window_end_time = None

    all_features = []

    with PcapReader(filepath) as pcap:
        for pkt in pcap:

            if not is_unicast_with_target_ip(pkt, target_ip):
                continue

            light_pkt = extract_packet_values(pkt)

            if window_start_time is None:
                window_start_time = light_pkt['time']
                window_end_time = window_start_time + 20.0

            # packet is out of bounds here  - calculate features, slide window
            while light_pkt['time'] >= window_end_time:

                if len(buffer) > 0:
                    features = calculate_features(buffer, target_ip)
                    if features:
                        features['timestamp'] = window_start_time
                        all_features.append(features)

                    if progress_callback:
                        current_pos = pcap.f.tell()
                        percentage = int((current_pos / file_size) * 100)
                        progress_callback(percentage)

                window_start_time += 5.0
                window_end_time += 5.0

                while len(buffer) > 0 and buffer[0]['time'] < window_start_time:
                    buffer.popleft()

            buffer.append(light_pkt)

    return all_features