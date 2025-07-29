
### A short hackathon project

This project was made during a 6-hour hackathon. The project is an interpreter for a novel programming language: describe a Statistics word problem (like the monty hall problem) in code, and the interpreter will automatically run all possible branches and determine the likelyhood that `pass` executes, assuming all `select` statements choose randomly from the provided options.

#### 'bychance' vs 'where'

In the language, there are two keywords, `bychance` and `where`. The keyword `where` is used for certainty: when a given criteria is guaranteed to be met. Meanwhile, `bychance` is used for *conditional probability*. (When we know an event _did_ happen, but that it wasn't _guaranteed_ to happen)

#### How do I run it?

If you want to run the code, you can run:

> python3 runner.py examples\\exampleName.txt

The example files have comments explaining what they represent. Additionally, use:

> python3 runner.py -h

for a list of arguments.

#### What next?

This was a one-day hackathon project, but I plan to start again and make a more complete version (without taking shortcuts in the design of the compiler, with a more practical language design, etc.) I plan to add it to my github in the future.