import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    # if len(state.my_fleets()) >= 1:
    #     return False
    
    current_destinations = [fleet.destination_planet for fleet in state.my_fleets()]
    untargeted_enemy_planets = [planet for planet in state.enemy_planets() if planet.ID not in current_destinations]    

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # find the weakest enemy planet without a fleet in flight
    weakest_planet = min(untargeted_enemy_planets, key=lambda t: t.num_ships, default=None)
    
    
    #weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def capture_best_neutral_planet(state):
    my_planets = state.my_planets()
    if not my_planets:
        return False

    current_destinations = [fleet.destination_planet for fleet in state.my_fleets()]
    untargeted_neutral_planets = [planet for planet in state.neutral_planets() if planet.ID not in current_destinations]
    if not untargeted_neutral_planets:
        return False

    best_planet = min(untargeted_neutral_planets, key=lambda p: (-p.growth_rate, min(state.distance(p.ID, my_p.ID) for my_p in my_planets), p.num_ships))
    strongest_planet = max(my_planets, key=lambda p: p.num_ships)

    # find the minimum ships to send
    ships = best_planet.num_ships + 1

    return issue_order(state, strongest_planet.ID, best_planet.ID, ships)