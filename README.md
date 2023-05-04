# Wordle
Implementation of [NYT word game](https://www.nytimes.com/games/wordle/index.html), originally created by Josh Wardle along with some solving algorithms. Words in 'words' were taken from [tabatkins' repository](https://github.com/tabatkins/wordle-list).  

## How to run
```bash
python game.py
```  

To play against a set solution (it has to be from the word bank):
```bash
python game.py -s <solution>
```  

To solve using one of the algorithms (defined in solver.py):
```bash
python game.py -p <algorithm>
```

