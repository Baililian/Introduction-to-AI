import heapq

# ============================================================
#  A* ALGORITHM - Core Implementation
# ============================================================

def a_star(graph, heuristics, start, goal):
    """
    A* Search Algorithm
    f(n) = g(n) + h(n)
    g(n) = actual cost from start to current node
    h(n) = heuristic estimate from current node to goal
    """
    open_set = []
    heapq.heappush(open_set, (0 + heuristics[start], 0, start, [start]))
    closed_set = set()

    print(f"\n{'='*65}")
    print(f"  A* Search | Start: {start} | Goal: {goal}")
    print(f"{'='*65}")
    print(f"{'Step':<6} {'Node':<12} {'g(n)':<8} {'h(n)':<8} {'f(n)':<8} Path")
    print(f"{'-'*65}")

    step = 1

    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        h = heuristics[current]
        path_str = ' -> '.join(str(n) for n in path)
        print(f"{step:<6} {str(current):<12} {g:<8} {h:<8} {f:<8} {path_str}")
        step += 1

        if current == goal:
            print(f"\n  ✔ Goal reached!")
            print(f"  Path : {' -> '.join(str(n) for n in path)}")
            print(f"  Cost : {g}")
            print(f"{'='*65}\n")
            return path, g

        if current in closed_set:
            continue
        closed_set.add(current)

        for neighbor, cost in graph.get(current, []):
            if neighbor not in closed_set:
                new_g = g + cost
                new_f = new_g + heuristics[neighbor]
                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

    print("  ✘ No path found.")
    print(f"{'='*65}\n")
    return None, float('inf')


# ============================================================
#  BUILD GRAPH FROM USER INPUT  
# ============================================================

BACK = 'back'
QUIT = 'quit'

def prompt(msg):
    """Get input, support 'back' and 'quit' keywords."""
    val = input(msg).strip()
    if val.lower() == 'back':
        return BACK
    if val.lower() == 'quit':
        return QUIT
    return val

def build_graph():
    print("\n" + "#"*65)
    print("  A* ALGORITHM - Dynamic Graph Builder")
    print("  Type 'back' at any prompt to go to the previous step.")
    print("  Type 'quit' at any prompt to exit.")
    print("#"*65)

    step = 1  # tracks which step we're on

    nodes      = []
    graph      = {}
    heuristics = {}

    while True:

        # ── STEP 1: Nodes ────────────────────────────────────────
        if step == 1:
            print("\n[STEP 1] Enter all node names (comma-separated).")
            print("         Example: A, B, C, D, E")
            raw = prompt("  Nodes: ")

            if raw == QUIT:
                return None, None, None, None
            if raw == BACK:
                print("  ℹ Already at the first step.")
                continue

            nodes = [n.strip() for n in raw.split(",") if n.strip()]
            if len(nodes) < 2:
                print("  ✘ Need at least 2 nodes — try again.")
                continue

            # Reset graph in case we came back here
            graph = {node: [] for node in nodes}
            heuristics = {}
            step = 2

        # ── STEP 2: Edges ─────────────────────────────────────────
        elif step == 2:
            print("\n[STEP 2] Enter edges as: FROM TO COST  (one per line)")
            print("         Edges are bidirectional (both directions added).")
            print("         Example:  A B 4")
            print("         Type 'done' when finished. Type 'back' to redo nodes.\n")

            # Reset edges in case we came back here
            graph = {node: [] for node in nodes}
            went_back = False

            while True:
                edge_input = prompt("  Edge: ")

                if edge_input == QUIT:
                    return None, None, None, None
                if edge_input == BACK:
                    went_back = True
                    break
                if edge_input.lower() == 'done':
                    break

                parts = edge_input.split()
                if len(parts) != 3:
                    print("  ✘ Format: FROM TO COST — try again.")
                    continue
                frm, to, cost_str = parts
                if frm not in graph or to not in graph:
                    print(f"  ✘ '{frm}' or '{to}' not in node list — skipping.")
                    continue
                try:
                    cost = int(cost_str)
                except ValueError:
                    print("  ✘ Cost must be a number — try again.")
                    continue

                graph[frm].append((to, cost))
                graph[to].append((frm, cost))
                print(f"  ✔ Added edge: {frm} <-> {to}  (cost: {cost})")

            if went_back:
                step = 1
            else:
                step = 3

        # ── STEP 3: Heuristics ────────────────────────────────────
        elif step == 3:
            print("\n[STEP 3] Enter heuristic h(n) for each node.")
            print("         h(n) = estimated cost from that node to the GOAL.")
            print("         Goal node should always have h = 0.")
            print("         Type 'back' to redo edges.\n")

            heuristics = {}
            went_back  = False

            for node in nodes:
                while True:
                    val = prompt(f"  h({node}): ")
                    if val == QUIT:
                        return None, None, None, None
                    if val == BACK:
                        went_back = True
                        break
                    try:
                        heuristics[node] = int(val)
                        break
                    except ValueError:
                        print("  ✘ Must be a number — try again.")
                if went_back:
                    break

            if went_back:
                step = 2
            else:
                step = 4

        # ── STEP 4: Start & Goal ──────────────────────────────────
        elif step == 4:
            print(f"\n[STEP 4] Available nodes: {', '.join(nodes)}")
            print("         Note: node names are case-sensitive (e.g. 'A' not 'a')")
            print("         Type 'back' to redo heuristics.\n")

            # Start node
            start_val = prompt("  Enter START node: ")
            if start_val == QUIT:
                return None, None, None, None
            if start_val == BACK:
                step = 3
                continue
            if start_val not in graph:
                print(f"  ✘ '{start_val}' not found. Available: {', '.join(nodes)}")
                continue

            # Goal node
            goal_val = prompt("  Enter GOAL node : ")
            if goal_val == QUIT:
                return None, None, None, None
            if goal_val == BACK:
                # stay in step 4 so user re-enters start too
                print("  ↩ Re-enter START node.")
                continue
            if goal_val not in graph:
                print(f"  ✘ '{goal_val}' not found. Available: {', '.join(nodes)}")
                continue
            if start_val == goal_val:
                print("  ✘ Start and Goal cannot be the same node.")
                continue

            return graph, heuristics, start_val, goal_val


# ============================================================
#  MAIN — Run as many examples as you want
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*65)
    print("  Welcome to A* Search Algorithm")
    print("  You can run as many examples as you like.")
    print("="*65)

    while True:
        graph, heuristics, start, goal = build_graph()

        if graph is not None:
            a_star(graph, heuristics, start, goal)

        again = input("  Run another example? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("\n  Goodbye!\n")
            break