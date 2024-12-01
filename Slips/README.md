# Stratosphere Linux IPS (SLIPS) on Raspberry Pi

## Overview

This repository provides instructions and resources to adapt the installation of **Stratosphere Linux IPS (SLIPS)** on Raspberry Pi devices, supporting both 32-bit and 64-bit architectures. By default, SLIPS does not natively support these platforms. This work makes it possible to run SLIPS on Raspberry Pi with minimal adjustments, ensuring lightweight intrusion prevention for your network.

## What is SLIPS?

**Stratosphere Linux IPS (SLIPS)** is an open-source Intrusion Prevention System designed to detect and block malicious activities on Linux devices. It analyzes network traffic in real-time, making it a powerful tool for enhancing security on edge devices.

Learn more about SLIPS on the official project page: [Stratosphere Linux IPS](https://github.com/stratosphereips/SLIPS).

## Key Features

- **Raspberry Pi Compatibility**: Enables SLIPS to run on both 32-bit (ARMv7) and 64-bit (ARM64) Raspberry Pi architectures.
- **Simple Deployment**: Pre-configured resources for straightforward setup using prebuilt files.
- **Lightweight Solution**: Tailored for the limited computational resources of Raspberry Pi devices.
- **TensorFlow Limitation**: Note that **TensorFlow** is difficult to install on Raspberry Pi 32-bit architectures. I decided not to install TensorFlow because it was necessary to downgrade the python version, which would put other detection modules at risk.

## Getting Started

### Prerequisites

- Raspberry Pi 3, 4, or later (32-bit or 64-bit architecture)
- A Debian-based Linux distribution (e.g., Raspberry Pi OS)
- Root or sudo access

### Installation

1. **Clone Slips repository**:
   ```bash
   git clone https://github.com/stratosphereips/StratosphereLinuxIPS.git
   cd StratosphereLinuxIPS

2. **Selects the folder corresponding to the Raspberry Pi's processor type (32-bit or 64-bit)**:
   
3. **Replace the contents of the Slips install folder with the contents of the previously selected folder**

4. **Execute installation script**:
   ```bash
   sudo chmod +x ./install/install.sh
   sudo ./install/install.sh