BitTorrent Client in Python

A lightweight, educational BitTorrent client built entirely in Python — designed to help understand the internals of the BitTorrent protocol: torrent parsing, peer discovery, tracker communication, handshakes, and piece exchange.

<img width="591" height="423" alt="image" src="https://github.com/user-attachments/assets/41f7be23-c7a2-43e4-99ad-066bb12d3068" />
<img width="1280" height="1657" alt="image" src="https://github.com/user-attachments/assets/eb6b3912-ea10-4b0a-b8c6-b229fe3e64c2" />

Overview

This project implements key parts of a BitTorrent client from scratch, focusing on learning the low-level mechanics of P2P networking.
Instead of relying on large libraries, this repo contains simple and readable Python code that helps you understand:

How '''.torrent''' files are structured

How magnet links work

How peers and trackers communicate

How the BitTorrent handshake works

How pieces are exchanged between peers

This is a perfect project for anyone exploring networking, protocol reverse engineering, distributed systems, or peer-to-peer architectures.

Features

Torrent Parsing

Decode '''.torrent'''  files (bencoded data)

Extract info_hash, piece length, file metadata & trackers

Magnet Link Support

Parse magnet URIs

Extract hash + display name + tracker list

Tracker Communication

Supports HTTP/UDP trackers

Announce & fetch peer list

Peer Discovery + Handshake

Establish peer connections

Implement BitTorrent handshake

Extended handshake support

Piece Management (WIP)

Piece selection

Request/response pipeline

Hash verification

Architecture (How It Works)
<img width="806" height="516" alt="image" src="https://github.com/user-attachments/assets/abe55f37-1cc3-4021-b423-c31178ce6d90" />

🔹 1. Torrent / Magnet Parsing

Located in '''torrent/parser.py'''
Responsible for extracting metadata necessary for downloading.

🔹 2. Tracker Communication

Located in '''network/tracker.py'''
Sends announce requests → receives list of peers.

🔹 3. Client Engine

Located in '''client/engine.py'''
Coordinates connections, handshakes, and piece exchanges.

🔹 4. Entry Point

'''app/main.py''' contains CLI logic and ties everything together.

Project Structure
'''bittorrent-python/
│
├── app/
│   └── main.py              # Entry point
│
├── torrent/
│   ├── parser.py            # Torrent & magnet parsing
│   └── __init__.py
│
├── network/
│   ├── tracker.py           # Tracker communication
│   └── __init__.py
│
├── client/
│   ├── engine.py            # Peer and piece logic
│   └── __init__.py
│
├── utils/
│   ├── hashing.py           # SHA1 utilities
│   └── __init__.py
│
├── samples/
│   ├── sample.torrent
│   ├── debug_peers.py
│   └── debug_torrent.py
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI
│
├── README.md
├── .gitignore'''

Installation
Clone the repository
'''git clone https://github.com/dvanhu/bittorrent-python.git
cd bittorrent-python'''

Install dependencies

If using requirements.txt:

'''pip install -r requirements.txt'''


📡 How the BitTorrent Handshake Works
<img width="2918" height="1667" alt="image" src="https://github.com/user-attachments/assets/ecb4f7ed-b74e-4d2a-a7d8-79c6ac94912d" />

Client connects to a peer (IP:port)

Sends handshake containing:

Protocol identifier '''(BitTorrent protocol)'''

Info-hash

Peer ID

Peer responds with its handshake

After handshake → piece requests begin

