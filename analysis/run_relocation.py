#!/usr/bin/env python3
"""Phases 7-11: origin sampling, walking neighborhoods, relocation optimization,
baseline heuristics, temporal/spatial heterogeneity, sensitivity analyses."""
import os, math, json, numpy as np, pandas as pd, geopandas as gpd
import osmnx as ox, networkx as nx
from scipy.spatial import cKDTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, PROC, TAB = f"{ROOT}/data/raw", f"{ROOT}/data/processed", f"{ROOT}/tables"
os.makedirs(TAB, exist_ok=True)
SEED = 42
rng = np.random.default_rng(SEED)

LAT0 = math.radians(35.68)
def to_m(xy):
    xy = np.asarray(xy, float)
    return np.c_[xy[..., 0] * 111320 * math.cos(LAT0), xy[..., 1] * 110540]

RADII = [100, 200, 300, 500]
MODELS = ["A_A", "A_B", "A_C"]
PERIODS = [f"{wd}_{h:02d}" for wd in ["weekday", "weekend"] for h in [8, 13, 17, 21, 23]]
N_ORIGINS = 2000
N_RANDOM_DRAWS = 10
THRESHOLDS = [0.10, 0.25, 0.50, 1.00]

# ---------------- load ----------------
edges = pd.read_parquet(f"{PROC}/segments.parquet")
ew = pd.read_parquet(f"{PROC}/edge_ward.parquet")
edges = edges.merge(ew, on=["u", "v", "key"], how="left")
W = ox.load_graphml(f"{RAW}/osm_walk_graph.graphml")
wn = ox.graph_to_gdfs(W, edges=False)
W_und = W.to_undirected()
wn_xy = np.c_[wn.x, wn.y]
wn_m = to_m(wn_xy)
wn_ids = wn.index.to_numpy()

# walk KD-tree: node index -> position in wn_ids
pos_of = {n: i for i, n in enumerate(wn_ids)}

# candidate drive edges: hail_ok only
cand = edges[edges.hail_ok].reset_index(drop=True)
cand_m = to_m(np.c_[cand.mx, cand.my])
edge_tree = cKDTree(cand_m)

# nearest walk node to each candidate edge midpoint (for reachability test)
_, near_walk = cKDTree(wn_m).query(cand_m)  # index into wn_m

# origins: random candidate segments
orig_idx = rng.choice(len(cand), size=N_ORIGINS, replace=False)
origins = cand.iloc[orig_idx].reset_index(drop=True)

print("computing reachable sets for", len(origins), "origins")
if os.path.exists(f"{PROC}/reach.json"):
    with open(f"{PROC}/reach.json") as f:
        reach = [{int(k): v for k, v in r.items()} for r in json.load(f)]
    print("loaded cached reach sets")
else:
    reach = []  # per origin: {edge_idx: min_walk_dist}
    for i, orow in origins.iterrows():
        om = to_m([[orow.mx, orow.my]])[0]
        # nearest walk node
        _, wi = cKDTree(wn_m).query(om.reshape(1, -1)[0])
        start = wn_ids[wi]
        lengths = nx.single_source_dijkstra_path_length(W_und, start, cutoff=500, weight="length")
        node_ids = np.fromiter(lengths.keys(), dtype=np.int64)
        dists = np.fromiter(lengths.values(), dtype=float)
        # map walk nodes -> candidate edges within 25 m
        pts = wn_m[[pos_of[n] for n in node_ids]]
        pairs = edge_tree.query_ball_point(pts, r=25.0)
        edist = {}
        for j, elist in enumerate(pairs):
            for e in elist:
                d = dists[j]
                if e not in edist or d < edist[e]:
                    edist[e] = d
        reach.append(edist)
        if i % 400 == 0:
            print(" ", i)
    with open(f"{PROC}/reach.json", "w") as f:
        json.dump([{str(k): v for k, v in r.items()} for r in reach], f)

print("evaluating strategies")
records = []
rand = np.random.default_rng(SEED + 1)
for i, orow in origins.iterrows():
    edist = reach[i]
    eidx = np.fromiter(edist.keys(), dtype=int)
    edist_v = np.fromiter(edist.values(), dtype=float)
    for r in RADII:
        m = edist_v <= r
        if not m.any():
            continue
        ei, di = eidx[m], edist_v[m]
        c = cand.iloc[ei]
        for per in PERIODS:
            for model in MODELS:
                col = f"{model}_{per}"
                a0 = orow[col]
                vals = c[col].to_numpy()
                ok = np.isfinite(vals)
                if not ok.any() or not np.isfinite(a0):
                    continue
                ei2, di2, v2 = ei[ok], di[ok], vals[ok]
                best = int(np.argmax(v2))
                astar, dstar = v2[best], di2[best]
                # heuristics
                # random draws
                rv = rand.choice(v2, size=min(N_RANDOM_DRAWS, len(v2)), replace=False).mean()
                # nearest major road (w_road==1): naive heuristic = closest major segment
                maj = c.w_road.to_numpy()[ok] >= 0.99
                a_major = v2[maj].max() if maj.any() else np.nan
                a_nearmajor = v2[maj][np.argmin(di2[maj])] if maj.any() else np.nan
                best_is_major = bool(c.w_road.to_numpy()[ok][best] >= 0.99)
                # highest taxi-flow segment (= A_A optimum, equals optimizer when model=A_A)
                fa = c[f"A_A_{per}"].to_numpy()[ok]
                a_flow = fa.max() if np.isfinite(fa).any() else np.nan
                base = a0 if abs(a0) > 1e-6 else np.nan
                rec = {
                    "origin": i, "radius": r, "period": per, "model": model,
                    "ward": orow.ward, "A0": a0, "Astar": astar, "walk_m": dstar,
                    "G_A": astar - a0,
                    "RAG": (astar - a0) / abs(base) if np.isfinite(base) else np.nan,
                    "A_random": rv, "A_major": a_major, "A_nearmajor": a_nearmajor,
                    "best_is_major": best_is_major, "A_flow": a_flow,
                    "gain_random": rv - a0,
                    "gain_major": (a_major - a0) if np.isfinite(a_major) else np.nan,
                    "gain_nearmajor": (a_nearmajor - a0) if np.isfinite(a_nearmajor) else np.nan,
                    "gain_flow": (a_flow - a0) if np.isfinite(a_flow) else np.nan,
                }
                # distance-to-threshold on relative gain
                for t in THRESHOLDS:
                    need = a0 + t * abs(base) if np.isfinite(base) else np.nan
                    if np.isfinite(need):
                        hit = di2[v2 >= need]
                        rec[f"dist_p{int(t*100)}"] = float(hit.min()) if len(hit) else np.nan
                    else:
                        rec[f"dist_p{int(t*100)}"] = np.nan
                records.append(rec)
    if i % 400 == 0:
        print("  eval", i, len(records))

df = pd.DataFrame(records)
df.to_parquet(f"{PROC}/relocation_results.parquet")
print("rows", len(df))
df.to_csv(f"{TAB}/relocation_results.csv", index=False)
print("done")
