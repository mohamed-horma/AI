# Adversarial Search Problem with Reversi

## Human against human

~~~
./reversi.py
~~~

## Human against random agent

~~~
./reversi.py -1 ReversiRandomAI
./reversi.py -2 ReversiRandomAI
~~~

## Random agent against greedy agent

~~~
./reversi.py -1 ReversiRandomAI -2 ReversiGreedyAI
~~~

## Contest (10 matches) Random agent against greedy agent
~~~
./compete.py -1 ReversiRandomAI -2 ReversiGreedyAI
~~~

## Exercise 1: Minimax with cutoff

~~~
./reversi.py -1 ReversiMinimaxAI -n 3 -2 ReversiGreedyAI 
./reversi.py -1 ReversiGreedyAI -2 ReversiMinimaxAI -n 3

./compete.py -1 ReversiMinimaxAI -n 3 -2 ReversiRandomAI
./compete.py -1 ReversiRandomAI -2 ReversiMinimaxAI -n 3 
~~~

## Exercise 2: Evaluation function

~~~
./reversi.py -1 ReversiMinimaxAI -n 3 -f MyEvaluationFunction -2 ReversiGreedyAI
./reversi.py -1 ReversiGreedyAI -2 ReversiMinimaxAI -f MyEvaluationFunction -n 3

./compete.py -1 ReversiMinimaxAI -n 3 -f MyEvaluationFunction -2 ReversiRandomAI
./compete.py -1 ReversiRandomAI -2 ReversiMinimaxAI -n 3 -f MyEvaluationFunction
~~~

## Exercise 3: Alpha-Beta

~~~
./reversi.py -1 ReversiAlphaBetaAI -n 3 -2 ReversiGreedyAI
./reversi.py -1 ReversiGreedyAI -2 ReversiAlphaBetaAI -n 3
  
./compete.py -1 ReversiAlphaBetaAI -n 3 -2 ReversiRandomAI
./compete.py -1 ReversiRandomAI -2 ReversiAlphaBetaAI -n 3

./compete.py -1 ReversiAlphaBetaAI -n 3 -f MyEvaluationFunction -2 ReversiRandomAI
./compete.py -1 ReversiRandomAI -2 ReversiAlphaBetaAI -n 3 -f MyEvaluationFunction 
~~~

## Exercise 4: Iterative deepening + Alpha-Beta

~~~
./reversi.py -1 ReversiAlphaBetaAI -n 6 -2 ReversiGreedyAI
./reversi.py -1 ReversiIterativeAlphaBetaAI -n 6 -2 ReversiGreedyAI
~~~
