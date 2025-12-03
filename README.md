# 📦 BitTorrent Client in Python

A lightweight, educational BitTorrent client built entirely in Python — designed to help you understand the internals of the BitTorrent protocol: torrent parsing, peer discovery, tracker communication, handshakes, and piece exchange.

<img width="591" alt="diagram" src="https://github.com/user-attachments/assets/41f7be23-c7a2-43e4-99ad-066bb12d3068" />
<img width="800" alt="architecture" src="https://github.com/user-attachments/assets/eb6b3912-ea10-4b0a-b8c6-b229fe3e64c2" />

---

## 🚀 Overview

This project implements core components of a BitTorrent client **from scratch**, focusing on understanding the low-level mechanics of P2P networking.

It explains:

- How `.torrent` files are structured  
- How magnet links work  
- How peers and trackers communicate  
- How the BitTorrent handshake works  
- How pieces are exchanged between peers  

Perfect for anyone exploring **networking**, **protocol reverse engineering**, or **distributed systems**.

---

## 🔥 Features

### **Torrent Parsing**
- Decode `.torrent` files (bencoded data)  
- Extract `info_hash`, piece length, file metadata & trackers  

### **Magnet Link Support**
- Parse magnet URIs  
- Extract info hash, display name, tracker list  

### **Tracker Communication**
- HTTP/UDP tracker support  
- Announce to trackers & fetch peer lists  

### **Peer Discovery + Handshake**
- Establish peer connections  
- Implement BitTorrent handshake  
- Extended handshake support  

### **Piece Management (WIP)**
- Piece selection  
- Request/response pipeline  
- SHA-1 hash verification  

---

## 🧠 Architecture (How It Works)

<img width="700" alt="arch" src="https://github.com/user-attachments/assets/abe55f37-1cc3-4021-b423-c31178ce6d90" />

### **1. Torrent / Magnet Parsing**
**File:** `torrent/parser.py`  
Extracts metadata required for downloading.

### **2. Tracker Communication**
**File:** `network/tracker.py`  
Sends announce requests and receives peer lists.

### **3. Client Engine**
**File:** `client/engine.py`  
Handles peer connections, handshakes, and piece workflow.

### **4. Entry Point**
**File:** `app/main.py`  
The CLI entrypoint connecting all modules.

---

## 📁 Project Structure
bittorrent-python/
│
├── app/
│ └── main.py # Entry point
│
├── torrent/
│ ├── parser.py # Torrent & magnet parsing
│ └── init.py
│
├── network/
│ ├── tracker.py # Tracker communication
│ └── init.py
│
├── client/
│ ├── engine.py # Peer & piece logic
│ └── init.py
│
├── utils/
│ ├── hashing.py # SHA1 utilities
│ └── init.py
│
├── samples/
│ ├── sample.torrent
│ ├── debug_peers.py
│ └── debug_torrent.py
│
├── .github/
│ └── workflows/
│ └── ci.yml # GitHub Actions CI
│
├── README.md
├── .gitignore


---

## 🛠️ Installation

### **1. Clone the repository**
```bash
git clone https://github.com/dvanhu/bittorrent-python.git
cd bittorrent-python

2. Install dependencies
pip install -r requirements.txt
```
📡 How the BitTorrent Handshake Works
<img width="1000" alt="handshake" src="https://github.com/user-attachments/assets/ecb4f7ed-b74e-4d2a-a7d8-79c6ac94912d" />

Client connects to a peer (IP:port)

Sends handshake containing:

Protocol identifier: BitTorrent protocol

info-hash

peer ID

Peer responds with its handshake

After verification → piece requests begin

This handshake enables secure and valid P2P communication.


bittorrent-python/
