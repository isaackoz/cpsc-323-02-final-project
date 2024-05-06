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
<prog>              ->  program <identifier>; var <dec-list> begin <stat-list> end.
<identifier>        ->  <letter><post-identifier>
<post-identifier>   ->  <letter><post-identifier>
<post-identifier>   ->  <digit><post-identifier>
<post-identifier>   ->  λ
<dec-list>          ->  <dec>:<type>;
<dec>               ->  <identifier>,<dec>
<dec>               ->  <identifier>
<type>              ->  integer
<stat-list>         ->  <stat>
<stat-list>         ->  <stat><stat-list>
<stat>              ->  <write>
<stat>              ->  <assign>
<write>             ->  write(<str><identifier>);
<str>               ->  "value=",
<str>               ->  λ
<assign>            ->  <identifier>=<expr>;
<expr>              ->  <term><term'>
<expr'>             ->  +<term><term'>
<expr'>             ->  -<term><term'>
<expr'>             ->  λ
<term>              ->  <factor><term'>
<term'>             ->  *<factor><term'>
<term'>             ->  /<factor><term'>
<term'>             ->  λ
<number>            ->  <sign><digit><post-number>
<post-number>       ->  <digit><post-number>
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
