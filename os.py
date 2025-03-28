
import random
import time
from dataclasses import dataclass
from typing import List, Optional

# Town Planning Configuration
MEMORY_TOWN_SIZE = 50  # How many lots are in our memory neighborhood
SIMULATION_DAYS = 15    # How many days to run our simulation

@dataclass
class MemoryHouse:
    """A house built by a process in our memory neighborhood"""
    address: int            # Where the house starts on Memory Street
    lots_occupied: int      # How many lots the house covers
    owner: str              # Which process family lives here (e.g., "Baker")
    move_in_day: int        # When the family moved in
    move_out_day: Optional[int] = None  # When they left (None if still living here)

class MemoryTown:
    """Manages our memory neighborhood and its houses"""
    
    def __init__(self, total_lots: int):
        self.total_lots = total_lots
        self.all_houses = []  # Records all houses ever built
        self.current_day = 0   # Tracks time in our simulation

    def build_house(self, needed_lots: int, family_name: str) -> bool:
        """A family tries to build a house on available lots"""
        if needed_lots > self.total_lots:
            print(f"Family {family_name} can't build - wants {needed_lots} lots but town only has {self.total_lots}!")
            return False

        # Sort houses by address to find empty spaces between them
        self.all_houses.sort(key=lambda house: house.address)
        next_empty_lot = 0  # Start looking from the beginning of town

        for house in self.all_houses:
            # Skip houses where families have moved out
            if house.move_out_day is not None:
                continue
                
            # Check for space before this house
            if next_empty_lot + needed_lots <= house.address:
                self._welcome_new_family(next_empty_lot, needed_lots, family_name)
                return True
                
            next_empty_lot = house.address + house.lots_occupied

        # Check if there's space at the end of town
        if next_empty_lot + needed_lots <= self.total_lots:
            self._welcome_new_family(next_empty_lot, needed_lots, family_name)
            return True

        print(f"Family {family_name} couldn't find {needed_lots} adjacent lots to build")
        return False

    def _welcome_new_family(self, address: int, lots: int, family: str) -> None:
        """Helper to create and record a new house"""
        new_house = MemoryHouse(
            address=address,
            lots_occupied=lots,
            owner=family,
            move_in_day=self.current_day
        )
        self.all_houses.append(new_house)
        print(f"Family {family} built a {lots}-lot house at address {address}")

    def family_moves_out(self, family_name: str) -> bool:
        """A process family leaves town, freeing their house"""
        found_family = False
        
        for house in self.all_houses:
            if house.owner == family_name and house.move_out_day is None:
                house.move_out_day = self.current_day
                found_family = True
                print(f"Family {family_name} moved out from {house.lots_occupied}-lot house at {house.address}")

        if not found_family:
            print(f"Family {family_name} doesn't have any active houses in town")
        return found_family

    def draw_town_map(self) -> None:
        """Create a visual map of current memory neighborhood"""
        # Start with all empty lots
        town_map = ['_'] * self.total_lots  

        # Mark occupied houses
        for house in self.all_houses:
            if house.move_out_day is None or house.move_out_day > self.current_day:
                for lot in range(house.address, house.address + house.lots_occupied):
                    town_map[lot] = house.owner[0]  # Use first letter of family name

        # Format the map into blocks of 10 lots
        map_rows = []
        for i in range(0, self.total_lots, 10):
            map_rows.append("".join(town_map[i:i+10]))

        # Print the town status
        print(f"\n Day {self.current_day} - Memory Neighborhood Map:")
        print("┌" + "──────────┬" * (len(map_rows)-1) + "──────────┐")
        for row in map_rows:
            print("│" + "│".join(f" {lot} " for lot in row) + "│")
        print("└" + "──────────┴" * (len(map_rows)-1) + "──────────┘")
        print(f"Key: _ = Empty lot, First letter = Family (e.g., 'B' for Baker)")
        print("═" * 60)  # Decorative separator

        self.current_day += 1

def run_town_simulation():
    """Run our memory neighborhood simulation"""
    memory_town = MemoryTown(MEMORY_TOWN_SIZE)
    family_names = ["Baker", "Taylor", "Miller", "Weaver", "Fisher"]
    
    print("\n Welcome to Memory Neighborhood Simulator!")
    print(f"Watching {MEMORY_TOWN_SIZE} memory lots over {SIMULATION_DAYS} days")
    print("Families will build houses and move out randomly\n")
    
    for day in range(SIMULATION_DAYS):
        print(f"\n Morning of Day {day + 1}:")
        
        # Random neighborhood activity
        activity = random.choices(
            ["build", "move_out", "quiet_day"],
            weights=[0.45, 0.45, 0.1],  # Most days have activity
            k=1
        )[0]

        if activity == "build":
            family = random.choice(family_names)
            lots_needed = random.randint(5, 10)  # Medium-sized houses
            memory_town.build_house(lots_needed, family)
        elif activity == "move_out":
            family = random.choice(family_names)
            memory_town.family_moves_out(family)

        # Show the town map at end of day
        memory_town.draw_town_map()
        time.sleep(1.5)  # Comfortable reading pace

if __name__ == "__main__":
    run_town_simulation()
    print("\nSimulation complete! Thanks for visiting Memory Neighborhood!")
