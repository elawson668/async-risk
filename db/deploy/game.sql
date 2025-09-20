-- Deploy async-risk:game to pg

BEGIN;

-- XXX Add DDLs here.

-- Player
    -- card 1-5, can be null. check if all 5 are populated, if so prompt that they must turn in
        -- foreign key to card table? or just text?
        -- one field for each card, can be null. Foreign key to a card value
    -- turn stage tracker, reinforce, attack, fortify, not your turn
    -- country count (for tracking elimination)

-- Card
   -- symbol (match 3 to get bonus)
   -- country (if turning in the card, and you have that country, get 2 bonus troops for that country)
   -- flag for if owned by a player

-- Card stack
   -- how to simulate shuffling? Re-use?

-- Continent
   -- user id, can be null. shows if anyone controls the continent

-- Country
    -- continent id
    -- user id, can't be null except at beginning
    -- troop count
    -- adjacent countries

-- Game
    -- phase (setup, play)
    -- current card bonus
    -- user id, tracks whose turn it is

-- Attack
    -- attacker id
    -- defender id
    -- country id
    -- dice count for attacker
    -- dice count for defender
    -- outcome?


-- Setup phase
-- calculate initial infantry count from player count at beginning
-- dice roll to determine order
-- claim countries
-- place additional troops

-- Play phase
-- Reinforce
    -- Calculate reinforcements
    -- Prompt to turn in cards (optional or mandatory), increase reinforcement counts

-- Attack
    -- Allow 0-n attacks
        -- Note attacker, defender, country, etc in attack table
        -- Prompt for how many troops to attack with, defend with
            -- How to prompt defender for how many units to defend with?
        -- Simulate dice roll, calculate result, decrease troops accordingly
        -- If country captured, award one card, do not prompt for turn in if max is reached
        -- Prompt to move troops to captured country, must be at least the number of dice you rolled with
        -- If defender is eliminated, attacker receives their cards, prompt for another turn in if max is reached
    -- Attacker can end attack stage at any time

-- Fortify
    -- Move 0-n troops from one connected country to another. How to calculate? Tree?
    -- Must leave at least 1 behind
    -- Can skip this stage if wanted, either way turn automatically ends

-- Go through turns, when all but one players are eliminated, and remaining player has all countries, they win

COMMIT;
