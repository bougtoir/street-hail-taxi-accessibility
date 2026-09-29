# DATA SOURCE AUDIT

Raw snapshots persisted under `data/raw/`; machine-readable ledger in `data/raw/acquisition_ledger.jsonl` (URL, UTC access time, bytes, SHA-256). All data accessed 2026-09-29 UTC.

## Used sources

### 1. OpenStreetMap road network & POIs (via Overpass API / OSMnx 2.0.7)
- URL: https://overpass-api.de/ ; provider: OpenStreetMap contributors
- License: ODbL 1.0
- Geographic scope: union polygon of Chiyoda, Chuo, Minato, Shinjuku, Shibuya wards (5 central wards of Tokyo); `data/raw/study_polygon.geojson`
- Temporal scope: live snapshot (2026-09-29)
- Files: `osm_drive_graph.graphml` (12,791 nodes / 29,165 directed edges), `osm_walk_graph.graphml` (60,804 / 182,538), `osm_pois*.geojson` (transit stations, taxi stands, nightlife, hotel/hospital; 3,539 features)
- Variables used: highway class, one-way directionality (directed edges), length, lanes, node degree, POI types
- Enters model as: candidate segments, road-suitability terms, urban-attractor kernels, taxi-stand proximity, walking neighborhoods

### 2. MLIT National Land Numerical Information (国土数値情報) N02 railway stations, Tokyo
- URL: https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-23/N02-23_GML.zip
- Provider: Ministry of Land, Infrastructure, Transport and Tourism (MLIT)
- License: NLNI terms (free use with attribution for research; source notation required)
- Temporal scope: FY2023 survey (乗降客数), railway status as of survey year
- Files: `N02_tokyo_stations.zip` → `N02/UTF-8/N02-23_Station.geojson`; 329 stations intersecting study polygon (+buffer)
- Variables: station name (N02_005), operator (N02_004), line (N02_003), station code (N02_005c). CORRECTION (CEUS pass): the FY2023 N02 schema carries NO passenger-count field; N02_004 is the operator name. The earlier build mistakenly read N02_004 as passengers, leaving the station kernel empty (all zeros). Corrected to an unweighted station-presence kernel (329 stations) and the full pipeline was rebuilt.
- Enters model as: station-presence attractor term (unweighted 300 m Gaussian kernel)

### 3. Tokyo Taxi Center user-monitor survey FY2023 (タクシー利用者モニター調査 集計報告書)
- URL: https://www.tokyo-tc.or.jp/center/uploads/monitor_2024.pdf
- Provider: Tokyo Taxi Center (公益財団法人東京タクシーセンター)
- License: publicly posted report PDF; used as citable published statistics
- Temporal scope: FY2023 survey, n=2,662 responses
- Used variable: hourly distribution of taxi use (24 bins, 6:00–5:00) — digitized from the published histogram → `analysis/build_segments.py` BASE_P
- Enters model as: temporal multiplier P(h) on the taxi-flow prior; the only empirical temporal anchor
- Limitation: self-selected user monitors, not fleet volumes; used only as a *shape* prior, not absolute demand

### 4. Tokyo Hire-Taxi Association yearbook 東京のタクシー2025 (context statistics)
- URL: https://taxi-tokyo.or.jp/assets/pdf/datalibrary/hakusyo2025all.pdf
- Used for: fleet size (46,475 vehicles FY2024), special-ward transport volumes, occupancy/実車率 context in the manuscript
- Not a model input; background citation only

## Attempted and substituted

### CSIS Pseudo-PFLOW v3.0 business-traffic (taxi/freight) trajectories
- URL: https://pflow.csis.u-tokyo.ac.jp/
- Status: **INACCESSIBLE in this environment** — requires JoRAS account + joint-research application to CSIS; not a direct download. Not a license violation, an access barrier.
- Substitution: taxi-flow prior reconstructed from public attractors (station locations, POIs, road hierarchy) × published hourly taxi-use profile. Rationale: street-hail opportunity at segment level is dominated by where taxis circulate, which tracks road hierarchy and trip-generation attractors. Documented as the single largest modeling assumption; sensitivity analyses vary it (kernel bandwidth 150/300/500 m; specifications A/B/C).

### Proprietary/fleet data (excluded by design)
- No taxi-company GPS, ride-hail APIs, or crowdsourced data were sought or used (Phase 0 contract).

## Known limitations
- OSM coverage bias (minor roads/sidewalks under-mapped); walk graph approximates pedestrian paths.
- NLNI passenger counts are FY2023; OSM is a live snapshot (mild temporal mismatch).
- Monitor-survey hourly profile is demand-side sampling, not supply-side flow.
- Taxi stands are under-mapped in OSM for Tokyo (stand100 term is sparse).
