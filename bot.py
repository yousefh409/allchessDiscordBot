import os
import random

import discord
from dotenv import load_dotenv
import requests
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')




awaiting = {} #Of the form {'discord_id': callback}
LICHESS_ENDPOINT = "https://lichess.org"

async def game(message):
    contents = message.content.split()
    if len(contents) <= 2:
        response = "here is the game link young padawan: https://www.youtube.com/watch?v=ub82Xb1C8os"
        await message.channel.send(response)
    else:
        response = contents[2] + " , Do you accept the challenge <@" + str(message.author.id) + "> has made (Y/N)"
        await message.channel.send(response)
        responderId = contents[2][3:-1]
        awaiting[responderId] = lambda retMessage: getGameLink(retMessage)


async def ranking(message):
    contents = message.content.split()
    if len(contents) <= 2:
        response = "your rating is -399843729847239374. next time, use the right command young padawan"
        await message.channel.send(response)
    else:
        username = contents[2]
        lichess_response = requests.get(url= LICHESS_ENDPOINT + '/api/user/' + username +  '/rating-history')
        if lichess_response.status_code == 200:
            data = [x for x in lichess_response.json() if x["points"] != []]
            response = "Here are " + username + "'s stats, **organized in [year, month, day, rating], with month starting at 0(January)**: ```" + str(json.dumps(data, indent=4, sort_keys=True)) + "```"
        else:
            response = "sorry, we encountered an error with either lichess, or the username you inputted :("
        await message.channel.send(response)


commands = {
    'game' : game,
    'ranking': ranking
}


async def getGameLink(message):
    result = message.content.lower()
    confirmations = ['y', 'yes', 'sure', 'yup', 'yea', 'yessir']
    if result in confirmations:
        lichess_response = requests.post(url = LICHESS_ENDPOINT + "/api/challenge/open")
        if lichess_response.status_code == 200:
            game_link = lichess_response.json()["challenge"]["url"]
            response = "**n i c e**, here is a game link for your game. go **dominate** \n" + game_link
        else:
            response = "we encountered an error with lichess :("
    else:
        response = "guess there shall be no challenge :("
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
        response = "do you want something young padawan??????"
        await message.channel.send(response)

    elif contents[1] in commands:
        await commands[contents[1]](message)

    else:
        response = "i did not understand what you said. pick up a dictionary young padawan"
        await message.channel.send(response)


client.run(TOKEN)
