import pandas as pd
from PySide6.QtCore import QThread, Signal
from threading import Event

from core.pcap_reader import extract_features_from_pcap

class Analyzer(QThread):
    progress_update = Signal(str)
    analysis_finished = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, file_path, model_service, target_ip, window_size_sec, step_size_sec):
        super().__init__()
        self._file_path = file_path
        self._model_service = model_service
        self._target_ip = target_ip
        self._window_size = window_size_sec
        self._step_size = step_size_sec

        self._cancellation_token = Event()

    def stop(self):
        self._cancellation_token.set()

    def run(self):
        try:
            self.progress_update.emit("Extracting features from PCAP... 0%")
            features, is_too_small = extract_features_from_pcap(
                self._file_path,
                self._target_ip,
                self._window_size,
                self._step_size,
                progress_callback= lambda percent: self.progress_update.emit(f"Extracting features from PCAP... {percent}% "),
                cancellation_token=self._cancellation_token
            )

            if self._cancellation_token.is_set():
                return

            if is_too_small:
                self.error_occurred.emit("Traffic was found, but capture is too small to analyse (less than 20 seconds)")
                return

            if not features:
                self.error_occurred.emit(f"No traffic found for the target IP. ({self._target_ip})")
                return

            df = pd.DataFrame(features)
            x = df.drop(columns=['timestamp'], errors='ignore')

            self.progress_update.emit("Running predictions...")

            probabilities = self._model_service.predict_proba(x)
            class_names = self._model_service.get_classes()

            results_df = pd.DataFrame(probabilities, columns=class_names)
            results_df = (results_df * 100).round(2)

            if 'timestamp' in df.columns:
                results_df.insert(0, 'timestamp', df['timestamp'])

            results = results_df.to_dict('records')

            self.progress_update.emit("Analysis complete.")
            self.analysis_finished.emit(results)

        except Exception as e:
            self.error_occurred.emit(str(e))