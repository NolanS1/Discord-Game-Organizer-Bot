

import os

from discord.ext import commands
import discord

from replit import db

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))
    
@bot.command(
    pass_context=True,
    name="pug",
    aliases=["l4d2game", "PUG", "lfd2game", "l4d2pug", "l4d2", "lfd2"])

#@commands.cooldown(1, 60 * 10, commands.BucketType.default)
async def pug(ctx):
  questionEmbed = discord.Embed(
      title="Pick up game?",
      description=
      "Respond with ✅ if you can play.\nRespond with ❌ if you are unable to play.",
      color=discord.Color.green())
  questionEmbed.set_thumbnail(
      url=
      "https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Left4Dead2.jpg/220px-Left4Dead2.jpg"
  )

  role = discord.utils.get(ctx.guild.roles, name="l4d2")

  await ctx.send(role.mention)
  await ctx.send(embed=questionEmbed)

  db['counter'] += 1
  reactionEmbed = await ctx.send(embed=create_embed())

  db['plyList'].insert(0, {
      "msgId": reactionEmbed.id,
      "plyList": [],
      "nplyList": []
  })

  if len(db['plyList']) > 3:
    db['plyList'].pop()

  #Send reactions to player info embed
  await reactionEmbed.add_reaction('✅')
  await reactionEmbed.add_reaction('❌')

@bot.event
async def on_raw_reaction_add(payload):
  if payload.member.bot == True:
    return
  index = get_message_index(payload)
  if index != -1:
    await edit_embed('✅', payload, index, "plyList")
    await edit_embed('❌', payload, index, "nplyList")

@bot.event
async def on_raw_reaction_remove(payload):
  index = get_message_index(payload)
  if index != -1:
    await edit_embed('✅', payload, index)
    await edit_embed('❌', payload, index, "nplyList")


async def edit_embed(emoji, payload, index=0, list="plyList"):
  if str(payload.emoji.name) != emoji:
    return

  channel = bot.get_channel(payload.channel_id)
  msg = await channel.fetch_message(payload.message_id)
  user = await bot.fetch_user(payload.user_id)

  if payload.event_type == 'REACTION_ADD' and
  (payload.member.mention not in db['plyList'][index]['plyList']
  and payload.member.mention not in db['plyList'][index]['nplyList']):
    db['plyList'][index][list].append(payload.member.mention)
  elif payload.event_type == 'REACTION_REMOVE' and user.mention in db[
      'plyList'][index][list]:
    db['plyList'][index][list].remove(user.mention)

  embed = create_embed(
      len(db['plyList'][index]['plyList']),
      "\n".join(ply for ply in db['plyList'][index]['plyList']),
      "\n".join(ply for ply in db['plyList'][index]['nplyList']))
  await msg.edit(embed=embed)

def create_embed(pNum=0,
                 pVal="Waiting for players",
                 npVal="Waiting for players"):
  plyInfoEmbed = discord.Embed(description=f"{pNum}/8 Players",
                               color=discord.Color.green())
  plyInfoEmbed.add_field(name="✅ Playing", value=pVal, inline=False)
  plyInfoEmbed.add_field(name="❌ Not Playing", value=npVal, inline=False)
  plyInfoEmbed.set_footer(text=f"{db['counter']}")

  return plyInfoEmbed


def get_message_index(payload):
  if payload.message_id == db['plyList'][0]['msgId']:
    return 0
  elif payload.message_id == db['plyList'][1]['msgId']:
    return 1
  elif payload.message_id == db['plyList'][2]['msgId']:
    return 2
  else:
    return -1


try:
  token = os.getenv("TOKEN") or ""
  bot.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
  else:
    raise e
