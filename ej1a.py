import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")

    with open(sys.argv[1], "r") as f:
        config = json.load(f)
        pokemons = config["pokemon"]
        pokeballs = config["pokeballs"]

    print(f"{'Pokemon':<12} | {'Pokeball':<12} | {'Probabilidad (%)':<15}")
    print("-" * 45)

    probabilities = []

    for pokemon_name in pokemons:
        row_probs = []
        for ball_name in pokeballs:
            pokemon = factory.create(pokemon_name, 100, StatusEffect.NONE, 1)

            results = [attempt_catch(pokemon, ball_name)[0] for _ in range(100)]
            prob = np.mean(results) * 100

            print(f"{pokemon_name:<12} | {ball_name:<12} | {prob:<15.2f}")

            row_probs.append(prob)

        probabilities.append(row_probs)

    probabilities = np.array(probabilities)

    # ---------- Gráfico 1: barras agrupadas por Pokéball ----------
    x = np.arange(len(pokeballs))
    width = 0.15

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, pokemon_name in enumerate(pokemons):
        bars = ax.bar(x + i*width, probabilities[i], width, label=pokemon_name)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 1, f"{height:.0f}%", ha='center', va='bottom', fontsize=9)

    ax.set_xticks(x + width * (len(pokemons)-1)/2)
    ax.set_xticklabels(pokeballs)
    ax.set_ylabel("Probabilidad de captura (%)")
    ax.set_title("Probabilidad de captura de Pokémon por Pokéball")
    ax.legend()
    plt.tight_layout()
    plt.savefig("graphs/ej1a_pokeballs.png")
    print("Gráfico guardado en 'ej1a_pokeballs.png'")

    # ---------- Gráfico 2: barras agrupadas por Pokémon ----------
    x2 = np.arange(len(pokemons))
    width2 = 0.15

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    for j, ball_name in enumerate(pokeballs):
        bars = ax2.bar(x2 + j*width2, probabilities[:, j], width2, label=ball_name)
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, height + 1, f"{height:.0f}%", ha='center', va='bottom', fontsize=9)

    ax2.set_xticks(x2 + width2 * (len(pokeballs)-1)/2)
    ax2.set_xticklabels(pokemons)
    ax2.set_ylabel("Probabilidad de captura (%)")
    ax2.set_title("Probabilidad de captura por Pokémon")
    ax2.legend()
    plt.tight_layout()
    plt.savefig("graphs/ej1a_pokemons.png")
    print("Gráfico guardado en 'ej1a_pokemons.png'")
