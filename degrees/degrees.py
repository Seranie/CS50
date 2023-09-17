import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO

    frontier = []
    explored = []

    # initialize starting node (to put into frontier)
    node = {}
    node['id'] = source
    node['parent'] = None
    node['action'] = None
    frontier.append(node)
    foo = None
    while True:
        foo, bar = explore(frontier, target, explored)
        if bar == False:
            frontier = foo
            continue
        else:
            break
        
    return foo



    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


def queueFrontier(node, frontier, explored):
    
    for row in frontier:
        if node['id'] == row['id']:
            return
    for row in explored:
        if node['id'] == row['id']:
            return

    return frontier.append(node)
    
        


def explore(frontier, endState, explored):
    # check if frontier is empty
    if len(frontier) == 0:
        return None, None

    # removes and stores first element of frontier
    currentNode = frontier[0]

    # else remove 1st element from frontier
    frontier = frontier[1:]

    # add explored path to explored
    explored.append(currentNode)

    # find frontiers from this current node/
    parent = currentNode['id'] 

    for action in neighbors_for_person(parent):

        # prepare node/
        id = list(action)[1]
        dic = {'id' : id, 'action': action, 'parent': parent}

        # check if current node is goal node
        if endGame(dic, endState):
            madePath = []
            makePath(dic, madePath, explored)
            madePath = list(reversed(madePath))
            return madePath, None

        # add to frontier
        queueFrontier(dic, frontier, explored)

    return frontier, False



def endGame(node, endState):
    if node['id'] == endState:
        return True
    else:
        return False


def makePath(currentNode, path, explored):
    if currentNode['action'] == None:
        return
    else:
        action = currentNode['action']
        path.append(action)
        nextNode = None
        for row in explored:
            if currentNode['parent'] == row['id']:
                nextNode = row
                break
    return makePath(nextNode, path, explored)
        
    


if __name__ == "__main__":
    main()
