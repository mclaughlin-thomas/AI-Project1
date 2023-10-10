import csv
import gc
import time
import math
import random
from queue import PriorityQueue



class Node(object):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    def __init__(self, x, y, diagonal_moves):
        self.gval = 0
        self.hval = 0
        self.fval = 0
        self.xval = x
        self.yval = y
        self.neighbors = []
        self.previous = None
        self.wall = False
        self.diagonal_moves = diagonal_moves  # Added parameter for diagonal moves


        if random.randint(1, 100) < 11:
            self.wall = True

    def add_neighbors(self, grid,width, height):
        """
        Given: None
        Task: Create nodes to be used in a graph
        Return: None
        """
        x = self.xval
        y = self.yval
        if x < width-1 :
            self.neighbors.append(grid[x+1][y])
        if x > 0:
            self.neighbors.append(grid[x-1][y])
        if y < height-1:
            self.neighbors.append(grid[x][y+1])
        if y>0:
            self.neighbors.append(grid[x][y-1])
        if self.diagonal_moves:
            if x > 0 and y > 0:
                self.neighbors.append(grid[x - 1][y - 1])
            if x < width - 1 and y > 0:
                self.neighbors.append(grid[x + 1][y - 1])
            if x > 0 and y < height - 1:
                self.neighbors.append(grid[x - 1][y + 1])
            if x < width - 1 and y < height - 1:
                self.neighbors.append(grid[x + 1][y + 1])
               
    def __lt__(self, other):
        return self.fval < other.fval


def set_parameters():
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    try:
        width = int(input("Enter the width of the graph: "))
        height = int(input("Enter the height of the graph: "))

        is_valid = True if width <= 0 or height <= 0 else False
        if is_valid is True:
            print("Number too small. Try again.\n\n")
            set_parameters()
        return width, height
    except ValueError:
        print("Invalid input. Please enter valid integers.")
        return set_parameters()  # calls fcn again if user inputs data wrong

def disable_diagonal_moves(space):
    """
    Given a 2D graph of nodes, set diagonal_moves to False for all nodes.
   
    :param graph: A 2D list of Node objects.
    """
    for row in space:
        for node in row:
            node.diagonal_moves = False


def create_space(width, height, diag):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    space = [[Node(i, j, diag) for j in range(width)] for i in range(height)]
    gc.collect()


    print("Completed init neighbors's\n")
    gc.collect()

    return space


def remove_from_array (array, element):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    for i in range(len(array) - 1, -1, -1):
        if array[i] == element:
            array.pop(i)


def heuristic_manhattan(node_one, node_two):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    distance = abs(node_one.xval-node_two.xval) + abs(node_one.yval-node_two.yval) #Manhattan
    return distance
def heuristic_euclidean(node_one, node_two):
    dx = node_one.xval - node_two.xval
    dy = node_one.yval - node_two.yval
    return math.sqrt(dx * dx + dy * dy)


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
   
    while current != start:
        current = came_from[current]
        path.append(current)
       
    return list(reversed(path))

#SEARCHES START
#---------------------------------------

#ALLOW DIAG| MAN, EUC |START
def astar_manhattan(start_space, end_space, space, width, height):
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    cost_so_far[start_space] = 0
    closed_set = set()

    node = start_space  
    # Update start node's g, h, and f values

    frontier.put((0, node))

    opened_nodes = 0  # Initialize the counter for opened nodes

    while not frontier.empty():
        _, popped_node = frontier.get()
        print(popped_node.xval , " ", popped_node.yval)
        popped_node.add_neighbors(space, width, height)


        if popped_node.xval == end_space.xval and popped_node.yval == end_space.yval:
            print(f"nodes opened\n{opened_nodes}")
            path  = reconstruct_path(came_from, start_space, popped_node)
            return path, opened_nodes
        closed_set.add(popped_node)

        for neighbor in popped_node.neighbors:
            print(f"Going through neighbor @ {neighbor.xval}, {neighbor.yval}")
            if neighbor.wall:
                print("This neighbor is a wall, skipping!")
                continue
            if neighbor in closed_set:
                print("This neighbor has already been explored! not doing that again!")
                continue
            newG = cost_so_far[popped_node] + 1

            if neighbor not in cost_so_far or newG < cost_so_far[neighbor]:
                print("Adding stuff to frontier")
                cost_so_far[neighbor] = newG
                priority_f = newG + heuristic_manhattan(neighbor, end_space)
                frontier.put((priority_f, neighbor))
                came_from[neighbor] = popped_node
                opened_nodes += 1

        # Update neighbors' g, h, and f values
        for neighbor in popped_node.neighbors:
            if neighbor.wall is True:
                continue
            neighbor.gval = cost_so_far[neighbor]
            neighbor.hval = heuristic_euclidean(neighbor, end_space)
            neighbor.fval = neighbor.gval + neighbor.hval

    return None

def astar_euclidean(start_space, end_space, space, width, height):
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    cost_so_far[start_space] = 0
    closed_set = set()

    node = start_space  
    # Update start node's g, h, and f values

    frontier.put((0, node))

    opened_nodes = 0  # Initialize the counter for opened nodes

    while not frontier.empty():
        _, popped_node = frontier.get()
        print(popped_node.xval , " ", popped_node.yval)
        popped_node.add_neighbors(space, width, height)


        if popped_node.xval == end_space.xval and popped_node.yval == end_space.yval:
            print(f"nodes opened\n{opened_nodes}")
            return reconstruct_path(came_from, start_space, popped_node), opened_nodes
        closed_set.add(popped_node)

        for neighbor in popped_node.neighbors:
            print(f"Going through neighbor @ {neighbor.xval}, {neighbor.yval}")
            if neighbor in closed_set:
                print("This neighbor has already been explored! not doing that again!")
                continue
            if neighbor.wall:
                print("This neighbor is a wall, skipping!")
                continue
            newG = cost_so_far[popped_node] + 1

            if neighbor not in cost_so_far or newG < cost_so_far[neighbor]:
                print("Adding stuff to frontier")
                cost_so_far[neighbor] = newG
                priority_f = newG + heuristic_euclidean(neighbor, end_space)
                frontier.put((priority_f, neighbor))
                came_from[neighbor] = popped_node
                opened_nodes += 1

        # Update neighbors' g, h, and f values
        for neighbor in popped_node.neighbors:
            if neighbor.wall is True:
                continue
            neighbor.gval = cost_so_far[neighbor]
            neighbor.hval = heuristic_euclidean(neighbor, end_space)
            neighbor.fval = neighbor.gval + neighbor.hval

    return False
#ALLOW DIAG| MAN, EUC |END




#SAVE DATA START
#---------------------------------------

def save_data_euclidean_diag(path, i, total_time, node_count):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: Nonep
    """
    #file_path_results = "AI-Project1\Manhattan Data\ZEROWALLTWELVETHOUSAND\data.csv"
    file_path_results = "C:\\Users\mclaught\Documents\Wall\Euc\Diag\hr2\h8000\data.csv"
    #file_path_adjtable = "C:\\Users\Handrail\Desktop\Manhattan Data\ZEROWALLFOURTHOUSAND\Adjtable.csv"
   

    with open(file_path_results, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Use writerow to write the header (if any) and data rows
        for node in reversed(path):
            writer.writerow([node.xval, node.yval])
        writer.writerow(["total states(including start and goal)", i])
        writer.writerow(["Time for Astar", total_time])
        writer.writerow(["Nodes opened", node_count])

def save_data_manhattan_diag(path, i, total_time, node_count):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: Nonep
    """
    #file_path_results = "AI-Project1\Manhattan Data\ZEROWALLTWELVETHOUSAND\data.csv"
    file_path_results = "C:\\Users\mclaught\Documents\Wall\Man\Diag\hr2\h8000\data.csv"
    #file_path_adjtable = "C:\\Users\Handrail\Desktop\Manhattan Data\ZEROWALLFOURTHOUSAND\Adjtable.csv"
   

    with open(file_path_results, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Use writerow to write the header (if any) and data rows
        for node in reversed(path):
            writer.writerow([node.xval, node.yval])
        writer.writerow(["total states(including start and goal)", i])
        writer.writerow(["Time for Astar", total_time])
        writer.writerow(["Nodes opened", node_count])

def save_data_euclidean_noDiag(path, i, total_time, node_count):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: Nonep
    """
    #file_path_results = "AI-Project1\Manhattan Data\ZEROWALLTWELVETHOUSAND\data.csv"
    file_path_results = "C:\\Users\mclaught\Documents\Wall\Euc\hNoDiag\hr2\h8000\data.csv"
   
    #file_path_adjtable = "C:\\Users\Handrail\Desktop\Manhattan Data\ZEROWALLFOURTHOUSAND\Adjtable.csv"
   

    with open(file_path_results, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Use writerow to write the header (if any) and data rows
        for node in reversed(path):
            writer.writerow([node.xval, node.yval])
        writer.writerow(["total states(including start and goal)", i])
        writer.writerow(["Time for Astar", total_time])
        writer.writerow(["Nodes opened", node_count])
def save_data_manhattan_noDiag(path, i, total_time, node_count):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: Nonep
    """
    #file_path_results = "AI-Project1\Manhattan Data\ZEROWALLTWELVETHOUSAND\data.csv"
    file_path_results = "C:\\Users\mclaught\Documents\Wall\Man\hNoDiag\hr2\h8000\data.csv"
    #file_path_adjtable = "C:\\Users\Handrail\Desktop\Manhattan Data\ZEROWALLFOURTHOUSAND\Adjtable.csv"
   

    with open(file_path_results, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Use writerow to write the header (if any) and data rows
        for node in reversed(path):
            writer.writerow([node.xval, node.yval])
        writer.writerow(["total states(including start and goal)", i])
        writer.writerow(["Time for Astar", total_time])
        writer.writerow(["Nodes opened", node_count])
#---------------------------------------
#SAVE DATA END



def main():
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
   
    #TRUE FOR DIAGONAL
    #FALSE FOR NODIAG
    diag = True
    width, height = set_parameters()
    space = create_space(width, height, diag)
    start_space = space[0][0]    
    end_space = space[width-1][height-1]
    start_space.wall = False
    end_space.wall = False

    #DIAGONALS MAN AND EUC START
    print("\nStarting search\n")
    start = time.time() # Start Timer
    path, node_count  = astar_manhattan(start_space, end_space, space, width, height)
    end =  time.time() # End Timer
    total_time= end - start
    print(total_time)
    print("\nEnding search\n")


    if path:
        print("Path:\n")
        for node in path:
            print(f"({node.xval}, {node.yval})")
        print(f"Total path length: {len(path)-1}")
        print(f"Total time taken: {total_time} seconds")
        print(f"Nodes explored from openset: {node_count }")
        save_data_manhattan_diag(path, len(path)-1, total_time, node_count)
    else:
        print("No path found")


    print("Starting search")
    start1 = time.time() # Start Timer
    path, node_count  = astar_euclidean(start_space, end_space, space, width, height)
    end1 =  time.time() # End Timer
    total_time1= end1 - start1
    print(total_time1)
    print("Ending search")


    if path:
        print("Path:")
        for node in path:
            print(f"({node.xval}, {node.yval})")
        print(f"Total path length: {len(path)-1}")
        print(f"Total time taken: {total_time1} seconds")
        print(f"Nodes explored from openset: {node_count }")
        save_data_euclidean_diag(path, len(path)-1, total_time1, node_count)
    else:
        print("No path found")
       
#DIAGONALS MAN AND EUC END

    disable_diagonal_moves(space)

#NO DIAG MAN AND EUC START
    print("\nStarting search\n")
    start2 = time.time() # Start Timer
    path, node_count  = astar_manhattan(start_space, end_space, space, width, height)
    end2 =  time.time() # End Timer
    total_time2= end2 - start2
    print(total_time2)
    print("\nEnding search\n")


    if path:
         print("Path:\n")
         for node in path:
             print(f"({node.xval}, {node.yval})")
         print(f"Total path length: {len(path)-1}")
         print(f"Total time taken: {total_time2} seconds")
         print(f"Nodes explored from openset: {node_count }")
         save_data_manhattan_noDiag(path, len(path)-1, total_time2, node_count)
    else:
         print("No path found")


    print("Starting search")
    start3 = time.time() # Start Timer
    path, node_count  = astar_euclidean(start_space, end_space, space, width, height)
    end3 =  time.time() # End Timer
    total_time3= end3 - start3
    print(total_time3)
    print("Ending search")


    if path:
        print("Path:")
        for node in path:
            print(f"({node.xval}, {node.yval})")
        print(f"Total path length: {len(path)-1}")
        print(f"Total time taken: {total_time3} seconds")
        print(f"Nodes explored from openset: {node_count }")
        save_data_euclidean_noDiag(path, len(path)-1, total_time3, node_count)
    else:
        print("No path found")


if __name__=="__main__":
    main()