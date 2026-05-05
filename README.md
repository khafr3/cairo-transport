# 🚦 Cairo Smart Transportation Network Optimization
### CSE112 — Design & Analysis of Algorithms | Alamein International University

> A comprehensive transportation optimization system for Greater Cairo implementing graph algorithms, dynamic programming, greedy approaches, and ML-based traffic prediction.

---

## 📋 Project Overview

This system solves real urban transportation challenges for Greater Cairo using:
- **15 districts** and **10 key facilities** modeled as graph nodes
- **28 existing roads** + **15 potential new roads** as weighted edges
- **4 algorithm families** covering all CSE112 requirements

---

## 🧮 Algorithms Implemented

| Algorithm | Purpose | Complexity |
|-----------|---------|-----------|
| **Kruskal's MST** | Infrastructure network design | O(E log E) |
| **Dijkstra's** | Shortest route planning | O((V+E) log V) |
| **A\* Search** | Emergency vehicle routing | O(E log V) |
| **DP (Knapsack)** | Bus scheduling optimization | O(R × B) |
| **DP (Knapsack)** | Road maintenance allocation | O(R × Budget) |
| **Greedy** | Traffic signal timing | O(I × R log R) |
| **Linear Regression** | Traffic congestion prediction | O(n × features) |

---

## 🗂️ Project Structure

```
cairo_transport/
├── algorithms.py        # Core Python algorithms (all CSE112 requirements)
├── ml_traffic.py        # ML-based traffic prediction (Bonus)
├── index.html           # Interactive web dashboard (Demo)
├── Dockerfile           # Containerized deployment support
├── requirements.txt     # Optional Python dependencies
├── run_localhost.bat    # Local launch shortcut for Windows
├── .gitignore           # Repository ignore rules
├── .github/workflows/   # CI and deployment workflows
├── test_algorithms.py   # Automated test suite
├── README.md            # Project documentation
└── Technical_Report.md  # Report documentation
```

---

## 🚀 How to Run

### Option 1: Web Demo (Recommended)
Simply open `index.html` in any modern browser. No installation needed!

### Option 2: Local Web Server
```bash
cd "c:\\Users\\LENOVO\\Desktop\\cairo transport"
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

### Option 3: Windows Shortcut
Double-click `run_localhost.bat` to launch the same local server.

### Option 4: Docker Container
```bash
docker build -t cairo-transport .
docker run -p 8000:8000 cairo-transport
```
Then open `http://localhost:8000`.

### Option 5: Python Algorithms
```bash
# Requirements: Python 3.8+, no external packages needed
python algorithms.py
```

### Option 6: ML Module
```bash
# Optional: pip install scikit-learn (or use built-in pure Python model)
python ml_traffic.py
```

---

## 🗺️ System Features

### 1. Infrastructure Network Design (MST)
- Kruskal's algorithm with **population-priority weighting**
- Critical facilities (hospitals, government centers) weighted 30% lower → always connected
- Compare existing roads vs including potential new roads
- Cost analysis in km of road network

### 2. Traffic Flow Optimization (Dijkstra)
- Time-dependent edge weights: `w = distance × (1 + 2 × congestion_ratio)`
- Four time periods: morning rush, afternoon, evening rush, night
- Full all-pairs distance analysis from any source

### 3. Emergency Response Planning (A*)
- Haversine geographic heuristic: `h(n) = ||coords(n) - coords(goal)|| × 111 km`
- Emergency mode uses raw distances (vehicles have right-of-way)
- Signal preemption plan generated for every intersection on route
- Comparison: A* explores fewer nodes than Dijkstra on average

### 4. Public Transit Optimization (Dynamic Programming)
- **Bus scheduling**: 0/1 knapsack variant allocating buses across 10 routes
- **Road maintenance**: maximize condition improvement within EGP budget
- **Memoized routing**: cached shortest paths avoid recomputation

### 5. Traffic Signal Optimization (Greedy)
- Green time proportional to congestion ratio at each intersection
- 120-second cycle distributed across incoming roads
- Identifies CRITICAL (>85%), HIGH (70-85%), NORMAL (<70%) roads
- Analysis of suboptimal cases (cascade effects across intersections)

### 6. ML Traffic Prediction (Bonus ⭐)
- Linear regression with cyclic time encoding (sin/cos of hour)
- 6 features: hour, day type, capacity, hour_sin, hour_cos, road_id
- 24-hour congestion forecast for any road segment

---

## 📊 Data Sources

All data from **CSE112-Project Provided Data**:
- Geographic coordinates of 15 neighborhoods + 10 facilities
- 28 existing road connections (distance, capacity, condition)
- 15 potential new road proposals with construction costs
- Temporal traffic patterns (morning/afternoon/evening/night)
- Metro lines and bus route data with passenger counts

---

## 🎯 Bonus Features

| Bonus Item | Implementation |
|-----------|----------------|
| ML Traffic Prediction | Linear regression with cyclic encoding |
| Algorithm Comparison Visualizer | Side-by-side Dijkstra vs A* race |
| Interactive Web Demo | Full HTML/JS dashboard |
| GitHub Repository | This repo with full README |

---

## 📈 Performance Results

| Metric | Value |
|--------|-------|
| MST edges (existing roads) | 24 edges |
| MST total length | 168.7 km |
| Dijkstra avg nodes explored | 12-15 |
| A* avg nodes explored | 6-9 (fewer!) |
| DP bus optimization improvement | ~12% more passengers vs uniform allocation |
| ML model R² (test) | ~0.30 (built-in regression) |

---

## 👨‍💻 Technical Report

See `Technical_Report.md` for:
- System architecture and design decisions
- Detailed algorithm analysis with proofs
- Performance benchmarks with charts
- Challenges and solutions

---

## 📦 Deployment & Containerization

This project includes:
- `Dockerfile` for containerized deployment
- `run_localhost.bat` for one-click local launch on Windows
- GitHub Actions workflows for CI and GitHub Pages deployment

If you publish this repository to GitHub, the included `.github/workflows/pages-deploy.yml` can deploy the site to `gh-pages` automatically.

## 🔗 Links

- 🌐 **Local Demo:** `http://localhost:8000`
- 📁 **GitHub Repo:** Add your repository URL here after publishing
- 📄 **Report:** `Technical_Report.md` (or convert to PDF separately)

---

*CSE112 — Design and Analysis of Algorithms | Spring 2026 | Alamein International University*
