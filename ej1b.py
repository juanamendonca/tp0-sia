import json
import sys
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    factory = PokemonFactory("pokemon.json")
    num_attempts = 10000

    with open(sys.argv[1], "r") as f:
        config = json.load(f)
        pokemons = config["pokemon"]
        pokeballs = config["pokeballs"]

    with open("pokemon.json") as f:
        pokemon_data = json.load(f)

    results = {}

    for pokemon_name in pokemons:
        pokemon = factory.create(pokemon_name, 100, StatusEffect.NONE, 1.0)

        # In order to calculate relative success, the base success is required
        # So we first did this basic pokeball run to get that average
        basic_attempts = [attempt_catch(pokemon, "pokeball")[0] for _ in range(num_attempts)]
        basic_prob = np.mean(basic_attempts)

        relative = {}
        for ball_name in pokeballs:
            attempts = [attempt_catch(pokemon, ball_name)[0] for _ in range(num_attempts)]
            prob = np.mean(attempts)
            relative_effectiveness = (prob / basic_prob) * 100 if basic_prob > 0 else 0
            relative[ball_name] = relative_effectiveness

        results[pokemon_name] = relative

    plt.figure(figsize=(10,6))
    for pokemon_name, relative in results.items():
        balls = list(relative.keys())
        rels = list(relative.values())
        plt.plot(balls, rels, marker='o', linestyle='-', label=pokemon_name)

    plt.ylim(0, None)
    plt.ylabel("Éxito relativo ( % )")
    plt.xlabel("Tipo de Pokebola")
    plt.title("Efectividad relativa por Pokébola")
    plt.grid(True)
    plt.legend()
    plt.show()