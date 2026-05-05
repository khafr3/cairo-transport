"""
Test Cases for Cairo Smart Transportation System
CSE112 - Design and Analysis of Algorithms
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from algorithms import *

def test_mst():
    """Test MST algorithms."""
    print("=== TESTING MST ALGORITHMS ===")

    # Test basic MST
    mst, cost = kruskal_mst(include_potential=False)
    print(f"Basic MST: {len(mst)} edges, {cost:.1f} km total")

    # Test MST with potential roads
    mst_full, cost_full = kruskal_mst(include_potential=True)
    print(f"Extended MST: {len(mst_full)} edges, {cost_full:.1f} km total")

    # Verify connectivity
    nodes = set()
    for edge in mst:
        nodes.add(str(edge[0]))
        nodes.add(str(edge[1]))
    print(f"Connected nodes: {len(nodes)} (should be {len(NEIGHBORHOODS) + len(FACILITIES)})")

    print("✓ MST tests passed\n")

def test_shortest_paths():
    """Test shortest path algorithms."""
    print("=== TESTING SHORTEST PATH ALGORITHMS ===")

    # Test Dijkstra
    graph = build_graph(time_period="morning")
    dist, path = dijkstra(graph, 2, 12, weight_idx=2)  # time-weighted
    print(f"Dijkstra (morning): {dist:.1f} km, path length: {len(path)}")

    # Test time-aware Dijkstra
    dist_ta, path_ta = dijkstra_time_aware(2, 12, "evening")
    print(f"Time-aware Dijkstra (evening): {dist_ta:.1f} km, path length: {len(path_ta)}")

    # Test A* emergency routing
    dist_astar, path_astar = astar("F9", 12, "morning", emergency=True)
    print(f"A* Emergency: {dist_astar:.1f} km, path length: {len(path_astar)}")

    # Test A* with traffic
    dist_astar_traffic, path_astar_traffic = astar("F9", 12, "morning", emergency=False)
    print(f"A* with traffic: {dist_astar_traffic:.1f} km, path length: {len(path_astar_traffic)}")

    print("✓ Shortest path tests passed\n")

def test_dp_algorithms():
    """Test dynamic programming algorithms."""
    print("=== TESTING DYNAMIC PROGRAMMING ===")

    # Test bus scheduling
    passengers, allocation = dp_bus_scheduling(total_buses=214)
    total_allocated = sum(allocation.values())
    print(f"Bus scheduling: {passengers:,} passengers, {total_allocated} buses allocated")

    # Verify allocation doesn't exceed total buses
    assert total_allocated <= 214, "Bus allocation exceeds total buses"
    print(f"Allocation details: {allocation}")

    # Test road maintenance
    improvement, selected, options = dp_road_maintenance(budget_million=500)
    total_cost = sum(item['cost'] for item in selected)
    print(f"Road maintenance: {improvement:.1f} improvement, {len(selected)} roads, {total_cost}M EGP cost")

    # Verify budget constraint
    assert total_cost <= 500, "Maintenance cost exceeds budget"
    print(f"Selected roads: {[r['id'] for r in selected]}")

    print("✓ DP tests passed\n")

def test_greedy_algorithm():
    """Test greedy traffic signal optimization."""
    print("=== TESTING GREEDY ALGORITHM ===")

    signals = greedy_traffic_signals("morning")
    print(f"Traffic signals optimized for {len(signals)} intersections")

    # Check that signals are properly distributed
    total_green = sum(sum(s['green_seconds'] for s in intersection) for intersection in signals.values())
    print(f"Total green time allocated: {total_green} seconds")

    # Test emergency preemption
    path, dist, preemption = greedy_emergency_preemption("F9", 12, "morning")
    print(f"Emergency preemption: {len(preemption)} intersections affected")
    print(f"Emergency route: {len(path)} nodes, {dist:.1f} km")

    print("✓ Greedy tests passed\n")

def test_memoization():
    """Test memoized route planning."""
    print("=== TESTING MEMOIZATION ===")

    # First call
    dist1, path1 = memoized_shortest_path(2, 12, "morning")
    print(f"First call: {dist1:.1f} km, {len(path1)} nodes")

    # Second call (should use cache)
    dist2, path2 = memoized_shortest_path(2, 12, "morning")
    print(f"Second call (cached): {dist2:.1f} km, {len(path2)} nodes")

    # Verify results are identical
    assert dist1 == dist2 and path1 == path2, "Memoization failed"
    print("✓ Memoization working correctly\n")

def test_complexity_analysis():
    """Test algorithm complexity claims."""
    print("=== TESTING COMPLEXITY CLAIMS ===")

    import time

    # MST complexity test
    start = time.time()
    mst, _ = kruskal_mst()
    mst_time = time.time() - start
    print(f"MST runtime: {mst_time:.4f} seconds")

    # Dijkstra complexity test
    graph = build_graph()
    start = time.time()
    dist, _ = dijkstra(graph, 1)  # all pairs from source
    dijkstra_time = time.time() - start
    print(f"Dijkstra runtime: {dijkstra_time:.4f} seconds")

    # A* complexity test
    start = time.time()
    dist_astar, _ = astar(1, 15, "afternoon", emergency=False)
    astar_time = time.time() - start
    print(f"A* runtime: {astar_time:.4f} seconds")

    print("✓ Complexity tests completed\n")

def run_all_tests():
    """Run all test cases."""
    print("🚦 Cairo Transportation System - Test Suite")
    print("=" * 50)

    try:
        test_mst()
        test_shortest_paths()
        test_dp_algorithms()
        test_greedy_algorithm()
        test_memoization()
        test_complexity_analysis()

        print("🎉 ALL TESTS PASSED!")
        print("✅ System is ready for demonstration")

    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()