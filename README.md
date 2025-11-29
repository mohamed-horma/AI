# State-Space Search Problem with Sokoban

## Run "By hand"

~~~
python3 sokoban.py --grid puzzle1.txt

./sokoban.py --agent DFS --grid puzzle1.txt
./sokoban.py -a DFS -g puzzle2.txt
~~~


### Note:

By default, Python3 3 uses hash randomization which leads to random number
of explored states with the above execution.
This prevents comparing the number of explored states with those examples given.

To turn this off use, on Linux:

    export PYTHONHASHSEED=0

or on Windows:

    set PYTHONHASHSEED=0


## Exercise 1: Breadth First Search

~~~
./sokoban.py -a BFS -g puzzle1.txt
./sokoban.py -a BFS -g puzzle2.txt
./sokoban.py -a BFS -g puzzle3.txt
./sokoban.py -a BFS -g puzzle4.txt
~~~

## Exercise 2: Greedy Best-First Search

~~~
./sokoban.py -a GBFS -g puzzle1.txt
./sokoban.py -a GBFS -g puzzle2.txt
./sokoban.py -a GBFS -g puzzle3.txt
./sokoban.py -a GBFS -g puzzle4.txt
./sokoban.py -a GBFS -g puzzle5.txt
./sokoban.py -a GBFS -g puzzle6.txt
~~~

## Exercise 3: A* Search

~~~
./sokoban.py -a ASS -g puzzle1.txt
./sokoban.py -a ASS -g puzzle2.txt
./sokoban.py -a ASS -g puzzle3.txt
./sokoban.py -a ASS -g puzzle4.txt
./sokoban.py -a ASS -g puzzle5.txt
./sokoban.py -a ASS -g puzzle6.txt
~~~

## Exercise 4: Iterative Deepening Search

~~~
./sokoban.py -a IDS -g puzzle1.txt
./sokoban.py -a IDS -g puzzle2.txt
./sokoban.py -a IDS -g puzzle3.txt
./sokoban.py -a IDS -g puzzle4.txt
./sokoban.py -a IDS -g puzzle5.txt
./sokoban.py -a IDS -g puzzle6.txt
~~~


## Exercise 5: Iterative Deepening A* Search

~~~
./sokoban.py -a IDASS -g puzzle1.txt
./sokoban.py -a IDASS -g puzzle2.txt
./sokoban.py -a IDASS -g puzzle3.txt
./sokoban.py -a IDASS -g puzzle4.txt
./sokoban.py -a IDASS -g puzzle5.txt
./sokoban.py -a IDASS -g puzzle6.txt
~~~
