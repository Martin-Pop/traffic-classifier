import statistics


def calculate_features(buffer, target_ip):
    """
    Calculated features for current buffer (one window).
    :param buffer: buffer with features
    :param target_ip: target ip
    :return: dictionary with features
    """

    total_packets = len(buffer)
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

    for pkt in buffer:
        sizes.append(pkt['length'])

        current_time = pkt['time']
        if last_time is not None:
            iats.append(current_time - last_time)
        last_time = current_time

        if pkt['is_tcp']:
            tcp_count += 1
        elif pkt['is_udp']:
            udp_count += 1

        if pkt['dst_ip'] == target_ip:
            in_packets += 1
            in_bytes += pkt['length']
        elif pkt['src_ip'] == target_ip:
            out_packets += 1
            out_bytes += pkt['length']

    total_bytes = sum(sizes)

    size_mean = statistics.mean(sizes)
    size_std = statistics.stdev(sizes) if len(sizes) > 1 else 0.0

    iat_mean = statistics.mean(iats) if iats else 0.0
    iat_std = statistics.stdev(iats) if len(iats) > 1 else 0.0
    iat_max = max(iats) if iats else 0.0

    return {
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