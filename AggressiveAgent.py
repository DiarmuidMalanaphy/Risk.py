from typing import List, Tuple

import numpy as np
from Agent import Player
import random
from enum import Enum



ADJACENCY_ARRAY = np.array([
    [],  # Empty list for territory ID 0 (assuming territory IDs start from 1)
    [43, 3, 5, 4],
    [],  # Empty list for territory ID 2
    [14, 6, 5, 1],
    [43, 1, 5, 7],
    [1, 3, 6, 7, 8, 4],
    [3, 5, 8],
    [8, 5, 4, 9],
    [5, 6, 7, 9],
    [7, 8, 10],
    [9, 11, 12],
    [10, 12, 13, 21],
    [10, 11, 13],
    [11, 12],
    [3, 15, 16],
    [14, 16, 17, 20],
    [14, 15, 17, 18],
    [16, 15, 20, 19, 18],
    [16, 17, 19, 21],
    [17, 18, 20, 21, 22, 35],
    [15, 17, 19, 27, 31, 35],
    [18, 19, 22, 23, 24, 11],
    [19, 21, 35, 23],
    [21, 22, 35, 24, 25, 26],
    [21, 23, 25],
    [24, 23, 26],
    [23, 25],
    [20, 31, 37, 28],
    [27, 37, 33, 32, 29],
    [28, 32, 30],
    [29, 32, 34, 43],
    [27, 37, 36, 35, 20],
    [29, 30, 34, 33, 28],
    [28, 32, 34, 37],
    [33, 32, 30],
    [31, 36, 22, 23, 19, 20],
    [35, 38, 37, 31],
    [38, 36, 33, 31, 27, 28],
    [37, 36, 39],
    [40, 41, 38],
    [39, 41, 42],
    [39, 42, 40],
    [41, 40],
    [30, 1, 4]
], dtype=object)


class AggressiveAgent(Player):

    def __init__(self, id: int, unassigned_units: int, weightings : dict[int]):
        self.positions_of_interest = {
            39: 1, # Indonesia
            9 : 1, # Central America
            10 : 0.75, # Venezuala
            3 : 0.75, # Greenland
            11 : 0.75, # Brazil
            21 : 0.75, # North Africa
            23 : 0.5, # East Africa
            22 : 0.5, # Egypt
            43 : 0.5, # Alaska
            38 : 0.25, # Siam
            30 : 0.25, # Kamchatka
        }
        self.attack_heuristic_weightings = {
            1: 1, # Point of interest
            2: 1, # If the territory is able to attack and gain the entire continent.
            3: 1, # If it places you below max troops
            4: 1, # Gives increased reinforcements  ( increasing from 13 territories to 14)
            5: 1, # If you're able to find a chain of attacks
            6: 1, # If the territory attack is able to decrease the number of borders.
            7: 1, # If the opponent is winning
            8: 1, # Troop differential
            9: 1, # If it exposes you to chaining
            10: 7, # Heuristic threshold
            
            
        }

        super().__init__(id, unassigned_units)

    def make_selection(self, available_territories: List['Territory']) -> 'Territory':
        class Continent(Enum):
            NORTH_AMERICA = 1
            SOUTH_AMERICA = 2
            EUROPE = 3
            AFRICA = 4
            ASIA = 5
            AUSTRALIA = 6
        choice = random.choice(available_territories)
        #print(choice.name)
        #print(choice.id)
        #print(choice.continent)
        # Get available territories in each continent
        # Initialize empty array to store territories
        continents = []
        for i in range(6):
            continents.append([])
        # Store each territory in respective array corresponding to a continent
        for t in available_territories:
            continents[t.continent.value-1].append(t)

        # Create arbitrary ranks of continents
        if len(continents[Continent.NORTH_AMERICA.value-1]) > 0:
            choice = random.choice(continents[Continent.NORTH_AMERICA.value-1])
        elif len(continents[Continent.SOUTH_AMERICA.value-1]) > 0:
            choice = random.choice(continents[Continent.SOUTH_AMERICA.value-1])
        elif len(continents[Continent.AUSTRALIA.value-1]) > 0:
            choice = random.choice(continents[Continent.AUSTRALIA.value-1])
        elif len(continents[Continent.AFRICA.value-1]) > 0:
            choice = random.choice(continents[Continent.AFRICA.value-1])
        elif len(continents[Continent.EUROPE.value-1]) > 0:
            choice = random.choice(continents[Continent.EUROPE.value-1])
        elif len(continents[Continent.ASIA.value-1]) > 0:
            choice = random.choice(continents[Continent.ASIA.value-1])

        # Min / max fraction

        # input("Enter to continue")
        return choice

    def add_infantry(self) -> 'Territory':
        if not self.personal_territories:
            return None
        territory = random.choice(list(self.personal_territories.values()))
        #print("Add infantry: " + territory.name)
        return territory

    def reinforce(self, total_reinforcements : int) -> List[Tuple['Territory', int]]:
        
        reinforcement_allocation = []

        if self.personal_territories:
            selected_territory_id = random.choice(list(self.personal_territories.keys()))
            selected_territory = self.personal_territories[selected_territory_id]
            reinforcement_allocation = [(selected_territory, total_reinforcements)]

        return reinforcement_allocation

    def invade(self, adjacent_territories: List[Tuple['Territory', List['Territory']]]) -> Tuple['Territory', 'Territory', int]:

        attacking_heuristics = self.generate_attacking_heuristic(adjacent_territories)
        #valid_attacks = []
        #for pair, heuristic in attacking_heuristics.items():
            
        #    if heuristic > self.attack_heuristic_weightings[10]:
                # valid_attacks.append(pair)

        #Not sure how to calculate the best number of units to send.
            


        

        max_troops_territory = max(self.personal_territories.values(), key=lambda t: t.troop_count)

        if max_troops_territory.troop_count <= 3:
            return None

        adjacent_enemy_territories = []
        for territory, adjacents in adjacent_territories:
            if territory == max_troops_territory:
                for adjacent in adjacents:
                    if adjacent.get_owner().id != self.id:
                        adjacent_enemy_territories.append(adjacent)

        if not adjacent_enemy_territories:
            return None

        min_troops_enemy_territory = min(adjacent_enemy_territories, key=lambda t: t.troop_count)
        troops_to_use = max_troops_territory.troop_count - 1

        return max_troops_territory, min_troops_enemy_territory, troops_to_use
    
    def generate_attacking_heuristic(self, adjacent_territories):
        # self.attack_heuristic_weightings = {
        #     1: 1, # Point of interest
        #     2: 1, # If the territory is able to attack and gain the entire continent.
        #     3: 1, # If it places you below max troops
        #     4: 1, # Gives increased reinforcements  ( increasing from 13 territories to 14)
        #     5: 1, # If you're able to find a chain of attacks
        #     6: 1, # If the territory attack is able to decrease the number of borders.
        #     7: 1, # If the opponent is winning
        #     8: 1, # Troop differential
        #     9: 1, # If it exposes you to chaining
        #     10: 7, # Heuristic threshold
            
            
        # }
        heuristic_values = {}
        gets_below_max = self.gets_below_max_troops()
        for source_territory, target_territory_list in adjacent_territories:
            if source_territory.troop_count > 2:
                for target_territory in target_territory_list:
                    target_ids = np.array([target.id for target in target_territory_list])
                    target_troop_counts = np.array([target.troop_count for target in target_territory_list])
                    heuristic_value = np.zeros(len(target_territory_list))

                    
                    #Weighting 1 -> Point of interest
                    if target_territory.id in self.positions_of_interest:
                        heuristic_value += self.positions_of_interest[target_territory.id] * self.attack_heuristic_weightings[1]

                    #Weighting 2 -> Gaining continent
                    gain_continent_mask, continent_values = np.array([self.can_gain_continent(source_territory, target) for target in target_territory_list]).T
                    heuristic_value[gain_continent_mask] += continent_values[gain_continent_mask] * self.attack_heuristic_weightings[2]

                    #Weighting 3 -> Going below max
                    if gets_below_max:
                        heuristic_value += self.attack_heuristic_weightings[3]

                    #Weighting 4 -> Gives increased reinforcements
                    current_amount = len(self.personal_territories)
                    if (current_amount + 1 % 3 == 0 and current_amount > 9):
                        heuristic_value += self.attack_heuristic_weightings[4]

                    #Weighting 5 -> If you can chain attacks
                    chained_territories = ADJACENCY_ARRAY[target_territory.id]
                    for t in chained_territories:
                        if t not in self.personal_territories:
                            heuristic_value += self.attack_heuristic_weightings[5]
                
                    #Weighting 6 -> If you're able to decrease border size
                    current_borders = ADJACENCY_ARRAY[source_territory.id]
                    next_borders = ADJACENCY_ARRAY[target_territory.id]
                    if len(next_borders) < len(current_borders):
                        heuristic_value += self.attack_heuristic_weightings[6]

                    #Weighting 7 -> If the enemy is winning
                    enemy_territories = len(target_territory.owner.personal_territories)
                    if (len(self.personal_territories) < enemy_territories):
                        heuristic_value += self.attack_heuristic_weightings[7]
                    

                    #Weighting 8 -> Troop differential
                    current_troops = source_territory.troop_count
                    enemy_troops = target_territory.troop_count
                    heuristic_value += (current_troops - enemy_troops) * self.attack_heuristic_weightings[8]

                    #Returning the heuristics

                    for i, target_territory in enumerate(target_territory_list):
                        heuristic_values[(source_territory, target_territory)] = heuristic_value[i]
                        
        for  heuristic_value in heuristic_values.values():
            print(heuristic_value)
        return(heuristic_values)

    
    def is_point_of_interest(self) -> bool:
        # Returns if targetted territority is a point of interest and the respective weighting
        return False
    
    def can_gain_continent(self, source_territory : 'Territory', target_territory : 'Territory') -> Tuple[bool,float]:
        # Returns if it can conquer a continent on the turn and the value of the continent
        return (False, 0)
    
    def gets_below_max_troops(self) -> bool:
        # Returns if an attack will take us below the max unassigned values (i.e attack if we're full)
        return False
    
    def gives_increased_reinforcements(self) -> bool:
        # Returns if taking this territory will give us increased reinforcements next round
        return False
        
    def can_chain_attack(self) -> bool:
        # Returns if attacking this territory will allow us to attack another adjacent territory
        return False

    def reduces_border_count(self) -> Tuple[bool, float]:
        # Returns if taking this territory will reduce the number of outside borders all our terrorities have
        return False
    
    def attacks_winning_enemy(self) -> bool:
        # Returns if an attack is attacking a territory belonging to the winning team
        return False
    
    def difference_between_troops(self) -> float:
        # Returns the difference between your attacking troops and defending troops of territory being targetted
        return 0

        
 
            


    def manoeuvre(self, manoeuverable_territories: List[Tuple['Territory', List['Territory']]]) -> Tuple['Territory', 'Territory', int]:
        # Filter out territories that don't have enough troops to manoeuvre
        valid_manoeuverable_territories = [
            (source, targets) for source, targets in manoeuverable_territories
            if source.troop_count > 1 and targets
        ]

        if not valid_manoeuverable_territories:
            return None, None, 0  # Indicating no valid manoeuvre available

        # Pick a random source territory and its list of reachable territories
        source_territory, reachable_territories = random.choice(valid_manoeuverable_territories)

        # Pick a random destination territory from the reachable territories
        destination_territory = random.choice(reachable_territories)

        # Decide to move a random number of troops (up to the number of troops in the source territory - 1)
        num_troops = random.randint(1, source_territory.troop_count - 1)

        return source_territory, destination_territory, num_troops

    def get_player_name(self):
        return (f"Aggressive Agent {self.id}")
