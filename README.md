# All Chess Discord Bot


# Description
This bot can be brought into a discord server, and instantly make practicing and playing chess much easier. It can quickly organize games on lichess, fetch user stats, and provide cool training examples.


# Commands
* `help` => Gets help(hey, you are reading it now!)
* `game <player> <--time [time (minutes)]> <--increment [increment (seconds)]> <--variant [variant]>` => Challenges <player> to a lichess match. If any of the <--[command]> commands are specified, they will create a game with the specified settings.
* `ranking <username>` => Gets the ranking of <username> on lichess
* `train` => Get a training puzzle, that you can follow the links to solve
* `joke` => Get a random joke(very funny i assure you)
* `fact` => Get a random cool fact. yes, they are factual
* `random <(optional)upper>` => Get a random number up to <upper>, which defaults to 1000
* `about` => Tells you some stuff about the bot
* `code` => Gives the link to our open-source code, where you can contribute

# Use On Local Devices
1. Create the appropriate stuff in the discord developers portal, and put the bot token in a `.env` file
2. Run `pip install -r requirements.txt` in the initial directory to install all required packages
3. Run `python bot.py` inside the `bots` folder to start the bot

    - To invite the bot to your discord server, go here: https://top.gg/bot/777276681517531187/invite/

# Helps or Questions
Please feel free to make a pull request, and maintainers will take a look at it swiftly. Please contact us if you have any questions!
