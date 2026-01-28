# 🚇 Delhi Metro Route, Distance & Fare Finder (Yellow Line)

## 📌 Project Overview

This project is a Delhi Metro Route Finder focused on the Yellow Line.
It models the metro network as a weighted graph, stores station and connectivity data in a SQLite database, and computes the shortest route, total distance, travel time, and fare between any two stations using Dijkstra’s Algorithm.

The project simulates a real-world metro navigation system and demonstrates concepts from Data Structures, Databases, and Algorithms using Python.

---

## 🎯 Key Features

- Stores metro station and connectivity data in SQLite
- Models stations as graph nodes and tracks as weighted edges
- Computes:
  - Complete station-by-station route
  - Total distance (km)
  - Total travel time (minutes)
  - Fare based on distance slabs
- Uses Dijkstra’s Algorithm to find the optimal route
- Modular design, easy to extend to more metro lines

---

## 🛠️ Technologies Used

- Python 3
- SQLite
- Pandas
- Requests
- Heapq (Priority Queue)
- Graph Algorithms

---

## 📁 Project Structure

Python Metro Project/
├── crawler.py
├── database_setup.py
├── create_connections.py
├── route_engine.py
├── yellow_line_detailed.csv
└── metro_project.db


---

## 🧠 Database Design

### 1️⃣ yellow_line_stations

Stores master station data.

| Column Name   | Description |
|--------------|-------------|
| station_name | Name of station |
| station_code | Station code |
| line         | Metro line |
| status       | Operational status |
| interchange  | Interchange flag |
| facilities   | Lift, escalator, parking |

---

### 2️⃣ station_connections

Stores graph edges (adjacent stations).

| Column Name   | Description |
|--------------|-------------|
| from_station | Source station |
| to_station   | Destination station |
| distance_km  | Distance in km |
| time_min     | Travel time (minutes) |
| line         | Metro line |

---

## 🗺️ Metro Graph Representation

Stations are represented as **nodes**, and connections as **edges with weights**.



## ⚙️ Algorithm Used

Dijkstra’s Algorithm is used to calculate the shortest path between stations.
Once the shortest distance to a station is finalized, it is not revisited.

---

## 💰 Sample Output

Route: Samaypur Badli → Jahangirpuri  
Distance: 3.90 km  
Time: 8 minutes  
Fare: ₹20

---

## 🎓 Learning Outcomes

- Graph representation of real-world systems
- Shortest path algorithms
- Database integration with Python
- Modular project design

---

## ⚠️ Disclaimer

This project is for academic and learning purposes only.
