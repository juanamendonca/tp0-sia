import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")

    # Cargar config desde JSON pasado como argumento
    with open(sys.argv[1], "r") as f:
        config = json.load(f)
        pokemon_name = config["pokemon"]
        pokeball = config["pokeball"]
        level = config.get("level", 50)

    status = StatusEffect.NONE
    hp_percentages = np.linspace(0.1, 1.0, 10)  # de 10% a 100%

    probs = []
    for hp_pct in hp_percentages:
        pokemon = factory.create(pokemon_name, level, status, hp_pct)
        probs.append(attempt_catch(pokemon, pokeball)[1]*100)

    # Gráfico
    plt.figure(figsize=(8, 6))
    plt.plot(hp_percentages * 100, probs, marker="o", label=pokemon_name)
    plt.xlabel("HP restante (%)")
    plt.ylabel("Probabilidad de captura (%)")
    plt.title(f"Efecto del HP en captura de {pokemon_name}\n(Pokeball: {pokeball}, Nivel {level}, Estado: {status.name})")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    plt.savefig("hp_vs_captura.png")
    print("Gráfico guardado en 'hp_vs_captura.png'")
