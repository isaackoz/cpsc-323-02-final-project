# cpsc-323-02-final-project
A compiler in Python using Predictive Parsing (LL)

## Setup
1. Create a folder and then open up the terminal
2. Type `git clone https://github.com/isaackoz/cpsc-323-02-final-project.git`
3. Cd into folder `cd cpsc-323-02-final-project`
4. Change your branch to your own `git checkout -b my-branch-name`
5. Make your changes
6. When you're ready to commit, type in `git commit -a -m "commit message"` which stages all modified files and adds a commit message
7. `git push` or `git push --set-upstream origin my-branch-name` if the former doesn't work
8. Then on github, go to your branch, click `contribute`, then press `Open Pull Request`. Then click `Create Pull Request`.
9. Pull requests ensure we're all on the same page.
10. To synchronize your branch to `main`  
    1. `git checkout main`
    2. `git pull`
    3. `git checkout my-branch-name`
    4. `git merge main`

## Grammar
Left-recursion and in BNF form.
```text
<prog>              ->  program <identifier> ; var <dec-list> begin <stat-list> end.
<identifier>        ->  <letter> <post-identifier>
<post-identifier>   ->  <letter> <post-identifier>
<post-identifier>   ->  <digit> <post-identifier>
<post-identifier>   ->  λ
<dec-list>          ->  <dec> : <type> ;
<dec>               ->  <identifier> <post-dec>
<post-dec>          ->  , <dec>
<post-dec>          ->  λ
<type>              ->  integer
<stat-list>         ->  <stat> <post-stat-list>
<post-stat-list>    ->  <stat> <post-stat-list>
<post-stat-list>    ->  λ
<stat>              ->  <write>
<stat>              ->  <assign>
<write>             ->  write ( <str> <identifier> );
<str>               ->  "value=" ,
<str>               ->  λ
<assign>            ->  <identifier> = <expr> ;
<expr>              ->  <term> <post-expr>
<post-expr>         ->  + <term> <post-expr>
<post-expr>         ->  - <term> <post-expr>
<post-expr>         ->  λ
<term>              ->  <factor> <post-term>
<post-term>         ->  * <factor> <post-term>
<post-term>         ->  / <factor> <post-term>
<post-term>         ->  λ
<factor>            ->  <identifier>
<factor>            ->  <number>
<factor>            ->  ( <expr> )
<number>            ->  <sign> <digit> <post-number>
<post-number>       ->  <digit> <post-number>
<post-number>       ->  λ
<sign>              ->  +
<sign>              ->  -
<sign>              ->  λ
<digit>             ->  0
<digit>             ->  1
<digit>             ->  2
<digit>             ->  3
<digit>             ->  4
<digit>             ->  5
<digit>             ->  6
<digit>             ->  7
<digit>             ->  8
<digit>             ->  9
<letter>            ->  p
<letter>            ->  q
<letter>            ->  r
<letter>            ->  s
```

## Grammar with short-hand letters for simplification
```text
S       ->  program A ; var C begin F end.
A       ->  T B
B       ->  T B
B       ->  R B
B       ->  λ
C       ->  D : E ;
D       ->  A V
V       ->  , D
V       ->  λ
E       ->  integer
F       ->  G W
W       ->  G W
W       ->  λ
G       ->  H
G       ->  J
H       ->  write ( I A );
I       ->  "value=" ,
I       ->  λ
J       ->  A = K ;
K       ->  M L
L       ->  + M L
L       ->  - M L
L       ->  λ
M       ->  U N
N       ->  * U N
N       ->  / U N
N       ->  λ
U       ->  A
U       ->  O
U       ->  ( K )
O       ->  Q R P
P       ->  R P
P       ->  λ
Q       ->  +
Q       ->  -
Q       ->  λ
R       ->  0
R       ->  1
R       ->  2
R       ->  3
R       ->  4
R       ->  5
R       ->  6
R       ->  7
R       ->  8
R       ->  9
T       ->  p
T       ->  q
T       ->  r
T       ->  s
```