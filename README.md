

## A couple notes on compatibility

1. I wrote all of this code in python3.6 and I doubt it  will work on python 2.(whatever). About that.. Python 2 is outdated. Stop using it.

2. The majority of my visualization stuff depends on `imageio` and `graphviz` which are two packages in Ubuntu repositories as `python3-imagio` and `python3-graphviz`.

3. I also have to do some minor file management to make the `.gif` images and because of this, I doubt that feature will work on MS machines, though I suspect only minimal modifications would be needed to make that work.. If you wanted to help, you could fork this repo and ensure compatibility in some Win10 dev enviroment. 


## Programmed

This directory contains my solutions to the programmed assignment.
The tenth assignment has been omitted because it has not been turned in
yet. I have also included my .tex files and my pdf reports.

## Written

Okay, this is also pretty obvious. This contains my solutions to all
of the written homeworks (pdf and tex files again).

## exam1

This directory has implementations of (almost) everything we covered up to 
the first exam. I sent this around in an email to the class shortly beforehand
and some people seemed to find it useful.

## final

okay, this is under construction. I have so far implemented a red black tree 
with insertion and deletion that draws images of insertion and deletion
in sequence at runtime. The API is almost identicle to the pseudocode syntax in
the text. I intend to begin writing code to do some 
Dynamic programming, greedy algorithms, and all of the graph algorithms.

When I am done, every function that I implement should include runtimes 
and some light commentary on the algorithm that is (probably) unclear in 
the text. 

It is my hope and intention that this will be useful to you guys. Note that some
of my code requires some packages (easily installed with apt, pacman, pip, or whatever).
Information about dependencies should be stored in file headers, but I am lazy and this
is informal, so I don't feel too bad if I missed something. If you notice any errors,
I'll fix them.


# Breadth first search example animation
![alt text](https://github.com/amo004/Algorithms/blob/master/final/GraphSearch/bfs.gif)

# Depth first search example animation
![alt text](https://github.com/amo004/Algorithms/blob/master/final/GraphSearch/dfs.gif)


# Prim's algorithm example animation
![alt text](https://github.com/amo004/Algorithms/blob/master/final/GraphSearch/mst.gif)
