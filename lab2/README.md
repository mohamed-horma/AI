# Constraint Satisfaction Problem with Takuzu

##  DFS (aka Backtracking)

~~~
python3 takuzu.py --agent DFS --grid takuzu1.txt
./takuzu.py -a DFS -g takuzu2.txt
./takuzu.py -a DFS -g takuzu3.txt
./takuzu.py -a DFS -g takuzu4.txt
./takuzu.py -a DFS -g takuzu5.txt
~~~

## Exercise 1: Forward Checking

~~~
./takuzu.py -a FC -g takuzu1.txt
./takuzu.py -a FC -g takuzu2.txt
./takuzu.py -a FC -g takuzu3.txt
./takuzu.py -a FC -g takuzu4.txt
./takuzu.py -a FC -g takuzu5.txt
~~~

## Exercise 2: Forward Checking with heuristic

~~~
./takuzu.py -a FC -g takuzu3.txt -f my_heuristic
./takuzu.py -a FC -g takuzu4.txt -f my_heuristic
./takuzu.py -a FC -g takuzu5.txt -f my_heuristic
~~~

## Exercise 3: Arc Consistency

~~~
./takuzu.py -a AC -g takuzu3.txt -f my_heuristic
./takuzu.py -a AC -g takuzu4.txt -f my_heuristic
./takuzu.py -a AC -g takuzu5.txt -f my_heuristic
~~~

## Exercise 4: Maintening Arc Consistency

~~~
./takuzu.py -a MAC -g takuzu3.txt -f my_heuristic
./takuzu.py -a MAC -g takuzu4.txt -f my_heuristic
./takuzu.py -a MAC -g takuzu5.txt -f my_heuristic
~~~
