import json
import sys
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    factory = PokemonFactory("pokemon.json")


    with open(sys.argv[1], "r") as f:
        config = json.load(f)
        pokemons = config["pokemon"]
        pokeballs = config["pokeballs"]

    with open("pokemon.json") as f:
        pokemon_data = json.load(f)

    num_attempts = 10000
    results = {}
    for pokemon_name in pokemons:
        pokemon = factory.create(pokemon_name, 100, StatusEffect.NONE, 1.0)

        relative = {}
        for ball_name in pokeballs:
            attempts = [attempt_catch(pokemon, ball_name)[0] for _ in range(num_attempts)]
            prob = np.mean(attempts)
            relative[ball_name] = prob

        relative = {k: (v / relative["pokeball"]) * 100 for k, v in relative.items()}
        results[pokemon_name] = relative

    plt.figure(figsize=(10,6))
    for pokemon_name, relative in results.items():
        balls = list(relative.keys())
        rels = list(relative.values())
        plt.plot(balls, rels, marker='o', linestyle='-', label=pokemon_name)

    plt.ylim(0, None)
    plt.ylabel("Éxito relativo (%)")
    plt.xlabel("Tipo de Pokebola")
    plt.title("Efectividad relativa por Pokebola")
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("graphs/ej1b.png")
    print("Gráfico guardado en 'ej1b.png'")