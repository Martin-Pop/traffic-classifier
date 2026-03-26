# Sběr a zpracování dat

## 1. Architektura sběru dat
Sběr síťového provozu probíhá externě přes hotspot na Raspberry Pi. Hlavní důvody pro tento přístup:

* **Jednodušší správa:** Není potřeba nic instalovat ani nastavovat na koncových zařízeních. Proces je jednotný pro mobily i PC.
* **Ochrana před Anti-Cheatem:** Některé hry na zařízeních detekují spuštěné síťové analyzátory (např. Wireshark) a zablokují se.

**Technické řešení:**
* **Zařízení:** Raspberry Pi připojené k domácímu routeru.
* **Topologie:** Na RPi je vytvořen Wi-Fi hotspot. Testované zařízení se na něj připojí a RPi pouze forwarduje traffic do routeru.
* **Odchytávání:** Provoz se zachytává přímo na síťovém rozhraní RPi do `.pcap` souboru.

## 2. Metodika měření
Data byla sbírána pro každou kategorii zvlášť:
1.  Na testovaném zařízení byly vypnuty všechny aplikace na pozadí.
2.  Byla spuštěna specifická aktivita pro danou kategorii (např. scrollování TikTok pro `short_video`, hraní Clash Royale pro `gaming`).
3.  Aktivita byla prováděna souvisle po určenou dobu (např. 5-10 minut).
4.  Data byla uložena do surového `.pcap` souboru ve složce k dané kategorii.

## 3. Zpracování dat
Surový `.pcap` soubor prochází fázemi čištění, než se z něj začnou počítat vlastnosti (features) pro model:

1.  **Filtrování (Clean):** Ponechají se pouze pakety, kde zdrojová / cílová IP odpovídá testovanému zařízení. Odstraní se broadcasty `*.255` a multicasty `224.*`, `239.*`.
2.  **Ořez (Cut-off):** Smaže se prvních a posledních 5 sekund záznamu. Tím se odstraní možné zkreslení vzniklé zapínáním/vypínáním (možná zbytečné).
3.  **Rozdělení na části (Sliding Window):** Provoz se rozseká na časová okna o velikosti **20 sekund** s krokem **5 sekund**. Každé okno je jeden řádek dat.

## 4. Vypočítané vlastnosti (Features)

### A. Použité vlastnosti

* `in_packet_ratio`: Poměr příchozích paketů vůči všem paketům (symetrie komunikace).
* `in_byte_ratio`: Poměr přijatých bajtů vůči všem bajtům.
* `size_mean`: Průměrná velikost paketu.
* `size_std`: Směrodatná odchylka velikosti paketů.
* `size_min` / `size_max`: Minimální a maximální velikost paketu.
* `iat_mean`: Průměrná mezera (Inter-Arrival Time) mezi pakety (frekvence komunikace).
* `iat_std`: Směrodatná odchylka mezer (plynulost?).
* `iat_max`: Nejdelší ticho v okně (čtení webu nebo idle).
* `tcp_ratio` / `udp_ratio`: Zastoupení transportních protokolů.

### B. Zamítnuté vlastnosti 
Následující vlastnosti byly zvažovány nebo původně počítány, ale nakonec nebudou použity.

* `total_bytes`, `in_bytes`, `out_bytes`
    * Absolutní hodnoty. Závisí na rychlosti nebo například na rozlišení.
* `total_packets`, `in_packets`, `out_packets`:
    * Stejný problém jako u bytest. Rychlost je lépe popsána pomocí `iat_mean`.
* `prev_total_packets`: 
    * Mělo znázorňovat růst / pokles komunikace mezi "okny", není potřeba díky sliding window.

## 5. Jednotlivá měření

## Definice měřených kategorií
Dataset je rozdělen do 7 kategorií, které pokrývají běžné chování uživatele na síti:

* **browsing:** Běžné prohlížení webu (e-shopy, články, mapy). Typické je nárazové načtení obsahu a následné ticho, když uživatel čte.
* **download:** Stahování velkých souborů nebo her (např. ze Steamu). Souvislý a nepřetržitý tok velkých paketů, který se snaží maximálně vytížit linku.
* **gaming:** Hraní online multiplayer her. Vyznačuje se rychlou, obousměrnou komunikací s velmi malými pakety (často přes UDP).
* **idle:** Zařízení je odložené, uživatel s ním nepracuje. Sítí proudí jen malý "šum" na pozadí (udržovací keep-alive pakety, notifikace).
* **video:** Sledování filmů a delších videí (Netflix, Disney+, YouTube). Vyznačuje se bufferováním – aplikace stáhne velký blok dat dopředu a pak má síť chvíli pauzu.
* **short_video:** Sledování krátkých formátů (TikTok, YT Shorts). Kvůli rychlému scrollování, přeskakování a interagování se obsah stahuje častěji a v menších blocích než u klasického videa.
* **voice:** Hlasové hovory v reálném čase (Discord, WhatsApp). Charakteristický je přiměřeně symetrický a pravidelný provoz oběma směry bez větších mezer.

## 6. Jednotlivá měření

| Datum a čas      | Kategorie   | Soubor             | Velikost PCAP | Doba měření (min) | Popis aktivity                          |
|:-----------------|:------------|:-------------------|:--------------|:------------------|:----------------------------------------|
| 17.03.2026 17:12 | browsing    | notebook.pcap      | 13 MB         | 5                 | Prohledávání alza.cz                    |
| 18.03.2026 20:19 | browsing    | wiki.pcap          | 6.7 MB        | 5                 | Prohledávání náhodných wiki článků      |
| 21.03.2026 20:34 | browsing    | datart_pc.pcap     | 5.3 MB        | 5                 | browsing na datartu                     |
| 23.03.2026 14:02 | browsing    | seznam.pcap        | 16 MB         | 5                 | čtení novinek od seznamu                |
| 23.03.2026 14:09 | browsing    | maps.pcap          | 31 MB         | 5                 | hledání zajímavých míst v lisabonu      |
| 21.03.2026 19:04 | download    | steam.pcap         | 53 MB         | 5                 | aktualizace blender (2kbytes/s cap)     |
| 21.03.2026 19:10 | download    | steam_1.pcap       | 53 MB         | 5                 | aktualizace blender (2kbytes/s cap)     |
| 17.03.2026 17:37 | gaming      | roblox.pcap        | 82 MB         | 10                | hraní hry oaklands                      |
| 19.03.2026 17:44 | gaming      | clash_royale.pcap  | 896 KB        | 5                 | hraní clash royale                      |
| 19.03.2026 18:06 | gaming      | mopeio.pcap        | 6.9 MB        | 5                 | hraní webový hry mope.io                |
| 21.03.2026 20:07 | gaming      | roblox_toh.pcap    | 26 MB         | 5                 | hraní hry toh                           |
| 21.03.2026 20:18 | gaming      | roblox_toh_1.pcap  | 31 MB         | 5                 | hraní hry toh                           |
| 23.03.2026 14:20 | gaming      | minecraft.pcap     | 6.4 MB        | 5                 | hraní hry minectaft na veřejném serveru |
| 23.03.2026 14:27 | gaming      | minecraft_1.pcap   | 3.7 MB        | 5                 | hraní hry minectaft na veřejném serveru |
| 21.03.2026 19:25 | idle        | pc_idle.pcap       | 203 KB        | 10                | idle počítače (win11)                   |
| 21.03.2026 19:51 | idle        | pc_idle_1.pcap     | 731 KB        | 10                | idle počítače (win11)                   |
| 21.03.2026 21:57 | idle        | idle_phone.pcap    | 194 KB        | 10                | idle telefonu (android)                 |
| 23.03.2026 15:45 | idle        | pc_idle_2.pcap     | 102 KB        | 10                | idle počítače (win11)                   |
| 23.03.2026 16:14 | short_video | tiktok.pcap        | 40 MB         | 10                | sledování tiktoku                       |
| 23.03.2026 16:27 | short_video | yt_shorts.pcap     | 108 MB        | 10                | sledování youtube shorts                |
| 15.03.2026 10:58 | video       | yt_test.pcap       | 14 MB         | 5                 | sledování náhodného vide na youtube     |
| 17.03.2026 19:45 | video       | netflix.pcap       | 42 MB         | 5                 | sledování filmu na netflixu             |
| 17.03.2026 19:51 | video       | netflix_1.pcap     | 17 MB         | 5                 | sledování filmu na netflixu             |
| 18.03.2026 21:07 | video       | disney.pcap        | 18 MB         | 5                 | sledování filmu na disney+              |
| 19.03.2026 17:17 | video       | cineb.pcap         | 58 MB         | 10                | sledování filmu na webu                 |
| 21.03.2026 21:08 | video       | yt_brave.pcap      | 28 MB         | 10                | sledování youtube v prohlížeči          |
| 19.03.2026 18:32 | voice       | whatsupcall.pcap   | 1.7 MB        | 5                 | telefonování                            |
| 19.03.2026 18:37 | voice       | whatsupcall_1.pcap | 1.7 MB        | 5                 | telefonování                            |
| 23.03.2026 14:48 | voice       | dc.pcap            | 7.4 MB        | 5                 | discord call                            |