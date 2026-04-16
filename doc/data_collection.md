# Data Collection and Processing

## 1. Data Collection Architecture
Network traffic is captured externally using a hotspot on a Raspberry Pi. The main reasons for this approach:

* **Simpler management:** Nothing needs to be installed or configured on the end devices. The process is identical for both mobile devices and PCs.
* **Anti-Cheat protection:** Some games detect running network analyzers (e.g., Wireshark) on the device and may block execution.

**Technical solution:**
* **Device:** Raspberry Pi connected to the home router.
* **Topology:** A Wi-Fi hotspot is created on the RPi. The tested device connects to it, and the RPi simply forwards traffic to the router.
* **Capture:** Traffic is captured directly on the RPi network interface into a `.pcap` file.

## 2. Measurement Methodology
Data was collected separately for each category. To make the dataset reflect real-world conditions as closely as possible, measurements were performed in two different scenarios:

1. **Device preparation (Background state):**
    * *Clean environment:* All background applications on the tested device were closed before measurement.
    * *Simulated real usage:* Common communication and work applications (e.g., web browser, Discord) were intentionally left running in the background to introduce realistic network noise.

2. **Data collection:** A specific activity for the given category was performed (e.g., scrolling TikTok for `video`, playing Clash Royale for `gaming`).

3. **Measurement duration:** The activity was performed continuously for a defined period (typically 5–10 minutes).

4. **Storage:** The measured data was saved as a raw `.pcap` file in the corresponding category folder.

## 3. Data Processing
The raw `.pcap` file goes through several cleaning phases before features are computed for the model:

1. **Filtering (Clean):** Only packets where the source/destination IP matches the tested device are kept. Broadcasts `*.255` and multicasts `224.*`, `239.*` are removed.
2. **Cut-off:** The first and last 5 seconds of the capture are removed. This eliminates possible distortion caused by starting/stopping the capture (possibly unnecessary).
3. **Segmentation (Sliding Window):** Traffic is split into time windows of **20 seconds** with a step of **5 seconds**. Each window represents one data row.

## 4. Computed Features

### A. Used Features

* `in_packet_ratio`: Ratio of incoming packets to all packets (communication symmetry).
* `in_byte_ratio`: Ratio of received bytes to all bytes.
* `size_mean`: Average packet size.
* `size_std`: Standard deviation of packet sizes.
* `size_min` / `size_max`: Minimum and maximum packet size.
* `iat_mean`: Average Inter-Arrival Time between packets (communication frequency).
* `iat_std`: Standard deviation of inter-arrival times (smoothness?).
* `iat_max`: Longest silence within the window (reading a webpage or idle state).
* `tcp_ratio` / `udp_ratio`: Distribution of transport protocols.

### B. Rejected Features
The following features were considered or originally computed but will not be used:

* `total_bytes`, `in_bytes`, `out_bytes`
    * Absolute values. Dependent on connection speed or, for example, resolution.
* `total_packets`, `in_packets`, `out_packets`
    * Same issue as bytes. Speed is better described using `iat_mean`.
* `prev_total_packets`
    * Intended to represent growth/decline of communication between windows. Not needed due to the sliding window approach.

## 5. Definition of Measured Categories
The dataset is divided into 7 categories that represent common user network behavior:

* **browsing:** Regular web browsing (e-shops, articles, maps). Characterized by burst content loading followed by silence while the user reads.
* **download:** Downloading large files or games (e.g., from Steam). Continuous stream of large packets attempting to fully utilize the connection.
* **gaming:** Playing online multiplayer games. Characterized by fast, bidirectional communication with very small packets (often over UDP).
* **idle:** The device is left unattended. Only small background “noise” flows through the network (keep-alive packets, notifications).
* **video:** Watching videos (Netflix, Disney+, YouTube). Characterized by buffering — the app downloads a large chunk of data in advance, then pauses network usage for a while.
* **voice:** Real-time voice communication (Discord, WhatsApp). Characterized by relatively symmetric and regular traffic in both directions without large gaps.

## 6. Individual Measurements

| Category     | Activity description                                                    | Total time (min) |
|:-------------|:------------------------------------------------------------------------|:-----------------|
| **browsing** | Browsing e-shops (Alza.cz, Datart)                                     | 10               |
| **browsing** | Reading articles and news (Wikipedia, Seznam)                           | 10               |
| **browsing** | Searching in maps                                                       | 5                |
| **browsing** | Regular web browsing (including background applications)                 | 15               |
| **download** | Downloading application updates (Steam – Blender)                        | 10               |
| **gaming**   | Playing Roblox games (Oaklands, ToH, including background measurement)  | 30               |
| **gaming**   | Playing Minecraft on a public server                                    | 10               |
| **gaming**   | Playing Clash Royale                                                    | 5                |
| **gaming**   | Playing a web game (mope.io)                                            | 5                |
| **idle**     | Computer idle state – Windows 11 (clean and with background apps)       | 50               |
| **idle**     | Phone idle state – Android                                              | 10               |
| **video**    | Watching YouTube (regular videos, Shorts, Brave browser + background)   | 50               |
| **video**    | Watching movies and series (Netflix, Disney+, Cineb)                    | 25               |
| **video**    | Browsing TikTok feed                                                    | 10               |
| **voice**    | Voice communication calls (WhatsApp, Discord)                           | 15               |