# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 13:32:23 2019

@author: dschafer
"""

#%%

import random

#%%


def make_deck():
    """Makes set of dominoes for trains
    """
    deck = []
    for i in range(13):
        for j in range(13):
            if j >= i:
                deck.append([i, j])
            else:
                pass
    return deck


def draw_hands(n_players=1):
    """picks hands to play with. One for each player, plus a list of
    """
    if n_players > 6:
        assert "too many players. someone can't play."

    deck = make_deck()

    random.shuffle(deck)

    hands = []

    for i in range(n_players):
        hands.append(deck[15*i:15*(i+1)])

    bag = deck[n_players*15:]

    return hands, bag


def check_if_double(tile: list):
    """Checks if a tile is a double
    """
    return tile[0] == tile[1]


def pick_start_tile(hands: list):
    """ Takes set of player hands, checks who has the highest double and returns
        the starting player and starting tile number
    """
    doubles = {}


    # write down all the doubles
    for player, hand in enumerate(hands):
        for tile in hand:
            if check_if_double(tile):
                doubles[tile[0]] = player

    # find the highest double. If no doubles, return None for start_player and starting tile
    try:
        max_double = max(doubles.keys())
    except ValueError:
        return None, None

    start_player = doubles[max_double]

    return start_player, max_double


#%%

"""
Some starting thoughts:
    -   Brute force isn't an option...14! combinations.
    -   Obvious approach is to start at start tiles, then iterated down
        valid paths, relying on game rules to prune naturally.
    -   This feels dijkstra-y (find the longest path v the shortest). Should
        review how that works.
    -
    -   First check that I have ANY starting tiles
    -   Tiles for which one of the values is unique in the hand can only appear
        at the start or end of the sequence.  It might prove useful to pull
        those out and try tacking them onto the end.
    -   Flavor of this...make set of all tiles for whom both numbers have even
        numbers of entries.
        this ring
    -   Need to deal with double closures...
"""






def recursive_max_train(seq, remaining_tiles):
    """Recursively lengthens series and returns highest value leg
    """
    # find what I'm playing on.  This requires me to order the tiles correctly
    live_end = seq[-1][1]

    # get list of tile that can be played
    playable_tiles = []
    viable_legs = []

    for tile in remaining_tiles:
        if live_end in tile:
            playable_tiles.append(tile)

    # if there are no playable tiles, return incoming sequence
    if not playable_tiles:
        return seq

    # for each playable tile, find the longest/highest value train
    for tile in playable_tiles:
        # find remaining hand
        _my_hand = remaining_tiles.copy()
        _my_hand.remove(tile)

        # if tile is ordered backwards, switch it so I get the live end right
        _my_tile = tile

        if tile[0] == live_end:
            pass
        elif tile[1] == live_end:
            _my_tile.reverse()
        else:
            assert "Shouldn't get here"

        # RECURSION HERE. BE CAREFUL OF ORDER.
        viable_legs.append(recursive_max_train(seq + [_my_tile], _my_hand))

    # find length of longest viable leg
    max_leg_len = max([len(leg) for leg in viable_legs])

    # set max_leg_value so
    max_leg_val = 0

    for leg in viable_legs:
        if len(leg) == max_leg_len:
            # some multi-layer list comprehension voodoo
            leg_val = sum([pip for tile in leg for pip in tile])

            if leg_val > max_leg_val:
                # if this is more valuable
                max_leg_val = leg_val
                max_leg = leg

    return max_leg



# get list of viable start tiles
# for each start tile, look at remaining tiles and add one that matches
# if no viable tiles, return sequence and score

#%%


def test_failed_draw_case():
    """ quick test that I'm handling cases where no doubles are drawn in
    """
    hands = draw_hands(4)[0]
    start_tile = pick_start_tile(hands)


    # testing that I'm handling weird start players right
    fail_draws = 0
    good_draws = 0
    for i in range(10000):
        hands = draw_hands(4)[0]
        start_tile = pick_start_tile(hands)[0]
        if start_tile is None:
            fail_draws += 1
        else:
            good_draws += 1

    return fail_draws, good_draws
