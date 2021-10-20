import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json
import random
import statcord


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
STATCORD_ID = os.getenv('STATCORD_ID')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')




awaiting = {} #Of the form {'discord_id': callback}
LICHESS_ENDPOINT = "https://lichess.org"
JOKE_ENDPOINT = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist"
FACT_ENDPOINT = "https://uselessfacts.jsph.pl/random.json?language=en"
TRAIN_IMAGE_ENDPOINT = "https://chesspuzzle.net/Images/Small/Puzzle"
TRAIN_ENDPOINT = "https://chesspuzzle.net/Puzzle/"
TRAIN_DAILY_ENDPOINT = "https://chesspuzzle.net/Daily/Api"
TRAIN_SOLUTION_ENDPOINT = "https://chesspuzzle.net/Solution/"


#################################### ANALYTICS ####################################
class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = STATCORD_ID
        self.api = statcord.Client(self.bot,self.key,custom1=self.custom1,custom2=self.custom2)
        self.api.start_loop()


    @commands.Cog.listener()
    async def on_command(self,ctx):
        self.api.command_run(ctx)

    async def custom1(self):
        # Do Things Here
        return "10" # Return a string.

    async def custom2(self):
        # Do Things Here
        return "10" # Return a string.

###################################################################################
async def game(message):
    contents = message.content.split()
    if len(contents) <= 2:
        response = "here is the game link young padawan: https://www.youtube.com/watch?v=ub82Xb1C8os"
        await message.channel.send(response)
    else:
        response = contents[2] + " , Do you accept the challenge <@" + str(message.author.id) + "> has made (Y/N)"
        await message.channel.send(response)
        responderId = contents[2][3:-1]
        awaiting[responderId] = lambda retMessage: get_game_link(retMessage, message)


async def ranking(message):
    contents = message.content.split()
    if len(contents) <= 2:
        response = "your rating is -399843729847239374. next time, use the right command young padawan"
        await message.channel.send(response)
    else:
        username = contents[2]
        success, lichess_response = make_request(f"/api/user/{username}/rating-history")
        if success:
            data = [x for x in lichess_response if x["points"] != []]
            response = "Here are " + username + "'s stats, **organized in [year, month, day, rating], with month starting at 0(January)**: ```" + str(json.dumps(data, indent=4, sort_keys=True)) + "```"
        else:
            response = "sorry, we encountered an error with either lichess, or the username you inputted :("
        await message.channel.send(response)


async def tournament(message):
    contents = message.content.split()
    await message.channel.send("This command is not yet supported.")


EMBED_COLOUR = 1932020
async def help(message):
    em = discord.Embed()
    em.title = "Help"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.add_field(name="Example Command", value="We reccomend you view example usage for each command using the \"!chess example\" command", inline=True)
    for key in helpInfo:
        em.add_field(name = key, value = helpInfo[key], inline=False)

    await message.channel.send(embed=em)


async def about(message):
    em = discord.Embed()
    em.title = "Help"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.add_field(name = "Creators", value ="yous#8647, sebitommy123#7816, and Chess Hobo#5674", inline=False)
    em.add_field(name="Help Command", value="View the commands that this bot supports: help", inline=True)
    em.add_field(name="Example Command", value="View example usage for each command: example", inline=True)
    em.add_field(name="Version", value="2.0.0", inline=True)
    em.add_field(name="Repository", value="https://github.com/yousefh409/allchessDiscordBot", inline=False)
    em.add_field(name="Invite", value="https://top.gg/bot/777276681517531187/invite/", inline=False)
    await message.channel.send(embed=em)

async def example(message):
    em = discord.Embed()
    em.title = "Example"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    for key in exampleInfo:
        em.add_field(name = key, value = exampleInfo[key], inline=False)

    await message.channel.send(embed=em)

async def code(message):
    em = discord.Embed()
    em.title = "Code"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.add_field(name = "Info", value ="We are an open-source project and would love for you to contribute", inline=False)
    em.add_field(name="Repository", value="https://github.com/yousefh409/allchessDiscordBot", inline=False)

    await message.channel.send(embed=em)


async def randomCommand(message):
    contents = message.content.split()
    if len(contents) < 3:
        rand_number = random.randint(0, 1000)
        response = f"here is a random number young padawan: **{rand_number}**"
        await message.channel.send(response)
    elif int(contents[2]) > 0:
        rand_number = random.randint(0, int(contents[2]))
        response = f"here is a random number young padawan: **{rand_number}**"
        await message.channel.send(response)
    else:
        response = f"do not try to fool me"
        await message.channel.send(response)


async def joke(message):
    success, lichess_response = make_request("", begin=JOKE_ENDPOINT)
    if success:
        if lichess_response["type"] == "single":
            joke = lichess_response["joke"]
        else:
            joke = lichess_response["setup"] + "\n" + lichess_response["delivery"]
        response = f"You asked for a joke, **you are getting one**: \n{joke}"
        await message.channel.send(response)
    else:
        response = "we encountered an error with the joke generator :("
        await message.channel.send(response)


async def fact(message):
    success, lichess_response = make_request("", begin=FACT_ENDPOINT)
    if success:
        fact = lichess_response["text"]
        response = f"You asked for a cool fact, **you are getting one** (yes it is true): \n {fact}"
        await message.channel.send(response)
    else:
        response = "we encountered an error with the fact generator :("
        await message.channel.send(response)


async def train(message):
    success, lichess_response = make_request("", begin=TRAIN_DAILY_ENDPOINT)
    puzzle_id = lichess_response["Puzzle"]
    image = TRAIN_IMAGE_ENDPOINT + f"{puzzle_id}.png"
    train = TRAIN_ENDPOINT + str(puzzle_id)
    solution = TRAIN_SOLUTION_ENDPOINT + str(puzzle_id)

    em = discord.Embed()
    em.title = f"Training Activity #{puzzle_id}"
    em.colour = discord.Colour(EMBED_COLOUR)
    em.type = "rich"
    em.set_image(url=image)
    em.add_field(name="Interactive", value=train, inline=False)
    em.add_field(name="Solution", value=solution, inline=False)
    await message.channel.send(embed=em)

async def num_serv(message):
    num_memb = 0
    for serv in client.guilds:
        num_memb += serv.member_count
    response = "I am in **" +  str(len(client.guilds))  + "** servers at the moment!\n"
    response += "This comes to a total of **" + str(num_memb) + "** people using All Chess!"

    await message.channel.send(response)

def make_request(endpoint, func=requests.get, begin=LICHESS_ENDPOINT, data={}):

    api_url =  begin + endpoint
    if func == requests.post:
        lichess_response = func(url=api_url, json=data)
    else:
        lichess_response = func(url=api_url)

    if lichess_response.status_code == 200:
        return True, lichess_response.json()

    return False, None


commands = {
    'game' : game,
    'play': game,
    'ranking': ranking,
    # 'tournament': tournament,
    'help': help,
    'about': about,
    'code': code,
    'random': randomCommand,
    'joke': joke,
    'fact': fact,
    'train': train,
    'num': num_serv,
    'example': example
}

helpInfo = {
    '!chess help': "Gets some info about the commands (hey, you are reading it now!)",
    '!chess example': "Give some example usage for each of the commands",
    '!chess game <player> <--time [time (minutes)]> <--increment [increment (seconds)]> <--variant [variant]>': "Challenges <player> to a lichess match. If any of the optional <--[command]> commands are specified, they will create a game with the specified settings.",
    '!chess ranking <username>': "Gets the ranking of <username> on lichess",
    '!chess train': "Get a training puzzle, that you can follow the links to solve",
    '!chess joke': "Get a random joke (very funny i assure you)",
    '!chess fact': "Get a random cool fact. yes, they are factual",
    '!chess random <(optional)upper>': "Get a random number up to <upper>, which defaults to 1000",
    '!chess about': "Tells you some stuff about the bot",
    '!chess code': "Gives the link to our open-source code, where you can contribute!"
}

exampleInfo = {
    'help': "!chess help \n - Provides you with a list of commands and what they do.",
    'example': "!chess example \n - Provides example usage for each command.",
    'game': "!chess game @yous --time 10 --increment 8 \n - Challenges @yous to a normal chess game with a time of 10 minutes, and an increment of 8 seconds.",
    'ranking': "!chess ranking yousefh409 \n - Gets the stats of yousefh409 on LiChess.",
    'train': "!chess train \n - Provides a cool training puzzle.",
    'joke': "!chess joke \n - Provides a funny joke.",
    'fact': "!chess fact \n - Provides a cool fact.",
    'random': "!chess random 1849429 \n - Gives a random number from 0 to 1849429.",
    'about': "!chess about \n - Gives some information about the bot.",
    'code': "!chess code \n - Gives some information about the software used in this bot."
}


async def get_game_link(message, orig_message):
    result = message.content.lower()
    confirmations = ['y', 'yes', 'sure', 'yup', 'yea', 'yessir']
    try:
        orig = orig_message.content.split()
        if result in confirmations:
            data = {"variant": "standard"}
            commands = ["--time", "--increment", "--variant"]
            if len(orig) > 3:
                if orig[3].lower() == "bullet":
                    data["clock"] = {'limit': 60, 'increment': 0}
                elif orig[3].lower() in commands:
                    for i in range(0, len(orig) - 3):
                        if orig[3 + i].lower() == "--time":
                            if "clock" in data and "increment" in data["clock"]:
                                data["clock"]["limit"] =  int(orig[4 + i]) * 60
                            else:
                                data["clock"] = {"limit": int(orig[4 + i]) * 60, "increment": 0}
                        elif orig[3 + i].lower() == "--increment":
                            if "clock" in data and "limit" in data["clock"]:
                                data["clock"]["increment"] =  int(orig[4 + i])
                            else:
                                data["clock"] = {"limit": 10800, "increment": int(orig[4 + i])}
                        elif orig[3 + i].lower() == "--variant":
                            data["variant"] = orig[4 + i].lower()
                else:
                    data["variant"] = orig[3].lower()
            success, lichess_response = make_request('/api/challenge/open', requests.post, data=data)
            if success:
                game_link = lichess_response["challenge"]["url"]
                response = "Nice, here is a game link for your game. Go **dominate** \n" + game_link
            else:
                response = "Sorry, we encountered an error with lichess :("
        else:
            response = "I guess there shall be no challenge :("
    except Exception as e:
        response = "Make sure to follow the command format correctly."
    await message.channel.send(response)


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    if str(message.author.id) in awaiting:
        await awaiting[str(message.author.id)](message)
        awaiting.pop(str(message.author.id))
        return

    contents = message.content.split()
    if len(contents) < 1:
        return

    elif contents[0] != "!chess":
        return

    if len(contents) <= 1:
        response = "Make sure to specify a command young padawan. Use \"!chess help\" to view some of these commands."
        await message.channel.send(response)

    elif contents[1] in commands:
        await commands[contents[1]](message)

    else:
        response = "I did not understand what you said, make sure you are using a command that I support."
        await message.channel.send(response)


def setup(bot):
    bot.run(TOKEN)
    bot.add_cog(StatcordPost(client))
    bot.change_presence(activity=discord.Game(name="!chess help"))

setup(client)