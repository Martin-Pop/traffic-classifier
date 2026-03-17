import csv
import os
from scapy.all import rdpcap, IP, TCP, UDP
import statistics

def calculate_features(chunk, target_ip):
    total_packets = len(chunk)
    if total_packets == 0:
        return None

    in_packets = 0
    out_packets = 0
    in_bytes = 0
    out_bytes = 0
    tcp_count = 0
    udp_count = 0
    sizes = []
    iats = [] 

    last_time = None

    for pkt in chunk:
        sizes.append(len(pkt))
        current_time = float(pkt.time)
        
        if last_time is not None:
            iats.append(current_time - last_time)
        last_time = current_time

        if pkt.haslayer(TCP): tcp_count += 1
        elif pkt.haslayer(UDP): udp_count += 1

        if pkt[IP].dst == target_ip:
            in_packets += 1
            in_bytes += len(pkt)
        elif pkt[IP].src == target_ip:
            out_packets += 1
            out_bytes += len(pkt)

    total_bytes = sum(sizes)

    size_mean = statistics.mean(sizes)
    size_std = statistics.stdev(sizes) if len(sizes) > 1 else 0.0
    
    iat_mean = statistics.mean(iats) if iats else 0.0
    iat_std = statistics.stdev(iats) if len(iats) > 1 else 0.0
    iat_max = max(iats) if iats else 0.0

    return {
        'total_packets': total_packets,
        'in_packets': in_packets,
        'out_packets': out_packets,
        'total_bytes': total_bytes,
        'in_bytes': in_bytes,
        'out_bytes': out_bytes,
        'in_packet_ratio': in_packets / total_packets if total_packets > 0 else 0,
        'in_byte_ratio': in_bytes / total_bytes if total_bytes > 0 else 0,
        'size_mean': round(size_mean, 2),
        'size_std': round(size_std, 2),
        'size_min': min(sizes),
        'size_max': max(sizes),
        'iat_mean': round(iat_mean, 6),
        'iat_std': round(iat_std, 6),
        'iat_max': round(iat_max, 6),
        'tcp_ratio': tcp_count / total_packets if total_packets > 0 else 0,
        'udp_ratio': udp_count / total_packets if total_packets > 0 else 0
    }

def clean_packets(packets, target_ip):
    cleaned = []
    for p in packets:
        if p.haslayer(IP):
            ip_src = p[IP].src
            ip_dst = p[IP].dst

            if ip_src == target_ip or ip_dst == target_ip:
                if not (ip_dst.endswith(".255") or ip_dst.startswith(("224.", "239."))):
                    cleaned.append(p)
    return cleaned

def cut_off_packets(packets):
    if not packets:
        return []

    start_time = float(packets[0].time) + 5.0
    end_time = float(packets[-1].time) - 5.0
    
    return [p for p in packets if start_time <= float(p.time) <= end_time]


def create_sliding_windows(packets, window_size=10.0, step_size=5.0):
    if not packets:
        return []

    windows = []
    start_time = float(packets[0].time)
    end_time = float(packets[-1].time)

    current_window_start = start_time

    while current_window_start + window_size <= end_time:
        current_window_end = current_window_start + window_size
        
        window_packets = [p for p in packets if current_window_start <= float(p.time) < current_window_end]
        windows.append(window_packets)
        current_window_start += step_size

    return windows


def transform_captured_data(category, input_file, output_file, target_ip):
        
    # CLEAN
    raw_packets = rdpcap(input_file)
    cleaned_packets = clean_packets(raw_packets, target_ip)
        
    if len(cleaned_packets) == 0:
        print(f"IP {target_ip} was not found")
        return
    
    # CUT OFF
    trimmed_packets = cut_off_packets(cleaned_packets)

    # SPLIT
    chunked_packets = create_sliding_windows(trimmed_packets, window_size=10.0, step_size=5.0)

    # CALCULATE FEATURES
    rows = []
    prev_total_packets = 0

    for chunk in chunked_packets:
        features = calculate_features(chunk, target_ip)
        
        if features:
            features['prev_total_packets'] = prev_total_packets
            features['label'] = category
            rows.append(features)
            prev_total_packets = features['total_packets']

    if not rows:
        return

    # SAVE
    file_exists = os.path.isfile(output_file)
    
    with open(output_file, mode='a', newline='') as csv_file:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
            
        writer.writerows(rows)