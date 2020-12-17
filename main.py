import discord
import os
import random

client = discord.Client()

secretsanta = []

def add_user(user):
    if user not in secretsanta:
      secretsanta.append(user)
      return str(user.name) + " has been added to Santa's list!"
    else:
      return "Don't try to get multiple presents, you naughty kid!"


def del_user(user):
  message = "Santa doesn't have anybody with this name on his list."
  if secretsanta:
    if user in secretsanta:
      secretsanta.remove(user)
      message = "Seems like " + str(user.name) + " won't be getting any presents this year."
  return message


async def scramble_users():
  participants = secretsanta.copy()
  coresp_santas = secretsanta.copy()

  random.shuffle(coresp_santas)

  ok = True
  for i in range(0, len(participants)):
    if participants[i] == coresp_santas[i]:
      scramble_users()
      ok = False

  if ok:
    for i in range(0, len(participants)):
      await participants[i].send("You are Secret Santa for " + coresp_santas[i].name)
  secretsanta.clear()


async def participants(message):
  if secretsanta:
    await message.channel.send("This Secret Santa's Participants are: ")
    for p in secretsanta:
      await message.channel.send(p.name)
  else:
    await message.channel.send("There are no participants yet")


@client.event
async def on_ready():
  print("{0.user} is working!".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.lower().startswith('santa add me'):
    mess = add_user(message.author)
    await message.channel.send(mess)
  elif message.content.lower().startswith('santa add '):
    if message.mentions:
      user = message.mentions[0]
      mess = add_user(user)
    else:
      mess = "Please use the mention tag (@)"
    await message.channel.send(mess)

  if message.content.lower().startswith('santa del '):
    if message.mentions:
      user = message.mentions[0]
      mess = del_user(user)
    else:
      mess = "Please use the mention tag (@)"
    await message.channel.send(mess)

  if message.content.lower().startswith('santa shuffle'):
    await scramble_users()
    await message.channel.send("I've send all of you a private message!")

  if message.content.lower().startswith('santa list'):
    await participants(message)

  if message.content.lower().startswith('santa help'):
    await message.channel.send("Santa help:")
    await message.channel.send("Santa add me - Adds you to the list")
    await message.channel.send("Santa add @<Username> - Adds a participant to the list")
    await message.channel.send("Santa del @<Username> - Deletes a participant to the list")
    await message.channel.send("Santa list - Displays the list of participants")

  if message.content.lower().startswith('satan'):
    await message.channel.send("Satan is not available at this moment")

client.run(os.getenv('TOKEN'))
