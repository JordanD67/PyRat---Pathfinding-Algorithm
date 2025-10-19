MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
move=[]
initial_vertex=(0,0)
all_explored_vertices = []

import heapq
import operator

'''the 'create_structure' function creates an empty list
*Input*
None
*Output*
--*list*--
'''
def create_structure () : # création d'une structure vide
  return []

'''the 'create_structure' function add an element to a list
*Input*
structure --*list*--
element --*string, int, float*--
*Output*
None
'''
def push_to_structure (structure, element) : # inserstion d'un nouvel élément dans la structure
  heapq.heappush(structure, element)

'''the 'pop_from_structure' function reurn and remove the smallest element
*Input*
structure --*list((int,pair(int,int))*--
*Output*
Smallest element from structure
'''
def pop_from_structure (structure) : # renvoie l'élément de valeur minimale et l'enlève de la structure
  return heapq.heappop(structure)

'''the 'move_from_locations' function gives the displacement that allows to go from source_location to target_location
*Input*
source_location --**pair(int,int)**-- is where you want to move from
target_location --**pair(int,int)**-- is where you want to move to

*Output*
A  move among `MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT` or `MOVE_RIGHT`'''

def move_from_locations (source_location, target_location) :   # Sert à trouver la direction dans laquelle aller à partir de deux cases adjacentes co-accessible
    difference = (target_location[0] - source_location[0], target_location[1] - source_location[1])
    if difference == (0, -1) :
        return MOVE_DOWN
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (-1, 0) :
        return MOVE_LEFT
    else :
        raise Exception("Impossible move")

'''the build_meta_graph create a complete graph containing locations
*Input*
graph -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze where the game takes place. This structure associates each cell with the dictionry of its neighbors. In that dictionary of neighbors, keys are cell coordinates, and associated values the number of moves required to reach that neighbor. As an example, `list(maze_map[(0, 0)].keys())` returns the list of accessible cells from `(0, 0)`. Then, if for example `(0, 1)` belongs to that list, one can access the number of moves to go from `(0, 0)` to `(0, 1)` by the code `maze_map[(0, 0)][(0, 1)]`.
location --**list(pair(int,int))**-- is where you want to move to

*Output*
meta_graph --**dict(pair(int, int), dict(pair(int, int), int))**-- Complete graph
routing_table --**dict(pair(int,int))'''

def build_meta_graph (maze_map, locations) :        # Return the meta-graph and all necessary routing tables
  meta_graph={location : {} for location in locations}        #Création du meta_graph qui est de la même forme que maze_map
  routing_tables={}                                           #Création de routing_tables qui contient toutes les routing_table 
  for location in locations:                                                    #On parcourt les sommets du méta_graph
    routing_table, explored_vertices = dijkstra(location, maze_map)             #On applique dijkstra à ce sommet
    routing_tables[location]=routing_table                                      #On incrémente routing_tables avec la routing_table de ce sommet
    for neighbor in locations:                                                  #On parcourt les voisins de ce sommet
      if neighbor!=location :                                                   #On élimine le cas ou le voisin est le sommet
        meta_graph[location][neighbor]= explored_vertices[neighbor]             #On incrémente le méta_graph
        meta_graph[neighbor][location]=meta_graph[location][neighbor] 
  return meta_graph, routing_tables

'''the dijkstra function gives a routing table corresponding to the BFS algorithm and the visited places
*Input*
graph -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze where the game takes place. This structure associates each cell with the dictionry of its neighbors. In that dictionary of neighbors, keys are cell coordinates, and associated values the number of moves required to reach that neighbor. As an example, `list(maze_map[(0, 0)].keys())` returns the list of accessible cells from `(0, 0)`. Then, if for example `(0, 1)` belongs to that list, one can access the number of moves to go from `(0, 0)` to `(0, 1)` by the code `maze_map[(0, 0)][(0, 1)]`.
start_vertex  -- **pair(int, int)** -- The initial location of your character in the maze.
*Output*
explored_vertices --**list(pair(int,int))**-- contains all the visited locations
routing_table --**dict(pair(int,int))'''

def dijkstra (start_vertex, graph) :    # Sert à trouver le plus court chemin dans un graphe pondéré 
# initialisation de la queueing_structure avec le sommet initial, à la distance 0, et sans parent
  queue=[]
  push_to_structure(queue, (0, start_vertex, None))
# initialisation de explored_vertices et routing_table
  explored_vertices = {}
  routing_table = {}
  while queue != [] :      # On s'arrête que quand la queue_structure est vide
    (distance,vertex,parent) = pop_from_structure(queue) # On sélectionne un sommet, avec les données associées
    if vertex not in explored_vertices:       # On regarde si il est déjà dans explored_vertices
      explored_vertices[vertex] = distance    # Si non, on l'insère 
      routing_table[vertex] = parent          # On incrémente la routing_table pour savoir comment rejoindre ce sommet de la plus courte manière 
      for neighbor in graph[vertex]:          # On regarde les voisins de ce sommet
        if neighbor not in explored_vertices:       # Pour optimiser, on ne s'occupe que des voisins qu'on n'a pas déjà visité
          distance_to_neighbor = distance + graph[vertex][neighbor]     # On met à jour la distance pour rejoindre ces voisins afin de choisir le bon chemin
          push_to_structure(queue, (distance_to_neighbor, neighbor,vertex))               # On insère les voisins dans la queueing_structure
  return (routing_table , explored_vertices)         # On renvoie la routing_table et explored_vertices

'''the give_score function associate a score (length of path) to each given neighbor
*Input*
current_vertex  -- **pair(int, int)** -- The current location of your character in the maze
neighbor  -- **lsit(pair(int, int))** --

*Output*
score --**dict(pair(int,int),int)'''

def give_score (graph, current_vertex, neighbors) :                             # Associate a score (length of path) to each given neighbor
  scores={}                                                                     # On crée le dictionnaire scores qui à chaque voisin associe le score correspondant
  (routing_table, explored_vertices)=dijkstra(current_vertex, graph)            # On applique dijkstra à current_vertex pour obtenir la distance entre current_vertex et ses voisins
  for neighbor in neighbors :                                                   # On incrémente scores en itérant sur les voisins de current_vertex
    scores[neighbor]=explored_vertices[neighbor]
  return scores

'''the find_route function give a list of position to follow to go from source_location to target_locaiton
*Input*
routing_table -- **dict(pair(int, int))** -- 
source_location  -- **pair(int, int)** -- The initial location of your character in the maze
target_location  -- **pair(int, int)** -- The location you want to go to

*Output*
route --**list(pair(int,int))'''

def find_route(routing_tables, location, target_location):  # Sert à trouver le chemin le plus court entre deux cases à partir de leur routing_table
  route=[]
  parent=target_location                 # On crée la variable parent qui sera modifié à chaque tour de boucle
  while parent != location :           # Tant qu'on est pas remonté à la case initiale on continue la boucle
    parent=routing_tables[location][parent]                   #parent devient le fils correspondant
    route.append(parent)                         # On incrémente la variable route
  route.reverse()                 # On renverse la liste
  return route  

'''the find_route2 function give a list of position to follow to go from source_location to target_locaiton
*Input*
routing_table -- **dict(pair(int, int))** -- 
source_location  -- **pair(int, int)** -- The initial location of your character in the maze
target_location  -- **pair(int, int)** -- The location you want to go to

*Output*
route --**list(pair(int,int))'''

def find_route2(routing_table, location, target_location):
  route=[]
  parent=target_location                 # On crée la variable parent qui sera modifié à chaque tour de boucle
  while parent != location :           # Tant qu'on est pas remonté à la case initiale on continue la boucle
    parent=routing_table[parent]                   #parent devient le fils correspondant
    route.append(parent)                         # On incrémente la variable route
  route.reverse()                 # On renverse la liste
  return route  

'''the meta_graph_route_to_route function gives a path to follow to perform a route in the meta graph
*Input*
graph -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze where the game takes place. This structure associates each cell with the dictionry of its neighbors. In that dictionary of neighbors, keys are cell coordinates, and associated values the number of moves required to reach that neighbor. As an example, `list(maze_map[(0, 0)].keys())` returns the list of accessible cells from `(0, 0)`. Then, if for example `(0, 1)` belongs to that list, one can access the number of moves to go from `(0, 0)` to `(0, 1)` by the code `maze_map[(0, 0)][(0, 1)]`.
location --**list(pair(int,int))**-- is where you want to move to

*Output*
meta_graph --**dict(pair(int, int), dict(pair(int, int), int))**-- Complete graph
route --**dict(pair(int,int))'''
def meta_graph_route_to_route (meta_graph_route, routing_tables) :              
  route=[]                                                                      #On crée une route vide que l'on va compléter
  for i in range(len(meta_graph_route)-1):
    route += find_route(routing_tables, meta_graph_route[i], meta_graph_route[i+1])
  route.append(meta_graph_route[-1])
  return route    

'''the greedy function gives a path to follow to perform a route in the graph performing the greedy algorithm
*Input*
graph -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze where the game takes place. This structure associates each cell with the dictionry of its neighbors. In that dictionary of neighbors, keys are cell coordinates, and associated values the number of moves required to reach that neighbor. As an example, `list(maze_map[(0, 0)].keys())` returns the list of accessible cells from `(0, 0)`. Then, if for example `(0, 1)` belongs to that list, one can access the number of moves to go from `(0, 0)` to `(0, 1)` by the code `maze_map[(0, 0)][(0, 1)]`.
initial_vertex --**pair(int,int)**--
routing_table -- **dict(pair(int, int))** -- 

*Output*
meta_graph --**dict(pair(int, int), dict(pair(int, int), int))**-- Complete graph
route --**dict(pair(int,int))'''   
def greedy (graph, initial_vertex, vertices_to_visit, routing_tables) :         # Greedy algorithm that goes to the score minimizer until all vertices are visited
  scores=give_score(graph, initial_vertex, vertices_to_visit)
  next_vertex=min(scores, key=scores.get)
  return meta_graph_route_to_route([initial_vertex, next_vertex], routing_tables)


'''the moves function give all the moves to do to follow a path
*Input*
route --**list(pair(int,int))

*Output*
move --** list of move among `MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT` or `MOVE_RIGHT`'''  
def moves(route):
  move = []
  for i in range(len(route)-1):
    move.append(move_from_locations(route[i], route[i+1]))
  return move

'''the densité return the density of cheese in each square
*Input*
`maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze. It is the same as in the `preprocessing` function, just given here again for convenience.
`maze_width` -- **int** -- The width of the maze, in number of cells.
`maze_height` -- **int** -- The height of the maze, in number of cells.
`pieces_of_cheese` -- **list(pair(int, int))** -- The location of remaining pieces of cheese in the maze.
 n --*int*--
 `player_location` -- **pair(int, int)** -- The current location of your character in the maze.
*Output*
densité --**dict(pair(int,int),int)**-'''  

def densité(maze_map, maze_width, maze_height, pieces_of_cheese, n,player_location):
  """
  fonction qui pour chaque carré de côté n (impair) dans le maze_map, renvoie le nombre de fromage contenue dans ce carré
  """
  densité = {}                  # dictionnaire qui à chaque centre de carré va renvoyer le nombre de fromage dans ce carré
  if n ==3 :
      pas = 1
  else :
      pas = int((n-1)/2)
  if player_location == (0,0):  #On différencie les cas en fonction de la position de départ
      for i in range(pas, maze_width-pas + 1):   #Parcourt de tous les carrés en dessous de la diagonale
          for j in range(pas, maze_height - i + 1):
              sum = 0
              for i2 in range(i-pas, i+pas+1):   #Parcourt de l'intérieur des carrés
                  for j2 in range(j-pas, j+pas+1):
                      
                      
                      if (i2,j2) in pieces_of_cheese:
              
                          sum+=1
                          densité[(i,j)]=sum
  else:                                             #Deuxième cas
      for i in range(pas, maze_width-pas):
          for j in range(maze_height-i,maze_height - pas + 1):
              sum = 0
              for i2 in range(i-pas, i+pas+1):
                  for j2 in range(j-pas, j+pas+1):
                      
                      
                      if (i2,j2) in pieces_of_cheese:
              
                          sum+=1
                          densité[(i,j)]=sum
      
  return densité
'''the road_to_take_cheese_on_the_road return the density of cheese in each square
*Input*
`maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze. It is the same as in the `preprocessing` function, just given here again for convenience.
`pieces_of_cheese` -- **list(pair(int, int))** -- The location of remaining pieces of cheese in the maze.
 distance_max --*int*--
 `player_location` -- **pair(int, int)** -- The current location of your character in the maze.
*Output*
road_to_cheese **--list(pair(int,int))'''  
def road_to_take_cheese_on_the_road(player_location, pieces_of_cheese, distance_max, maze_map):
  road_to_cheese = []
  routing_table, explored_vertices = dijkstra(player_location, maze_map)
  distances_to_cheese = {}
  for cheese_locations in pieces_of_cheese:         #On cherche le fromage le plus proche
    distances_to_cheese[cheese_locations] = explored_vertices[cheese_locations]
  nearest_cheese, min_distance = min(distances_to_cheese.items(), key=operator.itemgetter(1))
  if min_distance<=distance_max:                    #On regarde si le fromage le plus proche est assez proche 
    road_to_cheese=find_route2(routing_table, player_location, nearest_cheese)+[nearest_cheese]
  return road_to_cheese

"""<h1><b><center>PyRat functions</center></b></h1>

The `preprocessing` function is called at the very start of a game. It is attributed a longer time compared to `turn`, which allows you to perform intensive computations. If you store the results of these computations into **global** variables, you will be able to reuse them in the `turn` function.

*Input:*
*   `maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze where the game takes place. This structure associates each cell with the dictionry of its neighbors. In that dictionary of neighbors, keys are cell coordinates, and associated values the number of moves required to reach that neighbor. As an example, `list(maze_map[(0, 0)].keys())` returns the list of accessible cells from `(0, 0)`. Then, if for example `(0, 1)` belongs to that list, one can access the number of moves to go from `(0, 0)` to `(0, 1)` by the code `maze_map[(0, 0)][(0, 1)]`.
*   `maze_width` -- **int** -- The width of the maze, in number of cells.
*   `maze_height` -- **int** -- The height of the maze, in number of cells.
*   `player_location` -- **pair(int, int)** -- The initial location of your character in the maze.
*   `opponent_location` -- **pair(int,int)** -- The initial location of your opponent's character in the maze.
*   `pieces_of_cheese` -- **list(pair(int, int))** -- The initial location of all pieces of cheese in the maze.
*   `time_allowed` -- **float** -- The time you can take for preprocessing before the game starts checking for moves.

*Output:*
*   This function does not output anything.
"""

def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global initial_vertex
    density = densité(maze_map, maze_width, maze_height, pieces_of_cheese, 13,player_location)
    
    initial_vertex=max(density, key=lambda key: density[key])
    

"""The `turn` function is called each time the game is waiting
for the player to make a decision (*i.e.*, to return a move among those defined above).

*Input:*
*   `maze_map` -- **dict(pair(int, int), dict(pair(int, int), int))** -- The map of the maze. It is the same as in the `preprocessing` function, just given here again for convenience.
*   `maze_width` -- **int** -- The width of the maze, in number of cells.
*   `maze_height` -- **int** -- The height of the maze, in number of cells.
*   `player_location` -- **pair(int, int)** -- The current location of your character in the maze.
*   `opponent_location` -- **pair(int,int)** -- The current location of your opponent's character in the maze.
*   `player_score` -- **float** -- Your current score.
*   `opponent_score` -- **float** -- The opponent's current score.
*   `pieces_of_cheese` -- **list(pair(int, int))** -- The location of remaining pieces of cheese in the maze.
*   `time_allowed` -- **float** -- The time you can take to return a move to apply before another time starts automatically.

*Output:*
*   A chosen move among `MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT` or `MOVE_RIGHT`.
"""    

def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
  global initial_vertex
  global move
  global all_explored_vertices
  if player_location not in all_explored_vertices:
    all_explored_vertices.append(player_location)
  #Until we get to the initial_vertex we pickup the closest cheeses
  while initial_vertex not in all_explored_vertices:
    road_to_cheese = road_to_take_cheese_on_the_road(player_location, pieces_of_cheese, 4, maze_map)
    if road_to_cheese != []:    #No cheese close enough
      move3 = moves(road_to_cheese)
      return move3[0]
                                  #A cheese is close enough, looking for the shortest path to get it
    routing_table, explored_vertices = dijkstra(player_location, maze_map) 
    route=find_route2(routing_table, player_location, initial_vertex)+[initial_vertex]
    move=moves(route)

    return move.pop(0)
  #When we get to initial_vertex we do a greedy algorithm
  meta_graph, routing_tables=build_meta_graph(maze_map, pieces_of_cheese + [player_location])
  route=greedy(meta_graph, player_location, pieces_of_cheese, routing_tables)
  move2=moves(route)
  return move2.pop(0)