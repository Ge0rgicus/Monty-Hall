import random
import matplotlib.pyplot as plt

GAMES_PER_AGENT = 500
MUTATION_RATE = 0.02
DOORS = 10

def create_population(size=100):
    return [{"gene": random.random(), "wins": 0} for _ in range(size)]

def play_monty_hall(agent, games=GAMES_PER_AGENT, doors=DOORS):
    wins = 0
    for _ in range(games):
        car = random.randint(0, doors - 1)
        pick = random.randint(0, doors - 1)

        # Host must leave the car closed (if it's not the pick),
        # and randomly picks one goat to leave closed otherwise
        if car != pick:
            switch_door = car  # host is forced to leave the car
        else:
            # pick == car: host can leave any goat door closed
            goats = [d for d in range(doors) if d != pick]
            switch_door = random.choice(goats)

        if random.random() < agent["gene"]:
            new_pick = switch_door
        else:
            new_pick = pick

        if new_pick == car:
            wins += 1

    agent["wins"] = wins
def reproduce(population, target_size=100):
    total_wins = sum(a["wins"] for a in population)

    if total_wins == 0:
        return create_population(target_size)

    new_population = []
    for _ in range(target_size):
        pick = random.uniform(0, total_wins)
        cumulative = 0
        # FIX 1: Default parent to last agent so we never reference an unbound variable
        # if floating-point rounding causes `pick` to exceed the cumulative total.
        parent = population[-1]
        for agent in population:
            cumulative += agent["wins"]
            if cumulative >= pick:
                parent = agent
                break

        new_gene = parent["gene"] + random.uniform(-MUTATION_RATE, MUTATION_RATE)
        new_gene = max(0.0, min(1.0, new_gene))
        new_population.append({"gene": new_gene, "wins": 0})

    return new_population

def run_simulation(generations=100, population_size=100):
    population = create_population(population_size)
    history = {"avg_gene": [], "win_rate": []}

    # FIX 2: Compute both reference values from the same constant — no walrus operator.
    optimal = (DOORS - 1) / DOORS
    stay    = 1 / DOORS

    for gen in range(generations):
        for agent in population:
            play_monty_hall(agent)

        avg_gene = sum(a["gene"] for a in population) / population_size
        avg_wins = sum(a["wins"] for a in population) / population_size
        win_rate = avg_wins / GAMES_PER_AGENT

        history["avg_gene"].append(avg_gene)
        history["win_rate"].append(win_rate)

        print(f"Gen {gen+1:3d} | Avg gene: {avg_gene:.3f} | Win rate: {win_rate:.2%}")

        population = reproduce(population, population_size)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    gens = range(1, generations + 1)

    axes[0].plot(gens, history["avg_gene"], color="#8B5CF6")
    axes[0].axhline(1.0, color="#378ADD", linestyle="--", linewidth=0.8, label="Always switch (optimal)")
    axes[0].axhline(0.5, color="gray",    linestyle="--", linewidth=0.8, label="Random")
    axes[0].set_ylabel("Avg gene (switch probability)")
    axes[0].set_ylim(0, 1)
    axes[0].legend()

    axes[1].plot(gens, history["win_rate"], color="#1D9E75")
    axes[1].axhline(optimal, color="#378ADD", linestyle="--", linewidth=0.8, label=f"Optimal ({optimal:.0%})")
    axes[1].axhline(stay,    color="#E24B4A", linestyle="--", linewidth=0.8, label=f"Always stay ({stay:.0%})")
    axes[1].set_ylabel("Win rate")
    axes[1].set_ylim(0, 1)
    axes[1].set_xlabel("Generation")
    axes[1].legend()

    plt.suptitle(f"Monty Hall ({DOORS} doors) — Genetic Algorithm", fontsize=13)
    plt.tight_layout()
    plt.savefig("monty_hall_ga.png", dpi=150)
    plt.show()

run_simulation(100)