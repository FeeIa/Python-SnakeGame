# Snake Game - CSC1004 Project 3
### Developed by 124040016 - Bryan Edelson

This is the third out of the three projects in **CSC1004** course of CUHK-SZ. There are three types of feature implemented:
- **Basic**: Features that are required by the course project details.
- **Advanced**: Features that are implemented for extra score.
- **Additional**: Features that are implemented for self-interest.

## Features
### Basic Features
- **Basic Snake Rule:** Snake continuously moves forward at a certain speed.
- **Interactable Snake**: Player can control the snake's direction.
- **Food**: Food items randomly appear on the arena. There are different types of food differentiated by color corresponding to different length increase.
- **Game End Conditions:** Game will end when the snake collides with the arena's boundaries or itself.
- **Python GUI (Tkinter)**: The visual elements of this game is built using Tkinter.
- **Game Over Message:** When the game ends, player will be able to see the snake's length, score, and elapsed time (in seconds).
- **Direct Keyboard Control**: Player can use WASD or arrow keys (up, down, left, right) to control the snake's direction.

### Advanced Features
- **Different Types of Food:** Food can now give different effects (not just length increase anymore). They are differentiated by their color. Each food types have different chance of spawning.
- **Obstacles**: Obstacles are now generated randomly starting from a certain level. The game ends upon collision with obstacles.
- **Multiple Levels**: There are 25 levels in total with different settings. You can only proceed to the next level by reaching previous levels' required score.
- **Gradual Velocity**: As time passes, the snake's velocity will increase exponentially.
- **Menu Screen**: There is now a menu screen where you can "Exit" or "Start". Upon clicking "Start", you will be redirected to choose which level to play.

### Additional Features
- **Respawning Food**: Unconsumed food will respawn after 5 seconds. This allows player to choose to avoid certain food types if needed.

## Tutorials
### Starting The Game
1. Upon running the program, click "Start" to be redirected to the level selection menu.
2. Choose which level to play. By default, only Level 1 is unlocked.
3. Beat the level to unlock the next level.

### Gameplay
1. You will spawn as a snake with varying lengths from level to level. There will be a small pause before the game starts for you to prepare.
2. One food will randomly spawn on the map. Each type of food has different effects.
3. Survive. Avoid colliding with the boundaries, yourself, or the obstacles.
4. Reach the specified score to advance to the next level.
5. Once you advanced to a new level, it will be unlocked for you. This means you can go back to the main menu and still access the level afterward.