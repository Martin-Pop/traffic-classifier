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
Data byla sbírána pro každou kategorii zvlášť. Aby nasbíraný dataset co nejlépe reflektoval reálné podmínky, měření probíhalo ve dvou různých scénářích:

1.  **Příprava zařízení (Stav pozadí):**
    * *Čisté prostředí:* Na testovaném zařízení byly před měřením vypnuty veškeré aplikace na pozadí.
    * *Simulace běžného provozu:* Na pozadí byly záměrně ponechány spuštěné běžné komunikační a pracovní aplikace (např. webový prohlížeč, Discord), pro zanesení realistického síťového šumu.
2.  **Sběr dat:** Byla spuštěna specifická aktivita pro danou kategorii (např. scrollování TikTok pro `video`, hraní Clash Royale pro `gaming`).
3.  **Délka měření:** Aktivita byla prováděna souvisle po určenou dobu (zpravidla 5–10 minut).
4.  **Uložení:** Naměřená data byla uložena do surového `.pcap` souboru v příslušné složce dané kategorie.
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
* **video:** Sledování videí (Netflix, Disney+, YouTube). Vyznačuje se bufferováním – aplikace stáhne velký blok dat dopředu a pak má síť chvíli pauzu.
* **voice:** Hlasové hovory v reálném čase (Discord, WhatsApp). Charakteristický je přiměřeně symetrický a pravidelný provoz oběma směry bez větších mezer.

## ## 6. Jednotlivá měření

| Kategorie    | Popis aktivity                                                       | Celková doba (min) |
|:-------------|:---------------------------------------------------------------------|:-------------------|
| **browsing** | Prohledávání e-shopů (Alza.cz, Datart)                               | 10                 |
| **browsing** | Čtení článků a novinek (Wikipedie, Seznam)                           | 10                 |
| **browsing** | Hledání v mapách                                                     | 5                  |
| **browsing** | Běžné prohlížení webu (včetně aplikací na pozadí)                    | 15                 |
| **download** | Stahování aktualizací aplikací (Steam - Blender)                     | 10                 |
| **gaming**   | Hraní Roblox her (Oaklands, ToH, včetně měření na pozadí)            | 30                 |
| **gaming**   | Hraní Minecraftu na veřejném serveru                                 | 10                 |
| **gaming**   | Hraní hry Clash Royale                                               | 5                  |
| **gaming**   | Hraní webové hry (mope.io)                                           | 5                  |
| **idle**     | Nečinnost počítače - Win11 (čistá i s aplikacemi na pozadí)          | 50                 |
| **idle**     | Nečinnost telefonu - Android                                         | 10                 |
| **video**    | Sledování YouTube (klasická videa, Shorts, prohlížeč Brave + pozadí) | 50                 |
| **video**    | Sledování filmů a seriálů (Netflix, Disney+, Cineb)                  | 25                 |
| **video**    | Sledování sítě TikTok                                                | 10                 |
| **voice**    | Komunikační hovory (WhatsApp, Discord)                               | 15                 |