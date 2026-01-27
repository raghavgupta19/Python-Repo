import sqlite3
import heapq

def calculate_fare(distance):
    if distance <= 2:
        return 10
    elif distance <= 5:
        return 20
    elif distance <= 12:
        return 30
    elif distance <= 21:
        return 40
    elif distance <= 32:
        return 50
    else:
        return 60


def build_graph():
    conn = sqlite3.connect("metro_project.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT from_station, to_station, distance_km, time_min
        FROM station_connections
    """)
    rows = cur.fetchall()
    conn.close()

    graph = {}

    for src, dst, dist, time in rows:
        graph.setdefault(src, []).append((dst, dist, time))
        graph.setdefault(dst, []).append((src, dist, time))  # bidirectional

    return graph


def shortest_route(source, destination):
    graph = build_graph()

    # priority queue -> (distance, time, current_station)
    pq = [(0, 0, source)]

    # visited: station -> (distance, time)
    visited = {}

    # parent map to reconstruct path
    parent = {source: None}

    while pq:
        dist, time, station = heapq.heappop(pq)

        if station in visited:
            continue

        visited[station] = (dist, time)

        if station == destination:
            # reconstruct path
            path = []
            cur = destination
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()

            fare = calculate_fare(dist)
            return path, dist, time, fare

        for neighbor, d, t in graph.get(station, []):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = station
                heapq.heappush(
                    pq,
                    (dist + d, time + t, neighbor)
                )

    return None


if __name__ == "__main__":
    source = "Samaypur Badli"
    destination = "Jahangirpuri"

    result = shortest_route(source, destination)

    if result:
        path, distance, time, fare = result

        print(f"\n🚇 Route: {source} → {destination}\n")
        print("🛤️ Full Path:")
        print("  " + "  →  ".join(path))

        print(f"\n📏 Total Distance: {distance:.2f} km")
        print(f"⏱️ Total Time: {time} minutes")
        print(f"💰 Fare: ₹{fare}")
    else:
        print("❌ Route not found")
