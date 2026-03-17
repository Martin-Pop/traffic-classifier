import os
import sys

try:
    from src.transform import transform_captured_data
except ImportError:
    from transform import transform_captured_data

def print_usage():
    print("--- Script Usage ---")
    print("  new <category> <ip>")
    print("  all <category> <ip> (overwrites existing dataset)")
    print("  append <file.pcap> <category> <ip>")
    print("\nExamples:")
    print("  new gaming 192.168.1.10")
    print("  all gaming 192.168.1.10")
    print("  append roblox_match1.pcap gaming 192.168.1.10")
    print("----------------------")

def process_all_in_category(category_dir, category, output_csv, ip):
    found_any = False
    for file_name in os.listdir(category_dir):
        if file_name.endswith(".pcap") or file_name.endswith(".pcapng"):
            input_pcap = os.path.join(category_dir, file_name)
            print(f"Processing: {input_pcap} -> {output_csv}")
            transform_captured_data(category, input_pcap, output_csv, ip)
            found_any = True
    
    if not found_any:
        print(f"[WARNING] No .pcap files found in {category_dir}.")

def main():
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    mode = sys.argv[1].lower()

    input_base_dir = "data/raw_pcaps"
    output_base_dir = "data/datasets"
    os.makedirs(output_base_dir, exist_ok=True)

    if mode in ['new', 'all']:
        category = sys.argv[2]
        target_device_ip = sys.argv[3]
        
        category_dir = os.path.join(input_base_dir, category)
        output_csv = os.path.join(output_base_dir, f"{category}.csv")

        if not os.path.isdir(category_dir):
            print(f"[ERROR] Category directory does not exist: {category_dir}")
            sys.exit(1)

        if mode == 'new' and os.path.isfile(output_csv):
            print(f"[ERROR] Dataset {output_csv} already exists")
            print("Delete it manually, use 'append' to add a file, or 'all' to overwrite.")
            sys.exit(1)

        if mode == 'all' and os.path.isfile(output_csv):
            print(f"[INFO] Deleting old dataset: {output_csv}")
            os.remove(output_csv)

        process_all_in_category(category_dir, category, output_csv, target_device_ip)
        print(f"[DONE] Category '{category}' fully processed")

    elif mode == 'append':
        if len(sys.argv) < 5:
            print("[ERROR] Missing parameters for 'append' mode")
            print_usage()
            sys.exit(1)
        
        pcap_file = sys.argv[2]
        category = sys.argv[3]
        target_device_ip = sys.argv[4]

        category_dir = os.path.join(input_base_dir, category)
        input_pcap = os.path.join(category_dir, pcap_file)
        output_csv = os.path.join(output_base_dir, f"{category}.csv")

        if not os.path.isfile(input_pcap):
            print(f"[ERROR] File to append not found: {input_pcap}")
            sys.exit(1)

        print(f"Appending single file: {input_pcap} -> {output_csv}")
        transform_captured_data(category, input_pcap, output_csv, target_device_ip)
        print(f"[DONE] File '{pcap_file}' successfully appended to '{category}.csv'")

    else:
        print(f"[ERROR] Unknown mode: {mode}")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()