import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import http.client
import base64
import re

client = discord.Client()

token = open("./botToken", "r").read()

slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='the alliances'))

@client.event
async def on_message(ctx): 
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}: {ctx.content}")
    
@slash.slash(
    name="team",
    description="Retrieve information about any desired FTC team",
    guild_ids=[],
    options=[
        create_option(
                name="number",
                description="The team number of the desired team lookup",
                option_type=3,
                required="true"
        )
    ])
async def team(ctx: SlashContext, number: str):
    credentials = open("./ftcCredentials", "r").read()

    encoded = base64.urlsafe_b64encode(credentials.encode("utf-8"))
    encodedString = str(encoded, "utf-8")

    teamNumber = number

    conn = http.client.HTTPSConnection("ftc-api.firstinspires.org")
    headers = {
        'Authorization': 'Basic ' + encodedString,
    }
    conn.request("GET", "/v2.0/2021/teams?teamNumber=" + teamNumber + "&page=1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    teamInfo = data.decode("utf-8")

    parts = teamInfo.split(',')
    teamName = re.sub('"', '', parts[2]).split('nameShort:')
    teamCity = re.sub('"', '', parts[4]).split('city:')
    teamProv = re.sub('"', '', parts[5]).split('stateProv:')
    teamCount = re.sub('"', '', parts[6]).split('country:')
    teamWebsite = re.sub('"', '', parts[7]).split('website:')
    teamYear = re.sub('"', '', parts[8]).split('rookieYear:')

    await ctx.reply(f"Team {teamNumber} - {teamName[1]}\nLocation: {teamCity[1]}, {teamProv[1]}, {teamCount[1]}\nWebsite: {teamWebsite[1]}\nRookie year: {teamYear[1]}")

client.run(token)