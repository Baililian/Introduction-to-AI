from itertools import combinations

# ============================================================
#  A-PRIORI ALGORITHM - Core Implementation
# ============================================================

def get_frequent_itemsets(transactions, min_support):
    """
    A-Priori Algorithm
    
    Parameters:
        transactions  : list of sets, each set is one transaction
        min_support   : minimum number of transactions an itemset must appear in
    
    Returns:
        all_frequent  : dict of {frozenset: support_count}
    """

    all_frequent = {}
    
    # ── PASS 1: Find frequent single items ───────────────────
    print(f"\n{'='*60}")
    print(f"  PASS 1 — Counting individual items")
    print(f"{'='*60}")

    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1

    frequent_items = {frozenset([item]): count
                      for item, count in item_counts.items()
                      if count >= min_support}

    print(f"\n  {'Item':<20} {'Support':<10} {'Frequent?'}")
    print(f"  {'-'*40}")
    for item, count in sorted(item_counts.items()):
        status = "✔ YES" if count >= min_support else "✘ NO"
        print(f"  {item:<20} {count:<10} {status}")

    all_frequent.update(frequent_items)

    # ── PASS 2+: Find frequent k-itemsets ────────────────────
    current_frequent = frequent_items
    k = 2

    while current_frequent:
        print(f"\n{'='*60}")
        print(f"  PASS {k} — Counting {k}-item combinations")
        print(f"{'='*60}")

        # Generate candidates from previous frequent itemsets
        prev_items = list(current_frequent.keys())
        candidates = {}

        for i in range(len(prev_items)):
            for j in range(i + 1, len(prev_items)):
                union = prev_items[i] | prev_items[j]
                if len(union) == k:
                    candidates[union] = 0

        if not candidates:
            break

        # Count candidates in transactions
        for transaction in transactions:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    candidates[candidate] += 1

        # Filter by min support
        new_frequent = {itemset: count
                        for itemset, count in candidates.items()
                        if count >= min_support}

        print(f"\n  {'Itemset':<25} {'Support':<10} {'Frequent?'}")
        print(f"  {'-'*45}")
        for itemset, count in sorted(candidates.items(), key=lambda x: sorted(x[0])):
            label = "{" + ", ".join(sorted(itemset)) + "}"
            status = "✔ YES" if count >= min_support else "✘ NO"
            print(f"  {label:<25} {count:<10} {status}")

        all_frequent.update(new_frequent)
        current_frequent = new_frequent
        k += 1

    return all_frequent


def generate_rules(all_frequent, transactions, min_confidence):
    """Generate association rules from frequent itemsets."""

    total = len(transactions)
    rules = []

    for itemset in all_frequent:
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent in map(frozenset, combinations(sorted(itemset), size)):
                consequent = itemset - antecedent
                support_both = all_frequent[itemset]
                support_ant  = all_frequent.get(antecedent, 0)

                if support_ant == 0:
                    continue

                confidence = support_both / support_ant
                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, support_both, confidence))

    return rules


# ============================================================
#  BUILD TRANSACTIONS FROM USER INPUT
# ============================================================

BACK = 'back'
QUIT = 'quit'

def prompt(msg):
    val = input(msg).strip()
    if val.lower() == 'back':
        return BACK
    if val.lower() == 'quit':
        return QUIT
    return val


def build_transactions():
    print("\n" + "#"*60)
    print("  A-PRIORI ALGORITHM - Dynamic Transaction Builder")
    print("  Type 'back' to go to the previous step.")
    print("  Type 'quit' to exit.")
    print("#"*60)

    transactions = []
    min_support    = 2
    min_confidence = 0.5
    step = 1

    while True:

        # ── STEP 1: Transactions ──────────────────────────────
        if step == 1:
            print("\n[STEP 1] Enter your transactions.")
            print("         Each transaction = one line of comma-separated items.")
            print("         Example:  bread, milk, eggs")
            print("         Type 'done' when finished.\n")

            transactions = []
            went_back = False

            while True:
                val = prompt(f"  Transaction {len(transactions)+1}: ")
                if val == QUIT:
                    return None, None, None
                if val == BACK:
                    print("  ℹ Already at the first step.")
                    continue
                if val.lower() == 'done':
                    if len(transactions) < 2:
                        print("  ✘ Enter at least 2 transactions.")
                        continue
                    break

                items = set(i.strip().lower() for i in val.split(",") if i.strip())
                if not items:
                    print("  ✘ Empty transaction — try again.")
                    continue

                transactions.append(items)
                print(f"  ✔ Added: {{ {', '.join(sorted(items))} }}")

            step = 2

        # ── STEP 2: Min Support ───────────────────────────────
        elif step == 2:
            print(f"\n[STEP 2] Set minimum support.")
            print(f"         = how many transactions an item must appear in.")
            print(f"         Total transactions entered: {len(transactions)}")
            print(f"         Type 'back' to redo transactions.\n")

            val = prompt("  Minimum support (e.g. 2): ")
            if val == QUIT:
                return None, None, None
            if val == BACK:
                step = 1
                continue
            try:
                min_support = int(val)
                if min_support < 1:
                    print("  ✘ Must be at least 1.")
                    continue
                if min_support > len(transactions):
                    print(f"  ✘ Can't exceed total transactions ({len(transactions)}).")
                    continue
            except ValueError:
                print("  ✘ Must be a number — try again.")
                continue

            step = 3

        # ── STEP 3: Min Confidence ────────────────────────────
        elif step == 3:
            print(f"\n[STEP 3] Set minimum confidence (0.0 to 1.0).")
            print(f"         = how reliable an association rule must be.")
            print(f"         Example: 0.7 means the rule must be true 70% of the time.")
            print(f"         Type 'back' to redo minimum support.\n")

            val = prompt("  Minimum confidence (e.g. 0.7): ")
            if val == QUIT:
                return None, None, None
            if val == BACK:
                step = 2
                continue
            try:
                min_confidence = float(val)
                if not (0.0 <= min_confidence <= 1.0):
                    print("  ✘ Must be between 0.0 and 1.0.")
                    continue
            except ValueError:
                print("  ✘ Must be a decimal number — try again.")
                continue

            return transactions, min_support, min_confidence


# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Welcome to A-Priori Algorithm")
    print("  Finds frequent itemsets and association rules")
    print("  from your transaction data.")
    print("="*60)

    while True:
        transactions, min_support, min_confidence = build_transactions()

        if transactions is None:
            print("\n  Goodbye!\n")
            break

        # ── Run A-Priori ──────────────────────────────────────
        print(f"\n{'='*60}")
        print(f"  Running A-Priori")
        print(f"  Transactions   : {len(transactions)}")
        print(f"  Min Support    : {min_support}")
        print(f"  Min Confidence : {min_confidence}")
        print(f"{'='*60}")

        print("\n  Transactions entered:")
        for i, t in enumerate(transactions, 1):
            print(f"  T{i}: {{ {', '.join(sorted(t))} }}")

        all_frequent = get_frequent_itemsets(transactions, min_support)

        # ── Summary of frequent itemsets ──────────────────────
        print(f"\n{'='*60}")
        print(f"  FREQUENT ITEMSETS SUMMARY")
        print(f"{'='*60}")
        if all_frequent:
            for itemset, count in sorted(all_frequent.items(), key=lambda x: (len(x[0]), sorted(x[0]))):
                label = "{" + ", ".join(sorted(itemset)) + "}"
                print(f"  {label:<25} support = {count}")
        else:
            print("  No frequent itemsets found with given min support.")

        # ── Association Rules ─────────────────────────────────
        print(f"\n{'='*60}")
        print(f"  ASSOCIATION RULES  (confidence >= {min_confidence})")
        print(f"{'='*60}")
        rules = generate_rules(all_frequent, transactions, min_confidence)

        if rules:
            print(f"\n  {'Rule':<35} {'Support':<10} {'Confidence'}")
            print(f"  {'-'*55}")
            for ant, con, sup, conf in sorted(rules, key=lambda x: -x[3]):
                rule_str = "{" + ", ".join(sorted(ant)) + "} => {" + ", ".join(sorted(con)) + "}"
                print(f"  {rule_str:<35} {sup:<10} {conf:.0%}")
        else:
            print("  No association rules found with given confidence.")

        print()
        again = input("  Run another example? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("\n  Goodbye!\n")
            break