# Risk.py

This is a basic implementation of the board game Risk, written for a hackathon. The main goal of the project is to provide a framework for developing independent bot agents to play the game. There is a graphical representation of the game and a more performant mode where the graphics aren't rendered.

## Features

- Basic implementation of the Risk game mechanics
- Support for creating bot agents to play the game
- Graph-based optimizations for improved performance
- Wrote own C library to help performance in a critical region of the code.


## Files

    - `Agent.py`: This file provides an outline of how to design an independent Agent and makes it easy to plug into the Risk engine to simulate games. It defines the `Player` base class and the abstract methods that need to be implemented by custom bot agents.
    

    - `GraphOptimiser.c`: This file provides a performant method to traverse adjacent tiles in the Risk game. This was an experiment into how you'd extend Python code with C.

    - `RiskUI.py`: This file handles all the components that are not necessary for a player to know.




## Extending the Project

There are several areas where the project can be extended and improved:

- **Bug Fixing**: The current implementation may contain a few errors that need to be addressed.

- **Bot Development**: There is ample opportunity to create sophisticated bot agents to play the game.

- **Graph Optimizations**: Since Risk is inherently a graph-based game with vertices and edges, there are various optimizations that can be made to improve performance. For example, PKnight3 and Mel implemented the concept of "Islands" to improve the efficiency of the `get_maneouvrable_territories` function by 4x.

## How to build an Agent
    The `Player` class serves as a base class for creating bot agents. It defines the basic functionality and properties of a player in the Risk game. To create your own custom bot agent, you need to inherit from the `Player` class and implement the following abstract methods:

    1. `make_selection(self, available_territories: List['Territory']) -> 'Territory'`: This method is called during the initial territory selection phase. It should return the selected territory from the list of available territories.

    2. `add_infantry(self) -> 'Territory'`: This method is called during the infantry placement phase. It should return the territory where the player wants to place their infantry. It works on a singular infantry basis, with only one being placed per turn.

    3. `reinforce(self, total_reinforcements: int) -> List[Tuple['Territory', int]]`: This method is called during the reinforcement phase. It should return a list of tuples, where each tuple represents a territory and the number of reinforcements to be placed on that territory. The number of reinforcements placed should match the total_reinforcements.

    4. `invade(self, adjacent_territories: List[Tuple['Territory', List['Territory']]]) -> Tuple['Territory', 'Territory', int]`: This method is called during the invasion phase. It should return a tuple containing the source territory, the target territory, and the number of troops to use for the invasion. Like the add_infantry function it works on a turn by turn basis.

        If you do not wish to mount an invasion return None

    5. `manoeuvre(self, manoeuverable_territories: List[Tuple['Territory', List['Territory']]]) -> Tuple['Territory', 'Territory', int]`: This method is called during the maneuvering phase. It should return a tuple containing the source territory, the destination territory, and the number of troops to maneuver.


    The code also provides an example implementation of a bot agent called `RandomAgent`. This agent inherits from the `Player` class and implements the abstract methods using random choices. For example:

    - In the `make_selection` method, it randomly selects a territory from the available territories.
    - In the `add_infantry` method, it randomly selects a territory from its owned territories to place the infantry.
    - In the `reinforce` method, it randomly selects a territory and allocates all reinforcements to that territory.
    - In the `invade` method, it selects the territory with the maximum number of troops and targets the adjacent enemy territory with the minimum number of troops.
    - In the `manoeuvre` method, it randomly selects a source territory and a destination territory from the maneuverable territories and moves a random number of troops.

    You can use the `RandomAgent` as a starting point and modify its behavior to create your own custom bot agents.



