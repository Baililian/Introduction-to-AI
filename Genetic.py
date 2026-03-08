import random

# ============================================================
#  GENETIC ALGORITHM - Core Implementation
# ============================================================

def genetic_algorithm(target, population_size, mutation_rate, generations):
    """
    Genetic Algorithm — evolves a population of strings
    toward a target string.

    Parameters:
        target          : the string we want to evolve toward
        population_size : how many candidates per generation
        mutation_rate   : chance (0.0-1.0) of a character mutating
        generations     : how many generations to run

    Each individual is a string of the same length as target.
    Fitness = number of characters that match the target.
    """

    CHARS = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?.,'-"

    # ── Helpers ───────────────────────────────────────────────

    def random_individual():
        return ''.join(random.choice(CHARS) for _ in range(len(target)))

    def fitness(individual):
        return sum(1 for a, b in zip(individual, target) if a == b)

    def crossover(parent1, parent2):
        point = random.randint(1, len(target) - 1)
        return parent1[:point] + parent2[point:]

    def mutate(individual):
        result = list(individual)
        for i in range(len(result)):
            if random.random() < mutation_rate:
                result[i] = random.choice(CHARS)
        return ''.join(result)

    # ── Initial Population ────────────────────────────────────
    population = [random_individual() for _ in range(population_size)]

    print(f"\n{'='*65}")
    print(f"  GENETIC ALGORITHM")
    print(f"  Target          : '{target}'")
    print(f"  Population size : {population_size}")
    print(f"  Mutation rate   : {mutation_rate}")
    print(f"  Max generations : {generations}")
    print(f"{'='*65}")
    print(f"\n  {'Gen':<8} {'Best Individual':<35} {'Fitness':<10} {'Match'}")
    print(f"  {'-'*60}")

    best_overall = None
    best_fitness = -1

    for gen in range(1, generations + 1):

        # Evaluate fitness
        scored = [(ind, fitness(ind)) for ind in population]
        scored.sort(key=lambda x: -x[1])

        best_ind, best_fit = scored[0]

        # Track overall best
        if best_fit > best_fitness:
            best_fitness = best_fit
            best_overall = best_ind

        match_pct = (best_fit / len(target)) * 100

        # Print every 10 generations + first + last + when improved
        if gen == 1 or gen % 10 == 0 or best_fit == len(target) or best_fit > best_fitness:
            print(f"  {gen:<8} {best_ind:<35} {best_fit:<10} {match_pct:.1f}%")

        # Stop if perfect solution found
        if best_fit == len(target):
            print(f"\n  ✔ Perfect solution found at generation {gen}!")
            break

        # Selection — keep top 50%
        survivors = [ind for ind, _ in scored[:population_size // 2]]

        # Create next generation via crossover + mutation
        next_population = survivors[:]
        while len(next_population) < population_size:
            p1, p2 = random.sample(survivors, 2)
            child = mutate(crossover(p1, p2))
            next_population.append(child)

        population = next_population

    print(f"\n  {'='*65}")
    print(f"  RESULT")
    print(f"  Target   : '{target}'")
    print(f"  Best     : '{best_overall}'")
    print(f"  Fitness  : {best_fitness}/{len(target)} characters matched")
    print(f"  {'='*65}\n")

    return best_overall, best_fitness


# ============================================================
#  BUILD PARAMETERS FROM USER INPUT
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


def build_params():
    print("\n" + "#"*65)
    print("  GENETIC ALGORITHM - Dynamic Parameter Builder")
    print("  Type 'back' to go to the previous step.")
    print("  Type 'quit' to exit.")
    print("#"*65)

    target          = ""
    population_size = 100
    mutation_rate   = 0.01
    generations     = 500
    step = 1

    while True:

        # ── STEP 1: Target String ─────────────────────────────
        if step == 1:
            print("\n[STEP 1] Enter the TARGET string to evolve toward.")
            print("         The algorithm will try to guess this string")
            print("         by evolving a population over generations.")
            print("         Example: hello world\n")

            val = prompt("  Target: ")
            if val == QUIT:
                return None, None, None, None
            if val == BACK:
                print("  ℹ Already at the first step.")
                continue
            if not val:
                print("  ✘ Target cannot be empty.")
                continue

            target = val
            step = 2

        # ── STEP 2: Population Size ───────────────────────────
        elif step == 2:
            print(f"\n[STEP 2] Set POPULATION SIZE.")
            print(f"         = how many candidate solutions exist per generation.")
            print(f"         Recommended: 100 to 500.")
            print(f"         Type 'back' to redo target.\n")

            val = prompt("  Population size (e.g. 100): ")
            if val == QUIT:
                return None, None, None, None
            if val == BACK:
                step = 1
                continue
            try:
                population_size = int(val)
                if population_size < 10:
                    print("  ✘ Must be at least 10.")
                    continue
            except ValueError:
                print("  ✘ Must be a whole number — try again.")
                continue

            step = 3

        # ── STEP 3: Mutation Rate ─────────────────────────────
        elif step == 3:
            print(f"\n[STEP 3] Set MUTATION RATE (0.0 to 1.0).")
            print(f"         = chance that a character randomly changes.")
            print(f"         Too low = slow evolution.")
            print(f"         Too high = too random, won't converge.")
            print(f"         Recommended: 0.01 to 0.05")
            print(f"         Type 'back' to redo population size.\n")

            val = prompt("  Mutation rate (e.g. 0.01): ")
            if val == QUIT:
                return None, None, None, None
            if val == BACK:
                step = 2
                continue
            try:
                mutation_rate = float(val)
                if not (0.0 <= mutation_rate <= 1.0):
                    print("  ✘ Must be between 0.0 and 1.0.")
                    continue
            except ValueError:
                print("  ✘ Must be a decimal number — try again.")
                continue

            step = 4

        # ── STEP 4: Generations ───────────────────────────────
        elif step == 4:
            print(f"\n[STEP 4] Set max number of GENERATIONS.")
            print(f"         = how many times the population evolves.")
            print(f"         Algorithm stops early if target is found.")
            print(f"         Recommended: 500 to 5000")
            print(f"         Type 'back' to redo mutation rate.\n")

            val = prompt("  Generations (e.g. 1000): ")
            if val == QUIT:
                return None, None, None, None
            if val == BACK:
                step = 3
                continue
            try:
                generations = int(val)
                if generations < 1:
                    print("  ✘ Must be at least 1.")
                    continue
            except ValueError:
                print("  ✘ Must be a whole number — try again.")
                continue

            return target, population_size, mutation_rate, generations


# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*65)
    print("  Welcome to the Genetic Algorithm")
    print("  Evolves a population of random strings toward a target")
    print("  using selection, crossover, and mutation.")
    print("="*65)

    while True:
        target, population_size, mutation_rate, generations = build_params()

        if target is None:
            print("\n  Goodbye!\n")
            break

        genetic_algorithm(target, population_size, mutation_rate, generations)

        again = input("  Run another example? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("\n  Goodbye!\n")
            break