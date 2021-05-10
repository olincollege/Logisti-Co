# Logisti-Co.

Tower defense game focused on logistical management.

This is a tower defense game, similar to other games of this genre (Bloons Tower Defense or Plants vs. Zombies). Our setting is a factory which produces packages needing to be packed - your job is to create a robotic system which does this. Manage your economy and your robot placement to optimally deal with an increasing stream of packages without unpacked boxes from reaching the end of the path. See how long you can last!

## Website

[Click this link for our website!](https://sunsprint.github.io/Logisti-Co-Website/Home.html)

[Website repository link](https://github.com/Sunsprint/Logisti-Co-Website)

## Instructions for Use

1. Install the pygame library by running `pip install pygame` in a Terminal window.

2. Clone or download this repository into your desired directory.

3. Navigate to the directory in which you cloned the repository, and run the game using the terminal command `python run_game.py`

4. Place robot towers on the the game board by left-clicking on the screen, remove towers by right-clicking on them.

5. Packages should flow through the path and get periodically dealt with by the robots you placed. Use the in-game currency to place more robots.

6. End game by keyboard interrupt `ctrl+C` in the command line or by letting your lives run dry.

## Testing Instructions

1. Install the `pytest` and `pygame` libraries by using the command `pip install pytest pygame`

2. Clone or download this repository into your desired directory.

3. Navigate to the repository directory within the terminal window.

4. Run the command `pytest [FILENAME].py` to run a specific series of tests. Running the command `pytest *.py` to run all tests at once will not work as pytest will boot up our game rather than collecting all tests. The following is a list of all the test files you can run:
* test_game_model.py
* test_game_control.py


