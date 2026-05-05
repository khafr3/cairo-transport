"""
Cairo Smart Transportation System - Core Algorithms
CSE112 - Design and Analysis of Algorithms
"""

import heapq
import math
from collections import defaultdict
from functools import lru_cache

# ============================================================
# DATA LOADING - Cairo Network from Project Provided Data
# ============================================================

NEIGHBORHOODS = {
    1:  {"name": "Maadi",                     "pop": 250000, "type": "Residential",  "x": 31.25, "y": 29.96},
    2:  {"name": "Nasr City",                 "pop": 500000, "type": "Mixed",         "x": 31.34, "y": 30.06},
    3:  {"name": "Downtown Cairo",            "pop": 100000, "type": "Business",      "x": 31.24, "y": 30.04},
    4:  {"name": "New Cairo",                 "pop": 300000, "type": "Residential",   "x": 31.47, "y": 30.03},
    5:  {"name": "Heliopolis",                "pop": 200000, "type": "Mixed",         "x": 31.32, "y": 30.09},
    6:  {"name": "Zamalek",                   "pop":  50000, "type": "Residential",   "x": 31.22, "y": 30.06},
    7:  {"name": "6th October City",          "pop": 400000, "type": "Mixed",         "x": 30.98, "y": 29.93},
    8:  {"name": "Giza",                      "pop": 550000, "type": "Mixed",         "x": 31.21, "y": 29.99},
    9:  {"name": "Mohandessin",               "pop": 180000, "type": "Business",      "x": 31.20, "y": 30.05},
    10: {"name": "Dokki",                     "pop": 220000, "type": "Mixed",         "x": 31.21, "y": 30.03},
    11: {"name": "Shubra",                    "pop": 450000, "type": "Residential",   "x": 31.24, "y": 30.11},
    12: {"name": "Helwan",                    "pop": 350000, "type": "Industrial",    "x": 31.33, "y": 29.85},
    13: {"name": "New Admin Capital",         "pop":  50000, "type": "Government",    "x": 31.80, "y": 30.02},
    14: {"name": "Al Rehab",                  "pop": 120000, "type": "Residential",   "x": 31.49, "y": 30.06},
    15: {"name": "Sheikh Zayed",              "pop": 150000, "type": "Residential",   "x": 30.94, "y": 30.01},
}

FACILITIES = {
    "F1":  {"name": "Cairo Int'l Airport",    "type": "Airport",      "x": 31.41, "y": 30.11},
    "F2":  {"name": "Ramses Railway Station", "type": "Transit Hub",  "x": 31.25, "y": 30.06},
    "F3":  {"name": "Cairo University",       "type": "Education",    "x": 31.21, "y": 30.03},
    "F4":  {"name": "Al-Azhar University",    "type": "Education",    "x": 31.26, "y": 30.05},
    "F5":  {"name": "Egyptian Museum",        "type": "Tourism",      "x": 31.23, "y": 30.05},
    "F6":  {"name": "Cairo Int'l Stadium",    "type": "Sports",       "x": 31.30, "y": 30.07},
    "F7":  {"name": "Smart Village",          "type": "Business",     "x": 30.97, "y": 30.07},
    "F8":  {"name": "Cairo Festival City",    "type": "Commercial",   "x": 31.40, "y": 30.03},
    "F9":  {"name": "Qasr El Aini Hospital",  "type": "Medical",      "x": 31.23, "y": 30.03},
    "F10": {"name": "Maadi Military Hospital","type": "Medical",      "x": 31.25, "y": 29.95},
}

# Existing roads: (from, to, distance_km, capacity_veh_per_hr, condition_1_10)
EXISTING_ROADS = [
    (1, 3, 8.5, 3000, 7), (1, 8, 6.2, 2500, 6),
    (2, 3, 5.9, 2800, 8), (2, 5, 4.0, 3200, 9),
    (3, 5, 6.1, 3500, 7), (3, 6, 3.2, 2000, 8),
    (3, 9, 4.5, 2600, 6), (3, 10, 3.8, 2400, 7),
    (4, 2, 15.2, 3800, 9),(4, 14, 5.3, 3000, 10),
    (5, 11, 7.9, 3100, 7),(6, 9, 2.2, 1800, 8),
    (7, 8, 24.5, 3500, 8),(7, 15, 9.8, 3000, 9),
    (8, 10, 3.3, 2200, 7),(8, 12, 14.8, 2600, 5),
    (9, 10, 2.1, 1900, 7),(10, 11, 8.7, 2400, 6),
    (11,"F2",3.6, 2200, 7),(12, 1, 12.7, 2800, 6),
    (13, 4, 45.0,4000,10),(14,13,35.5, 3800, 9),
    (15, 7, 9.8, 3000, 9),("F1",5,7.5,3500,9),
    ("F1",2,9.2,3200,8),  ("F2",3,2.5,2000,7),
    ("F7",15,8.3,2800,8), ("F8",4,6.1,3000,9),
    # Facility connections
    (3, "F9", 1.2, 1500, 8), (1, "F10", 1.8, 1200, 7),
    (8, "F3", 2.1, 1800, 8), (3, "F4", 1.5, 1600, 8),
    (3, "F5", 0.8, 1000, 9), (2, "F6", 2.3, 2000, 8),
    (7, "F7", 3.2, 2200, 9), (4, "F8", 2.8, 2500, 9),
]

# Potential new roads: (from, to, distance_km, capacity, cost_million_EGP)
POTENTIAL_ROADS = [
    (1, 4, 22.8, 4000, 450),  (1, 14, 25.3, 3800, 500),
    (2, 13, 48.2, 4500, 950), (3, 13, 56.7, 4500, 1100),
    (5, 4, 16.8, 3500, 320),  (6, 8, 7.5, 2500, 150),
    (7, 13, 82.3, 4000, 1600),(9, 11, 6.9, 2800, 140),
    (10,"F7",27.4,3200,550),  (11, 13, 62.1, 4200, 1250),
    (12, 14, 30.5, 3600, 610),(14, 5, 18.2, 3300, 360),
    (15, 9, 22.7, 3000, 450), ("F1",13,40.2,4000,800),
    ("F7",9,26.8,3200,540),
]

TRAFFIC_PATTERNS = {
    "1-3":   {"morning": 2800, "afternoon": 1500, "evening": 2600, "night": 800},
    "1-8":   {"morning": 2200, "afternoon": 1200, "evening": 2100, "night": 600},
    "2-3":   {"morning": 2700, "afternoon": 1400, "evening": 2500, "night": 700},
    "2-5":   {"morning": 3000, "afternoon": 1600, "evening": 2800, "night": 650},
    "3-5":   {"morning": 3200, "afternoon": 1700, "evening": 3100, "night": 800},
    "3-6":   {"morning": 1800, "afternoon": 1400, "evening": 1900, "night": 500},
    "3-9":   {"morning": 2400, "afternoon": 1300, "evening": 2200, "night": 550},
    "3-10":  {"morning": 2300, "afternoon": 1200, "evening": 2100, "night": 500},
    "4-2":   {"morning": 3600, "afternoon": 1800, "evening": 3300, "night": 750},
    "4-14":  {"morning": 2800, "afternoon": 1600, "evening": 2600, "night": 600},
    "5-11":  {"morning": 2900, "afternoon": 1500, "evening": 2700, "night": 650},
    "6-9":   {"morning": 1700, "afternoon": 1300, "evening": 1800, "night": 450},
    "7-8":   {"morning": 3200, "afternoon": 1700, "evening": 3000, "night": 700},
    "7-15":  {"morning": 2800, "afternoon": 1500, "evening": 2600, "night": 600},
    "8-10":  {"morning": 2000, "afternoon": 1100, "evening": 1900, "night": 450},
    "8-12":  {"morning": 2400, "afternoon": 1300, "evening": 2200, "night": 500},
    "9-10":  {"morning": 1800, "afternoon": 1200, "evening": 1700, "night": 400},
    "10-11": {"morning": 2200, "afternoon": 1300, "evening": 2100, "night": 500},
    "11-F2": {"morning": 2100, "afternoon": 1200, "evening": 2000, "night": 450},
    "12-1":  {"morning": 2600, "afternoon": 1400, "evening": 2400, "night": 550},
    "13-4":  {"morning": 3800, "afternoon": 2000, "evening": 3500, "night": 800},
    "14-13": {"morning": 3600, "afternoon": 1900, "evening": 3300, "night": 750},
    "15-7":  {"morning": 2800, "afternoon": 1500, "evening": 2600, "night": 600},
    "F1-5":  {"morning": 3300, "afternoon": 2200, "evening": 3100, "night": 1200},
    "F1-2":  {"morning": 3000, "afternoon": 2000, "evening": 2800, "night": 1100},
    "F2-3":  {"morning": 1900, "afternoon": 1600, "evening": 1800, "night": 900},
    "F7-15": {"morning": 2600, "afternoon": 1500, "evening": 2400, "night": 550},
    "F8-4":  {"morning": 2800, "afternoon": 1600, "evening": 2600, "night": 600},
    # Facility connections
    "3-F9":  {"morning": 1400, "afternoon": 800, "evening": 1300, "night": 300},
    "1-F10": {"morning": 1100, "afternoon": 600, "evening": 1000, "night": 250},
    "8-F3":  {"morning": 1700, "afternoon": 900, "evening": 1600, "night": 400},
    "3-F4":  {"morning": 1500, "afternoon": 800, "evening": 1400, "night": 350},
    "3-F5":  {"morning": 900, "afternoon": 500, "evening": 850, "night": 200},
    "2-F6":  {"morning": 1900, "afternoon": 1000, "evening": 1800, "night": 450},
    "7-F7":  {"morning": 2100, "afternoon": 1100, "evening": 2000, "night": 500},
    "4-F8":  {"morning": 2400, "afternoon": 1300, "evening": 2300, "night": 550},
}

METRO_LINES = {
    "M1": {"name": "Line 1 (Helwan-New Marg)", "stations": [12,1,3,"F2",11],    "daily_passengers": 1500000},
    "M2": {"name": "Line 2 (Shubra-Giza)",     "stations": [11,"F2",3,10,8],   "daily_passengers": 1200000},
    "M3": {"name": "Line 3 (Airport-Imbaba)",  "stations": ["F1",5,2,3,9],     "daily_passengers":  800000},
}

BUS_ROUTES = {
    "B1":  {"stops": [1,3,6,9],         "buses": 25, "daily_passengers": 35000},
    "B2":  {"stops": [7,15,8,10,3],     "buses": 30, "daily_passengers": 42000},
    "B3":  {"stops": [2,5,"F1"],        "buses": 20, "daily_passengers": 28000},
    "B4":  {"stops": [4,14,2,3],        "buses": 22, "daily_passengers": 31000},
    "B5":  {"stops": [8,12,1],          "buses": 18, "daily_passengers": 25000},
    "B6":  {"stops": [11,5,2],          "buses": 24, "daily_passengers": 33000},
    "B7":  {"stops": [13,4,14],         "buses": 15, "daily_passengers": 21000},
    "B8":  {"stops": ["F7",15,7],       "buses": 12, "daily_passengers": 17000},
    "B9":  {"stops": [1,8,10,9,6],      "buses": 28, "daily_passengers": 39000},
    "B10": {"stops": ["F8",4,2,5],      "buses": 20, "daily_passengers": 28000},
}

# ============================================================
# GRAPH BUILDER
# ============================================================

def build_graph(roads=None, time_period="afternoon"):
    """Build adjacency list with time-aware weights."""
    if roads is None:
        roads = EXISTING_ROADS
    graph = defaultdict(list)
    for road in roads:
        u, v, dist, cap, cond = road
        # time-dependent multiplier from traffic patterns
        key = f"{u}-{v}"
        rev_key = f"{v}-{u}"
        pattern = TRAFFIC_PATTERNS.get(key) or TRAFFIC_PATTERNS.get(rev_key)
        if pattern:
            flow = pattern.get(time_period, pattern["afternoon"])
            # congestion ratio -> travel time multiplier
            congestion = min(flow / cap, 1.0)
            time_weight = dist * (1 + 2 * congestion)
        else:
            time_weight = dist
        graph[u].append((v, dist, time_weight, cap, cond))
        graph[v].append((u, dist, time_weight, cap, cond))
    return graph

# ============================================================
# A. MINIMUM SPANNING TREE — Kruskal's Algorithm
# ============================================================

class UnionFind:
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}
        self.rank   = {n: 0  for n in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


def kruskal_mst(include_potential=False):
    """
    Kruskal's MST with population-priority weighting.
    Critical facilities (hospitals, government) get priority edges.
    Time Complexity: O(E log E)
    Space Complexity: O(V + E)
    """
    all_roads = list(EXISTING_ROADS)
    if include_potential:
        # Convert potential roads to same format (add dummy condition=8)
        for r in POTENTIAL_ROADS:
            all_roads.append((r[0], r[1], r[2], r[3], 8))

    # Collect all node IDs
    nodes = set()
    for r in all_roads:
        nodes.add(str(r[0]))
        nodes.add(str(r[1]))

    def edge_weight(road):
        u, v, dist, cap, cond = road
        # Population priority: lower weight = higher priority connection
        pop_u = NEIGHBORHOODS.get(u, {}).get("pop", 50000) if isinstance(u, int) else 50000
        pop_v = NEIGHBORHOODS.get(v, {}).get("pop", 50000) if isinstance(v, int) else 50000
        avg_pop = (pop_u + pop_v) / 2
        # Critical facility bonus
        is_critical = False
        for fid in [u, v]:
            if isinstance(fid, str) and fid in FACILITIES:
                if FACILITIES[fid]["type"] in ["Medical", "Government", "Transit Hub"]:
                    is_critical = True
        pop_factor = 1 - (avg_pop / 600000) * 0.4  # high pop = lower weight
        crit_factor = 0.7 if is_critical else 1.0
        condition_factor = (11 - cond) / 10  # poor condition = higher weight
        return dist * pop_factor * crit_factor * condition_factor

    sorted_roads = sorted(all_roads, key=edge_weight)
    uf = UnionFind(nodes)
    mst_edges = []
    total_cost = 0

    for road in sorted_roads:
        u, v, dist, cap, cond = road
        su, sv = str(u), str(v)
        if uf.union(su, sv):
            mst_edges.append(road)
            total_cost += dist

    return mst_edges, total_cost


# ============================================================
# B1. DIJKSTRA'S ALGORITHM — Standard Route Planning
# ============================================================

def dijkstra(graph, source, target=None, weight_idx=1):
    """
    Dijkstra's shortest path algorithm.
    weight_idx: 1=distance, 2=time_weight
    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """
    dist = defaultdict(lambda: float('inf'))
    dist[source] = 0
    prev = {}
    pq = [(0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if target and u == target:
            break
        for edge in graph[u]:
            v = edge[0]
            w = edge[weight_idx]
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    # Reconstruct path
    def get_path(t):
        path = []
        while t in prev:
            path.append(t)
            t = prev[t]
        path.append(source)
        return list(reversed(path))

    if target:
        path = get_path(target) if target in prev or target == source else []
        return dist[target], path
    return dict(dist), prev


def dijkstra_time_aware(source, target, time_period="morning"):
    """Dijkstra with time-varying traffic weights."""
    graph = build_graph(time_period=time_period)
    return dijkstra(graph, source, target, weight_idx=2)


# ============================================================
# B2. A* SEARCH — Emergency Vehicle Routing
# ============================================================

def get_coords(node_id):
    """Get geographic coordinates for heuristic."""
    if isinstance(node_id, int) and node_id in NEIGHBORHOODS:
        n = NEIGHBORHOODS[node_id]
        return n["x"], n["y"]
    if isinstance(node_id, str) and node_id in FACILITIES:
        f = FACILITIES[node_id]
        return f["x"], f["y"]
    return None, None


def haversine_heuristic(a, b):
    """Great-circle distance heuristic (km)."""
    x1, y1 = get_coords(a)
    x2, y2 = get_coords(b)
    if x1 is None or x2 is None:
        return 0
    # Simplified Euclidean in degrees * ~111km/degree
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * 111


def astar(source, target, time_period="morning", emergency=True):
    """
    A* search for emergency vehicle routing.
    Uses geographic heuristic to guide search toward target.
    Time Complexity: O(E log V) best case
    Space Complexity: O(V)
    """
    graph = build_graph(time_period=time_period)

    g_score = defaultdict(lambda: float('inf'))
    g_score[source] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[source] = haversine_heuristic(source, target)

    open_set = [(f_score[source], source)]
    came_from = {}
    closed = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            return g_score[target], list(reversed(path))

        if current in closed:
            continue
        closed.add(current)

        for edge in graph[current]:
            neighbor = edge[0]
            if neighbor in closed:
                continue
            # Emergency vehicles use distance (not congested time)
            weight = edge[1] if emergency else edge[2]
            tentative_g = g_score[current] + weight

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + haversine_heuristic(neighbor, target)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return float('inf'), []


# ============================================================
# C. DYNAMIC PROGRAMMING — Public Transit Scheduling
# ============================================================

def dp_bus_scheduling(total_buses=214, routes=None):
    """
    DP solution: allocate buses across routes to maximize passenger coverage.
    Uses 0/1 knapsack variant.
    Time Complexity: O(R * B) where R=routes, B=buses
    Space Complexity: O(R * B)
    """
    if routes is None:
        routes = [
            {"id": rid, "min_buses": max(1, data["buses"] // 3),
             "max_buses": data["buses"] * 2,
             "passengers_per_bus": data["daily_passengers"] // data["buses"]}
            for rid, data in BUS_ROUTES.items()
        ]

    n = len(routes)
    # dp[i][b] = max passengers served using first i routes with b buses
    dp = [[0] * (total_buses + 1) for _ in range(n + 1)]
    # Keep track of choices for traceback
    choice = [[0] * (total_buses + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        r = routes[i - 1]
        for b in range(total_buses + 1):
            # Don't assign extra to this route
            dp[i][b] = dp[i-1][b]
            choice[i][b] = 0  # 0 means no buses assigned to this route
            # Try assigning k buses to route i
            for k in range(r["min_buses"], min(r["max_buses"], b) + 1):
                val = dp[i-1][b-k] + k * r["passengers_per_bus"]
                if val > dp[i][b]:
                    dp[i][b] = val
                    choice[i][b] = k

    # Traceback
    allocation = {}
    b = total_buses
    for i in range(n, 0, -1):
        r = routes[i - 1]
        allocated = choice[i][b]
        allocation[r["id"]] = allocated
        b -= allocated

    return dp[n][total_buses], allocation


def dp_road_maintenance(budget_million=500):
    """
    DP resource allocation for road maintenance.
    Maximize road condition improvement within budget.
    Time Complexity: O(R * Budget)
    Space Complexity: O(R * Budget)
    """
    # Roads needing maintenance (condition < 7)
    poor_roads = [(f"{r[0]}-{r[1]}", r[4], r[2]) for r in EXISTING_ROADS if r[4] < 7]

    # Maintenance options per road: cost (M EGP) -> condition improvement
    maintenance_options = []
    for road_id, cond, dist in poor_roads:
        # cost ≈ distance * (10-condition) * 2 M EGP, improvement = (10-cond)/2
        cost = int(dist * (10 - cond) * 2)
        improvement = (10 - cond) * dist  # weighted improvement
        maintenance_options.append({"id": road_id, "cost": cost, "value": improvement, "cond": cond})

    n = len(maintenance_options)
    B = budget_million
    dp = [[0.0] * (B + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = maintenance_options[i - 1]
        for b in range(B + 1):
            dp[i][b] = dp[i-1][b]
            if item["cost"] <= b:
                dp[i][b] = max(dp[i][b], dp[i-1][b - item["cost"]] + item["value"])

    # Traceback
    selected = []
    b = B
    for i in range(n, 0, -1):
        item = maintenance_options[i - 1]
        if b >= item["cost"] and dp[i][b] == dp[i-1][b - item["cost"]] + item["value"]:
            selected.append(item)
            b -= item["cost"]

    return dp[n][B], selected, maintenance_options


# ============================================================
# C2. MEMOIZED ROUTE PLANNING
# ============================================================

_route_cache = {}

def memoized_shortest_path(source, target, time_period="afternoon"):
    """Route planning with memoization to avoid recomputation."""
    key = (source, target, time_period)
    if key not in _route_cache:
        _route_cache[key] = dijkstra_time_aware(source, target, time_period)
    return _route_cache[key]


# ============================================================
# D. GREEDY — Traffic Signal Optimization
# ============================================================

def greedy_traffic_signals(time_period="morning"):
    """
    Greedy approach: assign green-light priority to roads with highest
    congestion ratio (flow/capacity) at major intersections.
    Time Complexity: O(I * R log R) where I=intersections, R=roads per intersection
    Space Complexity: O(I)
    """
    # Build intersection -> roads mapping
    intersections = defaultdict(list)
    for road_id, pattern in TRAFFIC_PATTERNS.items():
        parts = road_id.split("-")
        if len(parts) == 2:
            u, v = parts[0], parts[1]
            # Try to get capacity from existing roads
            cap = 2500  # default
            for r in EXISTING_ROADS:
                if str(r[0]) == u and str(r[1]) == v:
                    cap = r[3]
                    break
            flow = pattern.get(time_period, 1500)
            congestion_ratio = flow / cap
            intersections[u].append({"to": v, "flow": flow, "cap": cap, "ratio": congestion_ratio, "road": road_id})
            intersections[v].append({"to": u, "flow": flow, "cap": cap, "ratio": congestion_ratio, "road": road_id})

    signal_plan = {}
    for node, roads in intersections.items():
        # Greedy: sort by congestion ratio descending, assign green time proportionally
        sorted_roads = sorted(roads, key=lambda x: x["ratio"], reverse=True)
        total_ratio = sum(r["ratio"] for r in sorted_roads)
        cycle_time = 120  # seconds total cycle

        signal_plan[node] = []
        for r in sorted_roads:
            green_time = int((r["ratio"] / total_ratio) * cycle_time) if total_ratio > 0 else 30
            signal_plan[node].append({
                "direction": r["to"],
                "green_seconds": green_time,
                "congestion_ratio": round(r["ratio"], 3),
                "status": "CRITICAL" if r["ratio"] > 0.85 else "HIGH" if r["ratio"] > 0.7 else "NORMAL"
            })

    return signal_plan


def greedy_emergency_preemption(emergency_location, target_facility, time_period="morning"):
    """
    Greedy preemption: find intersections on emergency route and
    switch all signals to GREEN for emergency vehicle.
    """
    dist, path = astar(emergency_location, target_facility, time_period, emergency=True)
    signal_plan = greedy_traffic_signals(time_period)
    preemption_plan = []

    for node in path:
        node_key = str(node)
        if node_key in signal_plan:
            preemption_plan.append({
                "intersection": node_key,
                "action": "ALL GREEN for emergency",
                "normal_signals": signal_plan[node_key]
            })

    return path, dist, preemption_plan


# ============================================================
# UTILITY — Get node name
# ============================================================

def get_name(node_id):
    if isinstance(node_id, int) and node_id in NEIGHBORHOODS:
        return NEIGHBORHOODS[node_id]["name"]
    if isinstance(node_id, str) and node_id in FACILITIES:
        return FACILITIES[node_id]["name"]
    return str(node_id)


def format_path(path):
    return " → ".join(get_name(n) for n in path)


# ============================================================
# QUICK TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Cairo Smart Transportation System")
    print("=" * 60)

    # MST
    mst, cost = kruskal_mst()
    print(f"\n[MST] Kruskal's Algorithm")
    print(f"  Edges in MST: {len(mst)}")
    print(f"  Total network length: {cost:.1f} km")

    # Dijkstra
    graph = build_graph(time_period="morning")
    d, path = dijkstra(graph, 2, 12, weight_idx=1)
    print(f"\n[DIJKSTRA] Nasr City → Helwan")
    print(f"  Distance: {d:.1f} km | Path: {format_path(path)}")

    # A*
    dist_astar, path_astar = astar("F9", 12, "morning")
    print(f"\n[A*] Qasr El Aini Hospital → Helwan (Emergency)")
    print(f"  Distance: {dist_astar:.1f} km | Path: {format_path(path_astar)}")

    # DP
    passengers, allocation = dp_bus_scheduling()
    print(f"\n[DP] Bus Scheduling Optimization")
    print(f"  Max daily passengers: {passengers:,}")

    # Maintenance DP
    improvement, selected, _ = dp_road_maintenance(500)
    print(f"\n[DP] Road Maintenance (Budget: 500M EGP)")
    print(f"  Roads selected: {len(selected)}")

    # Greedy signals
    signals = greedy_traffic_signals("morning")
    print(f"\n[GREEDY] Traffic Signal Optimization")
    print(f"  Intersections optimized: {len(signals)}")

    print("\n✅ All algorithms executed successfully!")
