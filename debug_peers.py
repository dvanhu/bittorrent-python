# debug_peers.py — lightweight standalone tracker test
import hashlib, sys, requests
from urllib.parse import quote_from_bytes, urlencode
from typing import Tuple, Any, Optional

def decode_bencode_capture_info(b: bytes):
    def _dec(b, idx):
        if idx>=len(b): raise ValueError("eoi")
        c=chr(b[idx])
        if c.isdigit():
            colon=b.find(b":", idx)
            length=int(b[idx:colon].decode())
            s=b[colon+1:colon+1+length]
            return s, colon+1+length, None
        if c=="i":
            e=b.find(b"e", idx)
            return int(b[idx+1:e].decode()), e+1, None
        if c=="l":
            i=idx+1; items=[]; info=None
            while b[i:i+1]!=b"e":
                v,i,ir=_dec(b,i); items.append(v)
                if ir is not None: info=ir
            return items, i+1, info
        if c=="d":
            i=idx+1; d={}; info=None
            while b[i:i+1]!=b"e":
                k,i,_=_dec(b,i)
                if not isinstance(k,(bytes,bytearray)): raise ValueError("bad key")
                try: key=k.decode()
                except: key=k.decode("latin-1")
                if key=="info":
                    v, i, _ = _dec(b, i)
                    # capture raw slice for info
                    # here we recompute by re-scanning to find the value bytes:
                    # (simpler approach: we find slice by parsing again from this idx)
                    # but for debug we simply return decoded form and will recompute raw below
                    d[key]=v
                    continue
                v,i,_=_dec(b,i)
                d[key]=v
            return d, i+1, info
        raise ValueError("unknown")
    val, nxt, info_raw = _dec(b, 0)
    return val, info_raw

def capture_info_raw_exact(b: bytes):
    # Find the raw slice for the 'info' value by searching for b'd' then parsing keys
    # Simpler: walk top-level dict to find the 'info' key and capture raw bytes
    # We'll do a small deterministic scan similar to prior decoder:
    def _decode_at(b, idx):
        c=chr(b[idx])
        if c.isdigit():
            colon=b.find(b":", idx)
            length=int(b[idx:colon].decode())
            start=colon+1
            return b[start:start+length], start+length, None
        if c=="i":
            e=b.find(b"e", idx); return int(b[idx+1:e].decode()), e+1, None
        if c=="l":
            i=idx+1; items=[]
            while b[i:i+1]!=b"e":
                v,i,_=_decode_at(b,i); items.append(v)
            return items, i+1, None
        if c=="d":
            i=idx+1
            while b[i:i+1]!=b"e":
                k,i,_=_decode_at(b,i)
                if not isinstance(k,(bytes,bytearray)): raise ValueError("bad key")
                try: key=k.decode()
                except: key=k.decode("latin-1")
                if key=="info":
                    val_start=i
                    v,i,_=_decode_at(b,i)
                    val_end=i
                    return None, None, b[val_start:val_end]
                else:
                    v,i,_=_decode_at(b,i)
            return None, None, None
        raise ValueError("invalid")
    _,_,info_raw = _decode_at(b,0)
    return info_raw

if __name__=='__main__':
    tfile='sample.torrent'
    try:
        raw = open(tfile,'rb').read()
    except Exception as e:
        print("ERROR opening torrent:", e); raise SystemExit(1)

    # sanity print
    print("Opened", tfile, "size", len(raw))

    # compute exact info_raw slice
    info_raw = capture_info_raw_exact(raw)
    if info_raw is None:
        print("ERROR: couldn't capture raw info bytes"); raise SystemExit(1)
    print("Captured info_raw len:", len(info_raw))
    info_hash_raw = hashlib.sha1(info_raw).digest()
    print("Info hash (hex):", hashlib.sha1(info_raw).hexdigest())

    # announce
    # naive parse to extract announce quickly
    meta, _ = decode_bencode_capture_info(raw)
    announce = meta.get(b"announce") if isinstance(list(meta.keys())[0], bytes) else meta.get("announce")
    # handle both bytes/str keys
    if isinstance(announce, (bytes,bytearray)):
        try: announce_s=announce.decode()
        except: announce_s=announce.decode("latin-1")
    else:
        announce_s=str(announce)
    print("Announce:", announce_s)

    # Build peer_id (ASCII-safe deterministic)
    peer_id = b"-PC0001-1234567890"   # 20 bytes exactly
    encoded_info_hash = quote_from_bytes(info_hash_raw)
    encoded_peer_id  = quote_from_bytes(peer_id)

    params = {"port":"6881","uploaded":"0","downloaded":"0","left":"92063","compact":"1"}
    qs = urlencode(params)
    sep='&' if '?' in announce_s else '?'
    url = f"{announce_s}{sep}info_hash={encoded_info_hash}&peer_id={encoded_peer_id}&{qs}"

    print("Request URL:", url)
    print("Sending GET... (this may take up to 10s)")
    r = requests.get(url, timeout=15)
    print("HTTP status:", r.status_code)
    print("Response first 800 bytes (latin-1):")
    print(r.content[:800].decode('latin-1', errors='replace'))
    try:
        parsed, _ = decode_bencode_capture_info(r.content)
        print("Parsed tracker response keys:", list(parsed.keys()) if isinstance(parsed, dict) else type(parsed))
        if isinstance(parsed, dict):
            if b'failure reason' in parsed or 'failure reason' in parsed:
                fr = parsed.get(b'failure reason') or parsed.get('failure reason')
                if isinstance(fr,(bytes,bytearray)): fr = fr.decode('latin-1', errors='replace')
                print("Tracker failure reason:", fr)
            else:
                peers = parsed.get(b'peers') or parsed.get('peers')
                print("peers type:", type(peers))
                if isinstance(peers,(bytes,bytearray)):
                    print("peers len:", len(peers))
                    for i in range(0, len(peers), 6):
                        ip = ".".join(str(b) for b in peers[i:i+4])
                        port = int.from_bytes(peers[i+4:i+6], 'big')
                        print(f"{ip}:{port}")
    except Exception as e:
        print("Failed to parse tracker response as bencode:", e)
