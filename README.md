# Python: first & follow
A simple python script to compute the first &amp; follow of variables in a context-free grammar

## How to run
Create a .txt with your grammar in the same format as the sample input below with your productions spaced (ex. A B C).
The script does not print anything but generates a file with the output.
```
python3 task_5_1.py --file your_grammar_file.txt
```

## Sample input 
```
S : A B C D E
A : a | epsilon
B : b | epsilon
C : c
D : d | epsilon
E : e | epsilon
```

## Sample output
Variable : First : Follow
```
S : a b c : $
A : a epsilon : b c
B : b epsilon : c
C : c : d e $
D : d epsilon : e $
E : e epsilon :
```
