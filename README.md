# Genetic-Algo-grp-11

Genetic algorithm implementation based for optimizing based on Traveling Salesman Problem

## Project File

- `genetic_algorithm.py` — main Python file

## Requirements

- Python 3.x
- NumPy

## Install Dependencies

Open a terminal in the project folder and run:

pip install numpy

## How to Run

1. Download or clone the project folder.
2. Open a terminal in the folder containing `genetic_algorithm.py`.
3. Run the program with:

python genetic_algorithm.py

## Expected Output

The program will print s and their total distances and various randomly generated routes.

Example output format:

Route: ['B', 'A', 'D', 'C'], Total Distance: 82
Route: ['C', 'A', 'B', 'D'], Total Distance: 70

Because the initial population is random, your output may be different each time you run the file.

## Notes

- This version currently demonstrates:
  - population initialization
  - route encoding using permutations
  - fitness calculation
  - tournament selection logic
  - 
- This version does **not yet** include:
  - crossover
  - mutation
  - next-generation replacement
  - multi-generation comparison

## Troubleshooting

- If `numpy` is not installed, run:

pip install numpy

- If Python is not recognized, try:

python3 genetic_algorithm.py

## Future Improvements

The next version will add:
- crossover
- mutation
- elitism or replacement strategy
- evolution across generations
- comparison of best fitness across generations
