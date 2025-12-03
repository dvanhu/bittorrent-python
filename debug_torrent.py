import hashlib, sys
from typing import Tuple,Any,Optional

# small bencode decode (re-uses same capture logic)
def decode_bencode_capture_info(b: bytes):
    def _decode_at(b, idx):
        if idx >= len(b): raise ValueError("eoi")
        c = chr(b[idx])
        if c.isdigit():
            colon = b.find(b":", idx)
            length = int(b[idx:colon].decode())
            s = b[colon+1:colon+1+length]
            return s, colon+1+length, None
        if c == "i":
            e = b.find(b"e", idx)
            n = int(b[idx+1:e].decode())
            return n, e+1, None
        if c == "l":
            i = idx+1; items=[]; info=None
            while b[i:i+1] != b"e":
                v,i,inf = _decode_at(b,i)
                items.append(v)
                if inf is not None: info = inf
            return items, i+1, info
        if c == "d":
            i = idx+1; d={}
            info=None
            while b[i:i+1] != b"e":
                k,i,infk = _decode_at(b,i)
                if infk is not None: info = infk
                if not isinstance(k,(bytes,bytearray)): raise ValueError("bad key")
                key = None
                try: key=k.decode()
                except: key=k.decode("latin-1")
                if key == "info":
                    vs, s_i, infv = _decode_at(b, i)
                    # capture raw slice
                    raw = b[i:s_i]
                    d[key] = vs
                    i = s_i
                    info = raw
                    continue
                v,i,infv = _decode_at(b,i)
                d[key]=v
                if infv is not None: info = infv
            return d, i+1, info
        raise ValueError("unknown")
    val, nxt, info_raw = _decode_at(b, 0)
    return val, info_raw

p = "sample.torrent"
try:
    with open(p,"rb") as f:
        raw = f.read()
    print("Opened:", p, "size:", len(raw))
    meta, info_raw = decode_bencode_capture_info(raw)
    print("Top-level type:", type(meta))
    if isinstance(meta, dict):
        print("Top-level keys:", list(meta.keys()))
        ann = meta.get("announce")
        if isinstance(ann,(bytes,bytearray)):
            try: print("announce:", ann.decode())
            except: print("announce (latin1):", ann.decode("latin-1"))
        else:
            print("announce:", ann)
        info = meta.get("info")
        print("info present:", isinstance(info,dict))
        if isinstance(info,dict):
            print("info keys:", list(info.keys()))
            print("length:", info.get("length"))
            pl = info.get("piece length")
            print("piece length:", pl)
            pieces = info.get("pieces")
            print("pieces type:", type(pieces), "len:", len(pieces) if isinstance(pieces,(bytes,bytearray)) else "n/a")
    else:
        print("meta not dict, repr:", repr(meta)[:200])
    print("Captured info_raw:", "YES" if info_raw is not None else "NO")
    if info_raw is not None:
        print("info_raw bytes len:", len(info_raw))
        print("info hash (hex):", hashlib.sha1(info_raw).hexdigest())
except Exception as e:
    print("ERROR:", repr(e))
