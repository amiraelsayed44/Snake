import numpy as np

def dist(state, goal):
    """
    Calculate the Manhattan distance between the current state and the goal.
    
    Parameters:
        state (np.array): The current position of the snake's head.
        goal (np.array): The target position (food).
        
    Returns:
        int: Manhattan distance between the state and the goal.
    """
    return abs(goal[0] - state[0]) + abs(goal[1] - state[1])

def greedy(direction, pos, goal, body):
    """
    Greedy pathfinding algorithm for snake movement.
    Chooses the next direction that minimizes the distance to the goal (food),
    while avoiding collisions with the snake's own body.

    Parameters:
        direction (str): The current movement direction of the snake.
        pos (np.array): Current position of the snake's head.
        goal (np.array): Position of the food.
        body (list): List of coordinates representing the snake's body.

    Returns:
        str: The best direction to move ('UP', 'DOWN', 'LEFT', 'RIGHT').
    """
    # Define possible directions and their respective movement vectors
    directions = ['DOWN', 'UP', 'LEFT', 'RIGHT']
    moves = np.array([[0, 10], [0, -10], [-10, 0], [10, 0]])

    # Calculate new positions for each direction
    state_dict = {d: pos + m for d, m in zip(directions, moves)}

    # Compute distances from each possible position to the goal
    distance_dict = {d: dist(pos + m, goal) for d, m in zip(directions, moves)}

    # Remove directions that would result in a collision with the snake's body
    for d in directions.copy():
        if list(state_dict[d]) in body:
            directions.remove(d)

    # Default to current direction
    change = direction

    # If no safe direction is available, continue in the current direction
    if len(directions) == 0:
        return change

    # If current direction is not valid, fall back to the first safe option
    if direction not in directions:
        change = directions[0]

    # Choose the direction that minimizes the distance to the goal
    for d in directions:
        if distance_dict[d] < distance_dict[change]:
            change = d

    return change
