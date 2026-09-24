#!/bin/bash
# Captura e análise via tshark (Kali). Ajuste IFACE e PORTA.
IFACE="lo"
PORTA="8002"
echo "[*] Capturando 60s em $IFACE (porta $PORTA)..."
tshark -i "$IFACE" -f "tcp port $PORTA" -a duration:60 -w captura_brute.pcap
echo "[+] Total POST: $(tshark -r captura_brute.pcap -Y 'http.request.method==POST' 2>/dev/null | wc -l)"
echo "[+] 401: $(tshark -r captura_brute.pcap -Y 'http.response.code==401' 2>/dev/null | wc -l)"
echo "[+] 200: $(tshark -r captura_brute.pcap -Y 'http.response.code==200' 2>/dev/null | wc -l)"
tshark -r captura_brute.pcap -Y 'http.response.code==200' -T fields -e http.file_data 2>/dev/null
