# 2D Shooting Game
A top view 2D shooting game created using Python's Pygame Library.

## Overview
* player controls a character that appears at the center of the screen.
* player can move in four directions, controlled by using WSAD keys.
* player can aim and shoot by using mouse
* player can choose different weapons from armory system, at beginning, player has a default hand gun
* enemies (alien creatures) spawn at edges of the screen, and they will hunt the player down
* player will lose if taking enough damage from enemy. Player's score will be shown
* if player shoots all enemies, a new wave of enemy will respawn. Enemies are harder to kill and moves faster

## Implementation detail
### Basic movement of player
Implement the movement of the character (controlled by arrow key), and the orientation of the character (always facing the where mouse is, it is also the shooting direction)

### Game object animation
When moving the object, they should display animations rather than static, for example, the character should look like moving its legs when moving on the screen. Also, if an enemy is killed by the player, an animation should be shown.

### Character and NPC design
Design the attributes and methods of character and NPC classes.

### Other game object design 
weapons, warheads and bullets classes.

### interactions between projectiles and target being hit
This is the one of the core parts, since it defines how shooting/fighting behaves in this game. 

### Game resources
Game resources, including images, sounds, etc.

## Current Progress:
* Background has been set to a desert image
* player holding a pistol has been added
* control of player by WASD keys added 
* rotate and aim by mouse has been added
* sound effect added (foot steps and pistol shoot)

## Plan
* add bullet
* add enemy & enemy health bar
* kill enemy by bullet 
* add player health bar
* enemy can harm player by melee or ranged attack
* utilize a database to design a player profile and achievement system 
* design game menu (example: setting, create user profile, change user profile, view achievements, etc)

## How to run this demo 
Download the 2D_shooting_game folder, create your project. Activate your environment and install pygame package (pip install pygame). Then run '2D_shooting_game.py'
