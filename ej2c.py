import json
import sys
from enum import Enum
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect
import matplotlib.pyplot as plt
import numpy as np

def run_simulation(factory, pokemon_name, num_attempts, hp_frac=1.0, level=100, status=StatusEffect.NONE):
    pokemon = factory.create(pokemon_name, level, status, hp_frac)
    attempts = [attempt_catch(pokemon, "pokeball")[0] for _ in range(num_attempts)]
    mean_prob = np.mean(attempts) * 100
    std_err = np.std(attempts) / np.sqrt(num_attempts) * 100
    return mean_prob, std_err

def plot_bar_chart(x_labels, data_dict, errors_dict, xlabel, title):
    x = np.arange(len(x_labels))
    width = 0.25
    plt.figure(figsize=(10,6))
    for i, name in enumerate(data_dict.keys()):
        plt.bar(x + i*width, data_dict[name], width=width, yerr=errors_dict[name], capsize=4, label=name)
    plt.xticks(x + width, x_labels)
    plt.ylabel("Probabilidad de Captura (%)")
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()


if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")
    num_attempts = 5000

    pokemons = ["jolteon", "snorlax", "onix"]

    # 1) Vary HP
    hp_percentages = [0.01, 0.25, 0.5, 0.75, 1.0]
    hp_results = {}
    hp_errors = {}
    for pokemon_name in pokemons:
        probs, errs = zip(*[run_simulation(factory, pokemon_name, num_attempts, hp_frac=hp, level=100, status=StatusEffect.NONE) for hp in hp_percentages])
        hp_results[pokemon_name] = probs
        hp_errors[pokemon_name] = errs
    plot_bar_chart([f"{int(h*100)}%" for h in hp_percentages], hp_results, hp_errors, "Fracción de HP", "Efecto de la Fracción de HP en la Probabilidad de Captura")

    # 2) Vary Level
    levels = [1, 25, 50, 75, 100]
    level_results = {}
    level_errors = {}
    for pokemon_name in pokemons:
        probs, errs = zip(*[run_simulation(factory, pokemon_name, num_attempts, hp_frac=1.0, level=lvl, status=StatusEffect.NONE) for lvl in levels])
        level_results[pokemon_name] = probs
        level_errors[pokemon_name] = errs
    plot_bar_chart([str(l) for l in levels], level_results, level_errors, "Nivel", "Efecto del Nivel en la Probabilidad de Captura")

    # 3) Vary Status Effect
    statuses = [StatusEffect.NONE, StatusEffect.POISON, StatusEffect.BURN, StatusEffect.PARALYSIS, StatusEffect.SLEEP, StatusEffect.FREEZE]
    status_results = {}
    status_errors = {}
    for pokemon_name in pokemons:
        probs, errs = zip(*[run_simulation(factory, pokemon_name, num_attempts, hp_frac=1.0, level=100, status=s) for s in statuses])
        status_results[pokemon_name] = probs
        status_errors[pokemon_name] = errs
    plot_bar_chart([s.name for s in statuses], status_results, status_errors, "Efecto de Estado", "Impacto de los Efectos de Estado en la Probabilidad de Captura")