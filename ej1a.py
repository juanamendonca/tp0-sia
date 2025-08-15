import json
import sys
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

    for pokemon_name in pokemons:
        for ball_name in pokeballs:
            pokemon = factory.create(pokemon_name, 100, StatusEffect.NONE, 1.0)
            
            # Tomamos solo el primer elemento (éxito) de la tupla
            successes = sum(attempt_catch(pokemon, ball_name)[0] for _ in range(100))
            probability = successes / 100 * 100

            print(f"{pokemon_name:<12} | {ball_name:<12} | {probability:<15.2f}")
