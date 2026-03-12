import argparse
import os
import sys

try:
    from collector import collect_packets
    from utils import make_pcap_filename, get_unique_filepath
except ImportError:
    from src.collector import collect_packets
    from src.utils import make_pcap_filename, get_unique_filepath

def main():
    if os.geteuid() != 0:
        print("[ERROR] This script must be run as root.", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Collector CLI")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to sniff (e.g., wlan0)")
    parser.add_argument("-m", "--minutes", type=float, required=True, help="Duration of capture in minutes")
    parser.add_argument("-o", "--output", required=True, help="Output filename (e.g., gaming_01)")

    args = parser.parse_args()

    if args.minutes <= 0:
        print("[ERROR] Duration must be greater than 0.", file=sys.stderr)
        sys.exit(1)

    duration_seconds = int(args.minutes * 60)

    safe_filename = make_pcap_filename(args.output)
    
    # resolves output path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    output_dir = os.path.join(project_root, 'data', 'raw_pcaps')
    os.makedirs(output_dir, exist_ok=True)
    
    final_filepath = get_unique_filepath(os.path.join(output_dir, safe_filename))

    print(f"--- Packet Collection Started ---")
    print(f"Interface: {args.interface}")
    print(f"Duration:  {args.minutes} minutes")
    print(f"Output:    {final_filepath}")
    print(f"---------------------------------")
    print("Capturing... (Press Ctrl+C to stop manually)")

    try:
        captured_count = collect_packets(args.interface, duration_seconds, final_filepath)
        
        if captured_count > 0:
            print(f"\n[SUCCESS] Capture complete. Saved to {os.path.basename(final_filepath)}")
        else:
            print("\n[WARNING] Capture finished, but no packets were recorded. Check your interface/connection.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n[INFO] Capture interrupted by user (Ctrl+C). Exiting gracefully.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred in main: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()