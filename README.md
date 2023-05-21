# Wordle
Implementation of [New York Times' word game](https://www.nytimes.com/games/wordle/index.html), originally created by Josh Wardle, along with a few solving algorithms.

## Results
Algorithms used for solving:  
* random -- choose randomly any feasible word  
* best_letter -- choose feasible word with the most untried letters

Note: feasible word is a word that exists in a word bank and could be the solution based on known letter status.  
After evaluating these algorithms on words_wordle (original wordle word bank) and words_tabatkins ([tabatkins' word bank](https://github.com/tabatkins/wordle-list)), following results were achieved:  
| Algorithm | Word Bank | Wins | Games | Win rate | Avg. Score* |
|:---|:---|:---:|:---:|:---:|:---:|
| random | words_wordle | 2265 | 2309 | 98.09% | 3.78 |
| random | words_tabatkins | 12453 | 14855 | 83.83% | 3.84 |
| best_letter | words_wordle | 2283 | 2309 | 98.87% | 3.79 |
| best_letter | words_tabatkins | 12571 | 14855 | 84.62% | 3.86 |  

\* -- Average guess count of won games  
  
## How to run
```bash
python game.py
```  

To play against a set solution (it has to be from the word bank):
```bash
python game.py -s <solution>
```  

To solve using one of the algorithms:
```bash
python game.py -p <algorithm>
```  

To specify a word bank:
```bash
python game.py -w <filename>
```

