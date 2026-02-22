#!/bin/bash

source "$(dirname "$0")/ap_config.sh"

if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run as root."
  exit 1
fi

echo "Checking current status of ${IFACE}..."
ACTIVE_CON=$(nmcli -t -f DEVICE,NAME connection show --active | grep "^${IFACE}:" | cut -d: -f2)

if [ "$ACTIVE_CON" == "$CON_NAME" ]; then
    echo "Warning: Hotspot ($CON_NAME) is already running on ${IFACE}."
    echo "Aborting to prevent duplicates."
    exit 0
elif [ -n "$ACTIVE_CON" ]; then
    echo "Warning: ${IFACE} is currently connected to '${ACTIVE_CON}'."
    echo "This connection will be overridden by the Hotspot."
fi

echo "Enabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=1

echo "Starting Hotspot..."
nmcli device wifi hotspot ifname "$IFACE" ssid "$SSID" password "$PASS" con-name "$CON_NAME"
nmcli connection modify "$CON_NAME" ipv4.addresses 192.168.1.1/24
nmcli connection up "$CON_NAME"

if [ $? -eq 0 ]; then
    echo "-------------------------------------------"
    echo "SUCCESS: AP is UP on ${IFACE}"
    echo "SSID: ${SSID}"
    echo "Password: ${PASS}"
    echo "-------------------------------------------"
else
    echo "Error: Failed to start Access Point."
    sysctl -w net.ipv4.ip_forward=0
fi