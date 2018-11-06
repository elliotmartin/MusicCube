import rubik
import random

from collections import deque


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves.

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end: return []

    forward_parents = {start: None}
    backward_parents = {end: None}
    forward_moves = {}
    backward_moves = {}
    for move in rubik.quarter_twists:
        forward_moves[move] = move
        backward_moves[rubik.perm_inverse(move)] = move
    forward = (forward_moves, forward_parents, backward_parents)
    backward = (backward_moves, backward_parents, forward_parents)
    queue = deque([(start, forward), (end, backward), None])

    for i in range(7):
        while True:
            vertex = queue.popleft()
            if vertex is None:
                queue.append(None)
                break
            position = vertex[0]
            moves, parents, other_parents = vertex[1]
            for move in moves:
                next_position = rubik.perm_apply(move, position)
                if next_position in parents: continue
                parents[next_position] = (moves[move], position)
                queue.append((next_position, vertex[1]))
                if next_position in other_parents:
                    forward_path = path(next_position, forward_parents)
                    backward_path = path(next_position, backward_parents)
                    backward_path.reverse()
                    return forward_path + backward_path

    return None


def path(position, parents):
    path = []
    while True:
        move_position = parents[position]
        if move_position is None:
            path.reverse()
            return path
        path.append(move_position[0])
        position = move_position[1]

#takes the steps from shortest path and turns them to cube notation steps
def solution_to_turns(solution):
    return [rubik.quarter_twists_names[step] for step in solution]

#take a starting position and a solution and returns a list of all the cubes from applying each turn in the solution
def get_states(start, solution_steps):
    current = start
    states = []
    states.append(start)
    for step in solution_steps:
        next = rubik.perm_apply(step, current)
        states.append(next)
        current = next
    return states

#extracts just the front faces of a solution of a solution
def front(solution):
    chords = []
    for step in solution:
        chord = []
        chord.append(step[0])
        chord.append(step[3])
        chord.append(step[6])
        chord.append(step[9])
        chords.append(chord)

    return chords

#takes a list of states and extracts just the front face
def fronts_to_chords(states):
    chords = []
    for state in states:
        chords.append(list(rubik.num_to_notes[s] for s in state))
    return chords

def get_scramble(length):
    scramble = []
    for i in range(length):
        scramble.append(random.choice(rubik.quarter_twists))
    return scramble

def random_cube():
    scramble = get_scramble(40)
    cube = rubik.I
    for s in scramble:
        cube = rubik.perm_apply(s, cube)
    return cube

#create a random cube, get the solution, return the chords
def make_music():
    cube = random_cube()
    sol = shortest_path(cube, rubik.I)
    positions = get_states(rubik.I, sol)
    fronts = front(positions)
    chords = fronts_to_chords(fronts)
    #chords.append(['C', 'E', 'G', 'Bb'])
    return chords

if __name__ == '__main__':
    print(make_music())
