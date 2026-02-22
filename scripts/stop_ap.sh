#!/bin/bash

source "$(dirname "$0")/ap_config.sh"

if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run as root."
  exit 1
fi

echo "Checking current status of ${IFACE}..."
ACTIVE_CON=$(nmcli -t -f DEVICE,NAME connection show --active | grep "^${IFACE}:" | cut -d: -f2)

if [ "$ACTIVE_CON" != "$CON_NAME" ]; then
    echo "Notice: AP is NOT running on ${IFACE}."
    echo "Current connection is: ${ACTIVE_CON:-None}"
    echo "Nothing to stop. Exiting."
    exit 0
fi

echo "Stopping Hotspot profile (${CON_NAME})..."
nmcli connection down "$CON_NAME"

echo "Deleting Hotspot profile to prevent auto-reconnect..."
nmcli connection delete "$CON_NAME" 2>/dev/null

echo "Disabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=0

echo "Restoring ${IFACE} to standard client mode..."
nmcli device set "$IFACE" managed yes
nmcli device connect "$IFACE"

echo "Requesting new IP address from the home router..."
dhclient -r "$IFACE" && dhclient -v "$IFACE"

echo "-------------------------------------------"
echo "SUCCESS: AP stopped and interface restored."
echo "-------------------------------------------"