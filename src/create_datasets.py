import os
import sys

try:
    from src.transform import transform_captured_data
except ImportError:
    from transform import transform_captured_data

def main():
    target_device_ip = "192.168.1.10"
    input_base_dir = "data/raw_pcaps"
    output_base_dir = "data/datasets"

    if not os.path.exists(input_base_dir):
        sys.exit(1)

    os.makedirs(output_base_dir, exist_ok=True)

    for category in os.listdir(input_base_dir):
        category_dir = os.path.join(input_base_dir, category)
        
        if not os.path.isdir(category_dir):
            continue

        output_csv = os.path.join(output_base_dir, f"{category}.csv")
        
        if os.path.exists(output_csv):
            os.remove(output_csv)

        for file_name in os.listdir(category_dir):
            if file_name.endswith(".pcap"):
                input_pcap = os.path.join(category_dir, file_name)
                print(f"Transforming: {input_pcap} -> {output_csv}")
                transform_captured_data(category, input_pcap, output_csv, target_device_ip)

if __name__ == "__main__":
    main()