
# TP0 SIA - Análisis de Datos

## Introducción

Trabajo práctico orientativo para la materia Sistemas de Inteligencia Artificial con el
objetivo de evaluar la función de captura de un Pokemon.

[Enunciado](docs/SIA_TP0.pdf)

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Parado en la carpeta del tp0 ejecutar

```sh
pipenv install
```

para instalar las dependencias necesarias en el ambiente virtual

## Ejecución

```
pipenv run python main.py [config_file]
```

### Ejecución ejercicio 1 a 

```
pipenv run python ej1a.py configs/all.json
```

### Ejecución ejercicio 1 b 

```
pipenv run python ej1b.py configs/all.json
```

### Ejecución ejercicio 2 b 

```
pipenv run python ej2b.py configs/caterpie_ej2b.json
pipenv run python ej2b.py configs/mewtwo_ej2b.json
```

### Ejecución del resto de ejercicios

```
pipenv run python ej2<letra>.py
```

Los gráficos se guardan dentro de la carpeta graphs
