import os

def make_pcap_filename(raw_input: str) -> str:
    base_name = os.path.basename(raw_input)
    name, _ = os.path.splitext(base_name)
    
    if not name:
        name = "capture"
        
    return f"{name}.pcap"

def file_exists(filepath: str) -> bool:
    return os.path.exists(filepath)

def get_unique_filepath(filepath: str) -> str:
    if not file_exists(filepath):
        return filepath
        
    name, ext = os.path.splitext(filepath)
    counter = 1
    
    while True:
        new_filepath = f"{name}_{counter}{ext}"
        if not file_exists(new_filepath):
            return new_filepath
        counter += 1