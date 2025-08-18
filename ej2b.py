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
        pokemon_name = config["pokemon"]
        pokeball = config["pokeball"]
        noise = config.get("noise", 0)

    status = StatusEffect.NONE
    hp_percentages = np.linspace(0.1, 1.0, 10) 

    level = 100
    sim_means = []
    err_low = []
    err_high = []

    n_simulations = 100 

    for hp_pct in hp_percentages:
        pokemon = factory.create(pokemon_name, level, status, hp_pct)
    
        probs = [attempt_catch(pokemon, pokeball, noise)[1] * 100 for _ in range(n_simulations)]

        mean_prob = np.mean(probs)
        p25 = np.percentile(probs, 25)
        p75 = np.percentile(probs, 75)

        sim_means.append(mean_prob)
        err_low.append(max(mean_prob - p25, 0)) 
        err_high.append(max(p75 - mean_prob, 0))  

    # Gráfico
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        hp_percentages * 100,
        sim_means,
        yerr=[err_low, err_high],
        fmt="o-",
        capsize=5,
        label=pokemon_name,
    )
    plt.xlabel("HP restante (%)")
    plt.ylabel("Probabilidad de captura (%)")
    plt.title(
        f"Efecto del HP en captura de {pokemon_name}\n"
        f"(Pokeball: {pokeball}, Nivel {level}, Estado: {status.name}, Ruido: {noise})"
    )
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"graphs/ej2b_{pokemon_name}.png")
    print(f"Gráfico guardado en 'ej2b_{pokemon_name}.png'")
