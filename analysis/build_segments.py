#!/usr/bin/env python3
"""Phase 5-6: build directed road-segment table + taxi-flow prior + accessibility specs A/B/C."""
import os, json, math, numpy as np, pandas as pd, geopandas as gpd
import osmnx as ox, networkx as nx
from scipy.spatial import cKDTree
from shapely.geometry import Point

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, PROC = f"{ROOT}/data/raw", f"{ROOT}/data/processed"
os.makedirs(PROC, exist_ok=True)

# ---------------- temporal profile (Tokyo Taxi Center monitor survey R5/2024) --
# hours 6..5 as published (monitor_2024.pdf, "利用時間帯別集計", n=2662)
HOURS6_5 = list(range(6, 24)) + list(range(0, 6))
COUNTS = [50, 17, 133, 161, 172, 157, 188, 203, 176, 178, 175, 223,
          166, 110, 103, 145, 86, 78, 69, 31, 18, 14, 5, 4]
BASE_P = {h: c / sum(COUNTS) for h, c in zip(HOURS6_5, COUNTS)}
# night-shifted variant for nightlife-context segments: mass shifted +3h
NIGHT_P = {(h + 3) % 24: BASE_P[h] for h in BASE_P}
# weekend multiplier for nightlife context (documented assumption; sensitivity-tested)
WKND_NIGHT_BOOST = 1.4

PERIODS = []
for wd in ["weekday", "weekend"]:
    for h in [8, 13, 17, 21, 23]:
        PERIODS.append({"id": f"{wd}_{h:02d}", "weekday": wd, "hour": h})

def build():
    print("loading drive graph")
    G = ox.load_graphml(f"{RAW}/osm_drive_graph.graphml")
    nodes = ox.graph_to_gdfs(G, edges=False)
    edges = ox.graph_to_gdfs(G, nodes=False).reset_index()
    edges = edges[edges.geometry.notna()].copy()
    # directed edges already: each (u,v,key) is a direction
    edges["mid"] = edges.geometry.apply(lambda g: g.interpolate(0.5, normalized=True))
    edges["mx"] = edges["mid"].x; edges["my"] = edges["mid"].y
    edges["highway1"] = edges["highway"].apply(lambda h: h[0] if isinstance(h, list) else h)

    # road-class flow-capacity weight (documented assumption, sensitivity-tested)
    CLASS_W = {"motorway": 1.0, "trunk": 1.0, "primary": 1.0, "secondary": 0.7,
               "tertiary": 0.5, "residential": 0.25, "unclassified": 0.25,
               "living_street": 0.10, "service": 0.10, "pedestrian": 0.0}
    edges["w_road"] = edges["highway1"].map(CLASS_W).fillna(0.15)
    # hail-infeasible classes (vehicles cannot legally/safely stop)
    edges["hail_ok"] = ~edges["highway1"].isin(["motorway", "motorway_link",
                                              "trunk", "trunk_link", "pedestrian"])
    # lanes where mapped
    edges["lanes_n"] = pd.to_numeric(edges.get("lanes"), errors="coerce").fillna(1)
    # intersection intensity: mean endpoint degree (number of outgoing edges)
    deg = dict(G.out_degree())
    edges["deg"] = (edges["u"].map(deg).fillna(1) + edges["v"].map(deg).fillna(1)) / 2

    # ---------- attractors ----------
    mid_xy = np.c_[edges.mx, edges.my]
    # meters conversion (Tokyo ~35.7N): 1 deg lon ~90.95 km? use projected metric
    # simple equirectangular meters
    LAT0 = math.radians(35.68)
    def to_m(xy):
        return np.c_[xy[:, 0] * 111320 * math.cos(LAT0), xy[:, 1] * 110540]
    mid_m = to_m(mid_xy)

    SIG = float(os.environ.get("SIGMA", "300"))  # gaussian decay, m (documented; sensitivity 150/500)
    SUF = os.environ.get("SUFFIX", "")
    def kernel(attr_xy, weight):
        if len(attr_xy) == 0:
            return np.zeros(len(edges))
        tree = cKDTree(to_m(np.asarray(attr_xy)))
        d, idx = tree.query(mid_m, k=min(8, len(attr_xy)), distance_upper_bound=3 * SIG)
        d = np.asarray(d); idx = np.asarray(idx)
        valid = idx < len(attr_xy)
        d = np.where(valid & np.isfinite(d), d, np.nan)
        w = np.where(valid, np.asarray(weight)[np.clip(idx, 0, len(attr_xy) - 1)], 0.0)
        k = np.nansum(np.exp(-(d ** 2) / (2 * SIG ** 2)) * w, axis=1)
        return k

    # NLNI station locations. FY2023 N02 schema carries NO passenger-count field
    # (N02_004 is the operator name) -> use unweighted station presence kernel.
    st = gpd.read_file(f"{RAW}/N02/UTF-8/N02-23_Station.geojson")
    poly = gpd.read_file(f"{RAW}/study_polygon.geojson").geometry.iloc[0]
    st = st[st.intersects(poly.buffer(0.01))].copy()
    print("stations in/near area:", len(st))
    st_xy = np.c_[st.geometry.centroid.x, st.geometry.centroid.y]
    edges["k_station"] = kernel(st_xy, np.ones(len(st_xy)))

    # OSM POIs
    pois = gpd.read_file(f"{RAW}/osm_pois.geojson") if os.path.exists(f"{RAW}/osm_pois.geojson") else None
    for name, w in [("pois_nightlife", 1.0), ("pois_hotel_hosp", 0.8),
                    ("pois_transit", 0.5), ("pois_taxi_stands", 1.5)]:
        p = f"{RAW}/osm_{name}.geojson"
        if os.path.exists(p):
            f = gpd.read_file(p)
            f = f[f.intersects(poly.buffer(0.02))]
            xy = np.c_[f.geometry.centroid.x, f.geometry.centroid.y]
            edges[f"k_{name}"] = kernel(xy, np.full(len(xy), w))
        else:
            edges[f"k_{name}"] = 0.0

    # taxi-stand proximity (binary, 100m)
    pts = gpd.read_file(f"{RAW}/osm_pois_taxi_stands.geojson") if os.path.exists(f"{RAW}/osm_pois_taxi_stands.geojson") else None
    if pts is not None and len(pts):
        txy = np.c_[pts.geometry.centroid.x, pts.geometry.centroid.y]
        tree = cKDTree(to_m(txy)); d, _ = tree.query(mid_m)
        edges["stand100"] = (d <= 100).astype(float)
    else:
        edges["stand100"] = 0.0

    # ---------- demand field ----------
    z = lambda s: (s - s.mean()) / (s.std() + 1e-12)
    D = (np.log1p(edges.k_station) * 1.0 + np.log1p(edges.k_pois_nightlife) * 0.8
         + np.log1p(edges.k_pois_hotel_hosp) * 0.6 + np.log1p(edges.k_pois_transit) * 0.4
         + edges.w_road * 1.0 + np.log1p(edges.deg) * 0.3)
    edges["D"] = D
    # nightlife context share (drives temporal profile mixing)
    nl = z(np.log1p(edges.k_pois_nightlife))
    edges["nl_share"] = 1 / (1 + np.exp(-nl))  # 0..1

    def temporal_mult(row, wd, hour):
        mix = row.nl_share
        p = (1 - mix) * BASE_P[hour] + mix * NIGHT_P[hour]
        if wd == "weekend":
            p *= (1 - mix) + mix * WKND_NIGHT_BOOST
        return p

    for per in PERIODS:
        P = edges.apply(lambda r: temporal_mult(r, per["weekday"], per["hour"]), axis=1)
        F = edges.w_road.clip(lower=0.05) * (0.3 + edges.D) * P
        edges[f"F_{per['id']}"] = F

    # ---------- accessibility specifications ----------
    # A: flow-only
    # B: flow + road suitability (class, hail feasibility, intersection, taxi stand)
    # C: B + urban context (POI/station kernels already in F via D -> add explicit context terms)
    SUIT = z(edges.w_road) + 0.5 * z(np.log1p(edges.deg)) + 0.8 * edges.stand100
    edges["suitability"] = SUIT
    CTX = z(np.log1p(edges.k_station)) + 0.6 * z(np.log1p(edges.k_pois_nightlife)) \
        + 0.5 * z(np.log1p(edges.k_pois_hotel_hosp))
    edges["context"] = CTX
    for per in PERIODS:
        f = edges[f"F_{per['id']}"]
        edges[f"A_A_{per['id']}"] = z(np.log1p(f))
        edges[f"A_B_{per['id']}"] = z(z(np.log1p(f)) + 0.5 * SUIT)
        edges[f"A_C_{per['id']}"] = z(z(np.log1p(f)) + 0.5 * SUIT + 0.4 * CTX)
        # flow-only optimum reference
    edges.loc[~edges.hail_ok, [c for c in edges.columns if c.startswith("A_")]] = np.nan

    if not SUF:
        edges.drop(columns=["mid"]).to_file(f"{PROC}/segments.geojson", driver="GeoJSON")
    keep = ["u", "v", "key", "length", "highway1", "w_road", "hail_ok", "lanes_n", "deg",
            "mx", "my", "k_station", "k_pois_nightlife", "k_pois_hotel_hosp",
            "k_pois_transit", "k_pois_taxi_stands", "stand100", "D", "nl_share",
            "suitability", "context"] + [c for c in edges.columns if c.startswith(("F_", "A_"))]
    edges[keep].to_parquet(f"{PROC}/segments{SUF}.parquet")
    # ward membership of edge midpoints
    wards = {}
    for w in ["Chiyoda", "Chuo", "Minato", "Shinjuku", "Shibuya"]:
        wards[w] = ox.geocode_to_gdf(f"{w}, Tokyo, Japan").geometry.iloc[0]
    def ward_of(x, y):
        for n, p_ in wards.items():
            if p_.contains(Point(x, y)): return n
        return "other"
    edges["ward"] = [ward_of(x, y) for x, y in mid_xy]
    edges[["u", "v", "key", "ward"]].to_parquet(f"{PROC}/edge_ward.parquet")
    print("segments:", len(edges), "| hail_ok:", int(edges.hail_ok.sum()))

if __name__ == "__main__":
    build()
