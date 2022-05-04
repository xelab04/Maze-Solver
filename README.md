# Maze-Solver
So, uhm, included in this magnificent package, you have 4 AI search algorithms:
      - Breadth First Search
      - Depth First Search
      - Greedy Best First Search
      - A* Search
      
You are free to save your own mazes in the file "savestates" for easy retrieval.
There are 3 mazes I saved already for the purpose of a presentation and they allow you to play around and test the limitations of each algorithm used.

Controls:
The UI is not very user-friendly.
"z" : Prints out the current state of the maze in the terminal. Useful for getting the state of a board to be saved for later.
"x" : Resets the grid, removing all squares which are neither black nor white.
"c" :
    1 press: sets down starting position
    2 press: sets down goal position
    3 press: runs the solver AI
"v" : Cycles through the AI algorithms. Selected algorithm is output to the terminal.
"w" : Cycles through the saves 1,2 and 3.

Known Issues:
1. There are some annoyances, especially when it comes to the UI. I will be refining the interface in the future.
2. All algorithms work great other than BFS which gets slow if the starting point is placed in the middle of the maze without any walls.
3. Need to update the "w" key to work with any number of saves in savestates.py.
4. "c" is not intuitive to use since it tends to malfunction if the user uses it wrongly.
