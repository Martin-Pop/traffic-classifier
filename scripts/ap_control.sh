#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {on|off}"
    exit 1
fi

COMMAND=$1

if [[ "$COMMAND" != "on" && "$COMMAND" != "off" ]]; then
    echo "Error: Invalid argument '$COMMAND'. Please use 'on' or 'off'."
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run as root."
  exit 1
fi

source "$(dirname "$0")/ap_config.sh"

# gets current active connection name on specified interface
ACTIVE_CON=$(nmcli -t -f DEVICE,NAME connection show --active | grep "^${IFACE}:" | cut -d: -f2)


start_ap() {
    echo "Checking current status of ${IFACE}..."
    
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
    (
        set -e
        nmcli device wifi hotspot ifname "$IFACE" ssid "$SSID" password "$PASS" con-name "$CON_NAME"
        nmcli connection modify "$CON_NAME" ipv4.addresses 192.168.1.1/24
        nmcli connection up "$CON_NAME"
    ) > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "-------------------------------------------"
        echo "SUCCESS: AP is UP on ${IFACE}"
        echo "SSID: ${SSID}"
        echo "Password: ${PASS}"
        echo "-------------------------------------------"
    else
        echo "Error: Failed to start Access Point."
        sysctl -w net.ipv4.ip_forward=0
        exit 1
    fi
}


stop_ap() {
    echo "Checking current status of ${IFACE}..."
    
    if [ "$ACTIVE_CON" != "$CON_NAME" ]; then
        echo "Notice: AP is NOT running on ${IFACE}."
        echo "Current connection is: ${ACTIVE_CON:-None}"
        echo "Nothing to stop. Exiting."
        exit 0
    fi

    echo "Stopping Hotspot profile (${CON_NAME})..."
    nmcli connection down "$CON_NAME"

    echo "Deleting Hotspot profile to prevent auto-reconnect..."
    nmcli connection delete "$CON_NAME"

    echo "Disabling IP forwarding..."
    sysctl -w net.ipv4.ip_forward=0

    echo "Restoring ${IFACE} to standard client mode..."
    nmcli device set "$IFACE" managed yes

    echo "-------------------------------------------"
    echo "SUCCESS: AP stopped and interface restored."
    echo "-------------------------------------------"
}

case "$COMMAND" in
    on)
        start_ap ;;
    off)
        stop_ap ;;
esac