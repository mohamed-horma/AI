# ENSICAEN - École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE123

# @file agents.py
# @author Régis Clouard

import random
import copy
from collections import deque
from utils import PriorityQueue


DIRECTIONTABLE = [(0, -1), (1, 0), (0, 1), (-1, 0)] # North, East, South, West

class TortoiseBrain:
    """
    The base class for various flavors of the tortoise brain.
    This an implementation of the Strategy design pattern.
    """
    def think( self, sensor ):
        raise Exception("Invalid Brain class, think() not implemented")

class RandomBrain( TortoiseBrain ):
    """
    An example of simple tortoise brain: acts randomly...
    """
    def init( self, grid_size ):
        pass

    def think( self, sensor ):
        return random.choice(['eat', 'drink', 'left', 'right', 'forward', 'forward', 'wait'])

class ReflexBrain( TortoiseBrain ):
    def init( self, grid_size ):
        pass

    def think( self, sensor ):
        # case 1: danger: dog
        if abs(sensor.dog_front) < 3 and abs(sensor.dog_right) < 3:
            if sensor.dog_front <= 0:
                if sensor.free_ahead:
                    return 'forward';
                elif sensor.dog_right > 0:
                    return 'left'
                else:
                    return 'right'
            elif sensor.dog_front > 0:
                if sensor.dog_right > 0:
                    return 'left';
                else:
                    return 'right'
        # increase the performance measure
        if sensor.lettuce_here and sensor.drink_level > 10: return 'eat'
        if sensor.water_ahead and sensor.drink_level < 50: return 'forward'
        if sensor.water_here and sensor.drink_level < 100: return 'drink'
        # Nothing to do: move
        if sensor.free_ahead:
            return random.choice(['forward', 'right', 'forward', 'wait', 'forward', 'forward', 'forward'])
        else:
            return random.choice(['right', 'left'])
        return random.choice(['eat', 'drink', 'left', 'right', 'forward', 'forward', 'wait'])

#  ______                               _              
# |  ____|                             (_)             
# | |__    __  __   ___   _ __    ___   _   ___    ___ 
# |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \
# | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/
# |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|

# Character representation of environement elements 
WALL = 'X'
GROUND = '.'
UNKNOWN = '?'
LETTUCE = 'l'
POUND = 'p'
STONE = 's'
FREE = 'f'

class GameState():
    """ 
    This class is provided as an aid, but it is not required.
    You can modify it or even replace it with your own class.
    """

    def __init__(self, grid_size =0): 
        if grid_size > 0:
            self.size = grid_size
            self.worldmap = [ [  ((y in [0, self.size - 1] or  x in [0, self.size - 1]) and WALL) or UNKNOWN
                                 for x in range(self.size) ] for y in range(self.size) ]
    def __deepcopy__( self, memo ):
        state = GameState()
        state.size = self.size
        state.worldmap = copy.deepcopy(self.worldmap, memo)
        state.size = self.size
        state.x = self.x
        state.y = self.y
        state.direction = self.direction
        state.drink_level = self.drink_level
        state.dogx = self.dogx
        state.dogy = self.dogy
        state.health_level = self.health_level
        return state

    def __eq__( self, other ):
        """ Used by the lists. """
        return self.x == other.x and self.y == other.y and self.direction == other.direction

    def __hash__(self):
        """ Used by the sets. """
        return hash((self.x, self.y, self.direction))

    def update_state_from_sensor( self, sensor ):
        """
        Updates the current environment from sensor information.
        """
        # Update the agent features
        self.drink_level = sensor.drink_level
        (self.x, self.y) = sensor.tortoise_position
        self.direction = sensor.tortoise_direction
        self.health_level = sensor.health_level

        # Update the map
        (directionx, directiony) = DIRECTIONTABLE[self.direction]
        if sensor.lettuce_here:
            self.worldmap[self.x][self.y] = LETTUCE
        elif sensor.water_here:
            self.worldmap[self.x][self.y] = POUND
        else:
            self.worldmap[self.x][self.y] = GROUND
        
        # Update ahead cell
        ahead_x = self.x + directionx
        ahead_y = self.y + directiony
        if 0 <= ahead_x < self.size and 0 <= ahead_y < self.size:
            if sensor.lettuce_ahead:
                self.worldmap[ahead_x][ahead_y] = LETTUCE
            elif sensor.water_ahead:
                self.worldmap[ahead_x][ahead_y] = POUND
            elif sensor.free_ahead:
                self.worldmap[ahead_x][ahead_y] = GROUND
            elif self.worldmap[ahead_x][ahead_y] == UNKNOWN:
                self.worldmap[ahead_x][ahead_y] = STONE

        # Update the dog position
        if directionx == 0:
            self.dogx = self.x - directiony * sensor.dog_right
            self.dogy = self.y + directiony * sensor.dog_front
        else:
            self.dogx = self.x + directionx * sensor.dog_front
            self.dogy = self.y + directionx * sensor.dog_right

    def get_current_cell( self ):
        return self.worldmap[self.x][self.y]

    def display( self ):
        """
        For debugging purpose.
        """
        print("Memory..")
        for y in range(self.size):
            for x in range(self.size):
                print(self.worldmap[x][y], end=" ")
            print()

class RationalBrain(TortoiseBrain):
    """
    Agent utilisant A* pathfinding avec optimisations ciblées.
    """
    
    def init(self, grid_size):
        self.state = GameState(grid_size)
        self.grid_size = grid_size
        
        # Connaissance du monde
        self.lettuce_positions = set()
        self.water_positions = set([(1, 1)])
        self.obstacle_positions = set()
        self.explored_cells = set()
        
        # A* pathfinding
        self.current_path = []
        self.current_target = None
        self.path_cache = {}
        
        # Suivi de performance
        self.visit_count = {}
        self.position_history = deque(maxlen=15)
        self.stuck_counter = 0
        self.last_action = None
        
        # Paramètres adaptatifs
        if grid_size <= 15:
            self.WATER_CRITICAL = 25
            self.WATER_LOW = 50
            self.A_STAR_LIMIT = 200
        elif grid_size <= 25:
            self.WATER_CRITICAL = 30
            self.WATER_LOW = 60
            self.A_STAR_LIMIT = 350
        else:
            self.WATER_CRITICAL = 35
            self.WATER_LOW = 70
            self.A_STAR_LIMIT = 500
        
        # Initialisation
        self.explored_cells.add((1, 1))
        self.visit_count[(1, 1)] = 1
    
    def think(self, sensor):
        """Main decision function."""
        self.state.update_state_from_sensor(sensor)
        current_pos = sensor.tortoise_position
        
        # Mise à jour de la connaissance
        self._update_knowledge(sensor)
        self.explored_cells.add(current_pos)
        self.position_history.append(current_pos)
        self.visit_count[current_pos] = self.visit_count.get(current_pos, 0) + 1
        
        # Détection de blocage
        if self._is_stuck():
            self.current_path = []
            self.stuck_counter += 1
        
        # PRIORITÉ 1: Actions urgentes (danger immédiat)
        urgent = self._check_urgent_actions(sensor)
        if urgent:
            self.current_path = []
            self.last_action = urgent
            return urgent
        
        # PRIORITÉ 2: Manger si sur laitue ET assez d'eau
        if sensor.lettuce_here and sensor.drink_level > 15:
            self.current_path = []
            self.lettuce_positions.discard(current_pos)
            self.last_action = 'eat'
            return 'eat'
        
        # PRIORITÉ 3: Boire si sur eau ET besoin
        if sensor.water_here and sensor.drink_level < 95:
            self.current_path = []
            self.last_action = 'drink'
            return 'drink'
        
        # Validation du chemin
        if self.current_path and not self._is_path_valid(sensor):
            self.current_path = []
        
        # Planification avec A* si nécessaire
        if not self.current_path:
            self._plan_with_astar(sensor)
        
        # Exécution du chemin
        if self.current_path:
            action = self.current_path.pop(0)
            self.last_action = action
            return action
        
        # Fallback: exploration sécurisée
        action = self._explore_safely(sensor)
        self.last_action = action
        return action
    
    def _plan_with_astar(self, sensor):
        """Planifie avec A*."""
        current_pos = sensor.tortoise_position
        current_dir = sensor.tortoise_direction
        
        # Choisir la meilleure cible
        target_type, target_pos = self._choose_best_target(sensor)
        
        if not target_pos:
            # Pas de cible : explorer
            explore_target = self._choose_exploration_target(current_pos, sensor)
            if explore_target:
                path = self._a_star_search(current_pos, current_dir, explore_target, sensor)
                if path:
                    self.current_path = path
                    self.current_target = explore_target
            return
        
        # Chercher un chemin vers la cible
        path = self._a_star_search(current_pos, current_dir, target_pos, sensor)
        
        if path:
            self.current_target = target_pos
            self.current_path = path
            # Ajouter l'action finale
            if target_type == 'lettuce':
                self.current_path.append('eat')
            elif target_type == 'water':
                self.current_path.append('drink')
        else:
            # Cible inaccessible : explorer
            explore_target = self._choose_exploration_target(current_pos, sensor)
            if explore_target:
                path = self._a_star_search(current_pos, current_dir, explore_target, sensor)
                if path:
                    self.current_path = path
                    self.current_target = explore_target
    
    def _a_star_search(self, start_pos, start_dir, goal_pos, sensor):
        """Algorithme A* utilisant PriorityQueue de utils.py."""
        if start_pos == goal_pos:
            return []

        

        # File de priorité
        open_list = PriorityQueue()
        open_list.push([(start_pos, start_dir, None)], 0)  # chemin initial: [(pos, dir, action)]
        
        # Meilleurs scores g pour chaque état
        g_scores = {(start_pos, start_dir): 0}
        closed_set = set()
        
        nodes_explored = 0
        
        while not open_list.isEmpty() and nodes_explored < self.A_STAR_LIMIT:
            # pop retourne (item, priority)
            current_path, priority = open_list.pop()
            current_pos, current_dir, _ = current_path[-1]
            g_score = priority - self._heuristic(current_pos, current_dir, goal_pos)

            # Si on atteint le but
            if current_pos == goal_pos:
                # Retourner uniquement les actions
                return [action for (_, _, action) in current_path[1:] if action is not None]

            state_key = (current_pos, current_dir)
            if state_key in closed_set:
                continue
            closed_set.add(state_key)
            nodes_explored += 1

            # Générer successeurs
            for action in ['forward', 'left', 'right']:
                new_pos, new_dir = self._apply_action(current_pos, current_dir, action)
                
                # Vérifier validité
                if not self._is_valid_cell(new_pos):
                    continue

                # Calcul du coût g
                action_cost = 2 if action == 'forward' else 1
                penalty = self._get_penalty(new_pos, sensor)
                tentative_g = g_score + action_cost + penalty

                new_state = (new_pos, new_dir)
                if new_state not in g_scores or tentative_g < g_scores[new_state]:
                    g_scores[new_state] = tentative_g
                    h = self._heuristic(new_pos, new_dir, goal_pos)
                    f = tentative_g + h

                    # Ajouter le nouveau chemin
                    new_path = current_path + [(new_pos, new_dir, action)]
                    open_list.push(new_path, f)
        
        return []

    
    def _get_penalty(self, pos, sensor):
        """Pénalités pour positions indésirables."""
        penalty = 0
        
        # Pénalité pour visites répétées
        visits = self.visit_count.get(pos, 0)
        penalty += visits * 2
        
        # Pénalité si près du chien
        if self._is_near_dog(pos, sensor):
            penalty += 20
        
        # Pénalité si bloqué récemment
        if self.stuck_counter > 0 and pos in list(self.position_history)[-5:]:
            penalty += 10
        
        return penalty
    
    def _heuristic(self, pos, direction, goal):
        """Heuristique pour A*."""
        # Distance Manhattan
        h = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        
        # Bonus léger si orienté vers le but
        dx = goal[0] - pos[0]
        dy = goal[1] - pos[1]
        
        if abs(dx) > abs(dy):
            ideal_dir = 1 if dx > 0 else 3
        else:
            ideal_dir = 2 if dy > 0 else 0
        
        if direction != ideal_dir:
            h += 0.5
        
        return h
    
    def _choose_best_target(self, sensor):
        """Choisit la meilleure cible."""
        current_pos = sensor.tortoise_position
        
        # EAU PRIORITAIRE si niveau bas
        if sensor.drink_level < self.WATER_LOW:
            best_water = self._find_nearest(current_pos, self.water_positions, sensor)
            if best_water:
                return 'water', best_water
        
        # LAITUE si eau suffisante
        if sensor.drink_level > 25 and self.lettuce_positions:
            best_lettuce = self._find_nearest(current_pos, self.lettuce_positions, sensor)
            if best_lettuce:
                # Vérifier qu'on peut y aller
                dist = self._manhattan_distance(current_pos, best_lettuce)
                if sensor.drink_level > dist + 20:
                    return 'lettuce', best_lettuce
        
        # EAU de maintenance
        if sensor.drink_level < 85 and self.water_positions:
            best_water = self._find_nearest(current_pos, self.water_positions, sensor)
            if best_water:
                return 'water', best_water
        
        return None, None
    
    def _find_nearest(self, from_pos, targets, sensor):
        """Trouve la cible la plus proche."""
        best = None
        best_score = float('inf')
        
        for target in targets:
            dist = self._manhattan_distance(from_pos, target)
            visits = self.visit_count.get(target, 0)
            score = dist * 3 + visits * 4
            
            if self._is_near_dog(target, sensor):
                score += 25
            
            if score < best_score:
                best_score = score
                best = target
        
        return best
    
    def _choose_exploration_target(self, current_pos, sensor):
        """Choisit une cible d'exploration."""
        best_cell = None
        best_score = -float('inf')
        
        radius = min(12, self.grid_size // 2)
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = current_pos[0] + dx
                y = current_pos[1] + dy
                
                if not (1 <= x < self.grid_size - 1 and 1 <= y < self.grid_size - 1):
                    continue
                
                pos = (x, y)
                
                if not self._is_valid_cell(pos):
                    continue
                
                score = 0
                
                # Bonus pour inexploré
                if pos not in self.explored_cells:
                    score += 80
                
                # Pénalité distance
                dist = abs(dx) + abs(dy)
                score -= dist * 2
                
                # Pénalité visites
                visits = self.visit_count.get(pos, 0)
                score -= visits * 8
                
                if score > best_score:
                    best_score = score
                    best_cell = pos
        
        return best_cell
    
    def _check_urgent_actions(self, sensor):
        """Actions urgentes."""
        # Eau critique
        if sensor.drink_level <= self.WATER_CRITICAL:
            if sensor.water_here:
                return 'drink'
            if sensor.water_ahead and sensor.free_ahead:
                return 'forward'
        
        # Danger chien
        dog_dist = abs(sensor.dog_front) + abs(sensor.dog_right)
        if dog_dist < 3:
            return self._escape_dog(sensor)
        
        return None
    
    def _escape_dog(self, sensor):
        """Fuir le chien."""
        # Si chien devant et chemin libre, avancer
        if abs(sensor.dog_front) <= 1 and sensor.free_ahead:
            return 'forward'
        
        # Tourner à l'opposé du chien
        if sensor.dog_right > 0:
            return 'left'
        elif sensor.dog_right < 0:
            return 'right'
        elif sensor.free_ahead:
            return 'forward'
        else:
            return 'right'
    
    def _is_path_valid(self, sensor):
        """Vérifie si le chemin est valide."""
        if not self.current_path:
            return False
        
        first = self.current_path[0]
        if first == 'forward' and not sensor.free_ahead:
            return False
        
        # Vérifier si la cible existe toujours
        if self.current_target and self.current_target not in self.lettuce_positions and self.current_target not in self.water_positions:
            if self._manhattan_distance(sensor.tortoise_position, self.current_target) > 1:
                return False
        
        return True
    
    def _is_stuck(self):
        """Détecte un blocage."""
        if len(self.position_history) < 10:
            return False
        
        # Si on visite les mêmes 2-3 positions en boucle
        recent = list(self.position_history)[-8:]
        unique = len(set(recent))
        
        return unique <= 2
    
    def _explore_safely(self, sensor):
        """Exploration sécurisée."""
        # Éviter de répéter la même action
        if sensor.free_ahead:
            if self.last_action == 'forward':
                return random.choice(['forward', 'forward', 'right'])
            return 'forward'
        else:
            if self.last_action == 'right':
                return 'left'
            return 'right'
    
    def _update_knowledge(self, sensor):
        """Met à jour la connaissance du monde."""
        pos = sensor.tortoise_position
        
        # Case actuelle
        if sensor.lettuce_here:
            self.lettuce_positions.add(pos)
        if sensor.water_here and pos != (1, 1):
            self.water_positions.add(pos)
        
        # Case devant
        dx, dy = DIRECTIONTABLE[sensor.tortoise_direction]
        ahead = (pos[0] + dx, pos[1] + dy)
        
        if self._is_in_bounds(ahead):
            if sensor.lettuce_ahead:
                self.lettuce_positions.add(ahead)
            if sensor.water_ahead and ahead != (1, 1):
                self.water_positions.add(ahead)
            if not sensor.free_ahead:
                self.obstacle_positions.add(ahead)
    
    def _is_valid_cell(self, pos):
        """Vérifie si une cellule est valide."""
        x, y = pos
        
        if x <= 0 or y <= 0 or x >= self.grid_size - 1 or y >= self.grid_size - 1:
            return False
        
        if pos in self.obstacle_positions:
            return False
        
        return True
    
    def _is_in_bounds(self, pos):
        """Vérifie les limites."""
        x, y = pos
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size
    
    def _is_near_dog(self, pos, sensor):
        """Vérifie proximité du chien."""
        if not hasattr(self.state, 'dogx') or not hasattr(self.state, 'dogy'):
            return False
        
        dog_pos = (self.state.dogx, self.state.dogy)
        distance = abs(pos[0] - dog_pos[0]) + abs(pos[1] - dog_pos[1])
        return distance <= 3
    
    def _apply_action(self, pos, direction, action):
        """Applique une action."""
        x, y = pos
        
        if action == 'forward':
            dx, dy = DIRECTIONTABLE[direction]
            return (x + dx, y + dy), direction
        elif action == 'left':
            return (x, y), (direction - 1) % 4
        elif action == 'right':
            return (x, y), (direction + 1) % 4
        
        return (x, y), direction
    
    def _manhattan_distance(self, pos1, pos2):
        """Distance Manhattan."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])