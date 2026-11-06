#!/usr/bin/env python3
"""Data acquisition for street-hail taxi accessibility study (Paper 1, public data only).

Downloads and persists raw snapshots under data/raw/ with a machine-readable
acquisition ledger (JSONL): source URL, version/date, sha256, size, license.
"""
import hashlib, json, os, sys, time, urllib.request, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
os.makedirs(RAW, exist_ok=True)
LEDGER = os.path.join(RAW, "acquisition_ledger.jsonl")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def record(entry):
    entry = dict(entry)
    entry.setdefault("accessed_utc", datetime.datetime.utcnow().isoformat() + "Z")
    with open(LEDGER, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print("LEDGER:", json.dumps(entry))

def fetch(url, dest, **meta):
    req = urllib.request.Request(url, headers={"User-Agent": "devin-research/1.0 (academic study)"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except Exception as e:
        record({"source": meta.get("source", url), "url": url, "status": "FAILED", "error": str(e)})
        return None
    with open(dest, "wb") as f:
        f.write(data)
    record({"source": meta.get("source"), "url": url, "status": "OK", "path": dest,
            "bytes": len(data), "sha256": sha256(dest), **{k: v for k, v in meta.items() if k != "source"}})
    return dest

# ---------------------------------------------------------------
# 1. OSM road network (drive graph) for the 5 central wards of Tokyo
#    via OSMnx (Overpass API). Saved as GraphML (raw snapshot) +
#    cleaned graph.
# ---------------------------------------------------------------
def get_osm():
    import osmnx as ox
    wards = ["Chiyoda, Tokyo, Japan", "Chuo, Tokyo, Japan", "Minato, Tokyo, Japan",
             "Shinjuku, Tokyo, Japan", "Shibuya, Tokyo, Japan"]
    polys = [ox.geocode_to_gdf(w).geometry.iloc[0] for w in wards]
    from shapely.ops import unary_union
    poly = unary_union(polys)
    import geopandas as gpd
    gpd.GeoSeries([poly], crs=4326).to_file(os.path.join(RAW, "study_polygon.geojson"), driver="GeoJSON")
    print("downloading drive graph...")
    t0 = time.time()
    G = ox.graph_from_polygon(poly, network_type="drive", retain_all=False, simplify=True)
    print("nodes", len(G.nodes), "edges", len(G.edges), f"{time.time()-t0:.0f}s")
    p = os.path.join(RAW, "osm_drive_graph.graphml")
    ox.save_graphml(G, p)
    record({"source": "OpenStreetMap via Overpass (OSMnx)", "url": "https://overpass-api.de/",
            "status": "OK", "path": p, "bytes": os.path.getsize(p), "sha256": sha256(p),
            "license": "ODbL 1.0", "scope": "5 central wards Tokyo", "temporal": "current snapshot"})
    # pedestrian-walkable network for walking distances (walk graph)
    t0 = time.time()
    W = ox.graph_from_polygon(poly, network_type="walk", retain_all=False, simplify=True)
    print("walk nodes", len(W.nodes), "edges", len(W.edges), f"{time.time()-t0:.0f}s")
    p = os.path.join(RAW, "osm_walk_graph.graphml")
    ox.save_graphml(W, p)
    record({"source": "OpenStreetMap walk network via Overpass", "url": "https://overpass-api.de/",
            "status": "OK", "path": p, "bytes": os.path.getsize(p), "sha256": sha256(p),
            "license": "ODbL 1.0", "scope": "5 central wards Tokyo"})
    return poly

# ---------------------------------------------------------------
# 2. OSM POIs: stations, taxi stands, nightlife, hotels, hospitals,
#    airports/terminals within the polygon (features_from_polygon).
# ---------------------------------------------------------------
def get_pois(poly):
    import osmnx as ox, geopandas as gpd
    tags = {
        "public_transport": True, "railway": ["station", "halt", "subway_entrance"],
        "amenity": ["taxi"], "tourism": ["hotel", "attraction", "museum"],
        "aeroway": ["aerodrome", "terminal"],
        "leisure": ["nightclub"], "shop": True, "office": True,
        "amenity:taxi": True,
    }
    tags = {"railway": ["station"], "public_transport": True,
            "amenity": ["taxi", "bar", "nightclub", "hospital"],
            "tourism": ["hotel", "attraction"], "shop": True, "office": True,
            "aeroway": ["aerodrome"]}
    t0 = time.time()
    try:
        feats = ox.features_from_polygon(poly, tags=tags)
    except Exception as e:
        print("POI fetch failed:", e); return
    print("pois", len(feats), f"{time.time()-t0:.0f}s")
    p = os.path.join(RAW, "osm_pois.geojson")
    feats[feats.geometry.geom_type.isin(["Point", "Polygon", "MultiPolygon"])].to_file(p, driver="GeoJSON")
    record({"source": "OSM POI features via Overpass", "url": "https://overpass-api.de/",
            "status": "OK", "path": p, "bytes": os.path.getsize(p), "sha256": sha256(p),
            "license": "ODbL 1.0", "tags": tags})

# ---------------------------------------------------------------
# 3. National Land Numerical Information (NLNI / 国土数値情報):
#    N02 railway station passenger data, Tokyo (area code 13).
#    License: NLNI terms (free use w/ attribution for research).
# ---------------------------------------------------------------
NLNI_CANDIDATES = [
    "https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-23/N02-23_GML.zip",
    "https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-2023/N02-2023_GML.zip",
    "https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-22/N02-22_GML.zip",
]
def get_nlni():
    dest = os.path.join(RAW, "N02_tokyo_stations.zip")
    for url in NLNI_CANDIDATES:
        r = fetch(url, dest, source="NLNI N02 railway station passengers (Tokyo)",
                  license="MLIT National Land Numerical Information terms")
        if r and os.path.getsize(dest) > 1000:
            return
    record({"source": "NLNI N02", "url": NLNI_CANDIDATES, "status": "INACCESSIBLE"})

if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("all", "osm"):
        poly = get_osm()
    else:
        import geopandas as gpd
        poly = gpd.read_file(os.path.join(RAW, "study_polygon.geojson")).geometry.iloc[0]
    if step in ("all", "pois"):
        get_pois(poly)
    if step in ("all", "nlni"):
        get_nlni()
    print("done")
