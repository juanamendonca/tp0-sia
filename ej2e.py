import json
import numpy as np
import matplotlib.pyplot as plt
from src.pokemon import PokemonFactory, StatusEffect
from src.catching import attempt_catch

# --- Cargar configuraciones ---
with open("configs/jolteon.json") as f:
    cat_cfg = json.load(f)
with open("configs/mewtwo.json") as f:
    mew_cfg = json.load(f)

factory = PokemonFactory("pokemon.json")

# --- Definir rangos de simulación ---
effects = list(StatusEffect)
healths = [0.01, 0.25, 0.5, 0.75, 1.0]
levels = [50, 75, 100]  # puedes ajustarlo según lo que pida el enunciado
pokeballs = list(set(cat_cfg["pokeballs"]) & set(mew_cfg["pokeballs"]))  # bolas comunes

results = {}
for pokemon_name in ["jolteon", "mewtwo"]:
    results[pokemon_name] = []
    for effect in effects:
        for health in healths:
            for level in levels:
                for ball in pokeballs:
                    pokemon = factory.create(pokemon_name, int(level), effect, float(health))
                    probs = []
                    for _ in range(100):
                        success, _ = attempt_catch(pokemon, ball)
                        probs.append(success)
                    avg_prob = np.mean(probs) * 100
                    results[pokemon_name].append(
                        (effect.name, health, level, ball, avg_prob)
                    )

# --- Graficar resultados individuales ---
for pokemon, result_data in results.items():
    # Tomar top 10 combinaciones por probabilidad
    data = sorted(result_data, key=lambda x: x[4])[-10:]
    labels = [f"{x[0]}, HP {int(x[1]*100)}%, LVL {x[2]}, {x[3]}" for x in data]
    probs = [x[4] for x in data]

    plt.figure(figsize=(6, 5))
    plt.barh(labels, probs, edgecolor="black", color="skyblue")
    plt.xlabel("Probabilidad de Captura (%)")
    plt.ylabel("Combinaciones")
    plt.title(f"Mejores combinaciones para capturar a {pokemon.capitalize()}")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.xlim(0, 110)

    # Etiquetas sobre las barras
    for i, rate in enumerate(data):
        plt.text(rate[4] + 1, i, f"{rate[4]:.0f}%", va="center")

    plt.tight_layout()
    plt.savefig(f"graphs/ej2e_{pokemon}.png")
    print(f"Gráfico guardado en 'ej2e_{pokemon}.png'")
