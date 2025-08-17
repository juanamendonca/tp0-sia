import numpy as np
import matplotlib.pyplot as plt
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

pokemons = ["caterpie","snorlax","jolteon"]
ball = "pokeball"
level = 100
noise = 0.0 
n_tries = 1000

factory = PokemonFactory("pokemon.json")
effects = [
    StatusEffect.NONE, StatusEffect.POISON, StatusEffect.BURN, StatusEffect.PARALYSIS, StatusEffect.SLEEP, StatusEffect.FREEZE
]

results = {}

for name in pokemons:
    results[name] = {}
    for eff in effects:
        vals = []
        pkm = factory.create(name, level, eff, 1.0) 
        for _ in range(n_tries):
            ok, _ = attempt_catch(pkm, ball, noise)
            vals.append(ok)
        results[name][eff.name] = vals

for name, data in results.items():
    rates = {eff: np.mean(bools) * 100 for eff, bools in data.items()}

    plt.figure(figsize=(6, 4))
    xs = list(rates.keys())
    ys = list(rates.values())
    bars = plt.bar(xs, ys, color="skyblue")

    plt.xlabel("Estado de Salud")
    plt.ylabel("Probabilidad de Captura (%)")
    plt.title(f"Efecto del Estado de Salud en la Probabilidad de Captura de {name.capitalize()}")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.ylim(0, 110)

    for x, y in zip(xs, ys):
        plt.text(x, y, f"{y:.2f}%", ha="center", va="bottom")

    plt.tight_layout()
    plt.show()
