import json
import numpy as np
import matplotlib.pyplot as plt
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

def run_for_pokemon(config_path, reps=100):
    # Crear la factory
    factory = PokemonFactory("pokemon.json")

    # Cargar configuración específica
    with open(config_path, "r") as f:
        config = json.load(f)

    pokemon_name = config["pokemon"]
    pokeballs = config["pokeballs"]
    level = config.get("level", 100)
    noise = config.get("noise", 0)

    # HP y efectos a evaluar
    hp_percentages = [0.01, 0.25, 0.5, 0.75, 1.0]
    effects = list(StatusEffect)

    results = []

    # Probar todas las combinaciones
    for effect in effects:
        for hp_pct in hp_percentages:
            pokemon = factory.create(pokemon_name, level, effect, hp_pct)
            for ball in pokeballs:
                probs = []
                for _ in range(reps):
                    success, _ = attempt_catch(pokemon, ball, noise)
                    probs.append(success)
                mean_prob = np.mean(probs) * 100
                results.append((effect.name, int(hp_pct*100), ball, mean_prob))

    # Ordenar y tomar top 10
    top10 = sorted(results, key=lambda x: x[3], reverse=True)[:10]

    # Graficar
    labels = [f"{e}, HP {hp}%, {b}" for e, hp, b, _ in top10]
    probs = [p for _, _, _, p in top10]

    plt.figure(figsize=(8, 6))
    plt.barh(labels, probs, color="skyblue", edgecolor="black")
    plt.xlabel("Probabilidad de Captura (%)")
    plt.ylabel("Combinaciones")
    plt.title(f"Mejores combinaciones para capturar a {pokemon_name.capitalize()}")
    plt.xlim(0, 100)
    plt.grid(axis="x", linestyle="--", alpha=0.6)

    for i, val in enumerate(probs):
        plt.text(val + 1, i, f"{val:.1f}%", va="center")

    plt.tight_layout()
    filename = f"graphs/ej2d_{pokemon_name}.png"
    plt.savefig(filename)
    print(f"Gráfico guardado en 'ej2d_{pokemon_name}.png'")

if __name__ == "__main__":
    run_for_pokemon("configs/jolteon.json", reps=100)
    run_for_pokemon("configs/mewtwo.json", reps=100)
