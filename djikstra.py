import heapq

def max_bandwidth_path(graph, a, b):
    # Initialize max_bandwidth array with negative infinity for all centers except 'a'.
    max_bandwidth = {center: float('-inf') for center in graph}
    max_bandwidth[a] = float('inf')

    # Priority queue to keep track of centers to visit next (center, max_bandwidth).
    priority_queue = [(a, max_bandwidth[a])]

    while priority_queue:
        current_center, current_max_bandwidth = heapq.heappop(priority_queue)

        # If 'b' is reached, return the maximum bandwidth seen so far.
        if current_center == b:
            return current_max_bandwidth

        # Check neighbors of 'current_center'.
        for neighbor, edge_bandwidth in graph[current_center]:
            new_max_bandwidth = min(current_max_bandwidth, edge_bandwidth)
            
            # If a higher bandwidth is found to reach 'neighbor', update max_bandwidth and push it to the queue.
            if new_max_bandwidth > max_bandwidth[neighbor]:
                max_bandwidth[neighbor] = new_max_bandwidth
                heapq.heappush(priority_queue, (neighbor, new_max_bandwidth))

    # If no path is found from 'a' to 'b', return a message indicating that.
    return "No path found from 'a' to 'b'"

# Example usage:
graph = {
    'a': [('c', 10), ('b', 5)],
    'b': [('c', 8), ('d', 12)],
    'c': [('e', 7)],
    'd': [('e', 6)],
    'e': []
}

a = 'a'
b = 'e'
max_bandwidth = max_bandwidth_path(graph, a, b)
print(f"Maximum bandwidth from {a} to {b}: {max_bandwidth}")