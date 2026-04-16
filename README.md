# TrafficClassifier

This application analyzes and classifies network traffic. It uses machine learning (Scikit-Learn) to identify user activities. The program processes raw PCAP files and predicts traffic categories.

## Features
* Fast analysis of PCAP network recordings.
* AI classification for categories: browsing, download, gaming, video, idle, voice.
* GUI built with PySide6.
* Charts for data visualization.

## How to Run the Application

### 1. Compiled Version
1. Download and extract the application ZIP file.
2. Open the TrafficClassifier folder.
3. Run .exe file.

### 2. Developer Version
Requires Python 3.9 or newer.
1. Clone the repository to your computer.
2. Create a virtual environment.
3. Activate the virtual environment.
4. Install dependencies (available in requirements.txt).
5. Run the application: python src/main.py.

## Project Configuration
* **analysed_captures_directory**: Folder where analysis results are saved.
* **model_path**: Path to the trained AI model file.
* **window_size_sec**: Analysis window duration. Must match the value used during training.
* **step_size_sec**: Analysis window step. Must match the value used during training.
