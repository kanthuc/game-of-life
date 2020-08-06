# game-of-life

*Conway's Game of Life* is a very popular celular automaton, a model consisting of cells within a grid that have two states -- alive and dead -- that are influenced by the arrangement of the cells in the previous grid state. The model iterates through each grid state continuously and studying the shifting patterns and systems that are possible within this model has become a popular pastime of many mathemeticians, biologists, physicists, and nerds alike. The rules are very simple.

Each cell in the infinite grid depends on its 8 nieghboring cells to live in the next grid state. A cell will be alive in the next grid state if:

1. Its current state is alive and it has 2 or 3 live neighbors
2. Its current state is dead and it has exactly 3 live neighbors

All other cells will be in the 'dead' state in the next grid state.

This program creates a visual display and simulation for the user that follows the rules of Conway's Game of Life. You can draw an initial pattern by toggling a cell with your left mouse click. From there, you can run an animation of the following evolving grid state, or manually flip through each grid state at your own pace. Enjoy.
