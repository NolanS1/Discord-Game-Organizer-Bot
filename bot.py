import discord
import asyncio
from discord.ext import commands
from discord import Member
from discord.utils import get
import json
import psycopg2
import yaml


bot = commands.Bot(command_prefix='!')

credentials = yaml.load(open('./config.yml'))

#Shows some details regarding the bot
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----------------------')

@bot.command(pass_context = True, name="pug", aliases = ["l4d2game","PUG","lfd2game"])
@commands.cooldown(1, 60*10, commands.BucketType.default)
async def pug(ctx):
    time = "pug"
    teamname = "pug"
    conn = psycopg2.connect(credentials["PGURI"], sslmode='require')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scrim (id SERIAL PRIMARY KEY, team text,time text,people json)''')
    emptyJson = {"useridsplaying": [],"useridsnotplaying": []}
    c.execute("INSERT INTO scrim(team, time, people) VALUES (%s, %s, %s) RETURNING id",(teamname, time, json.dumps(emptyJson)))
    last_id = c.fetchone()[0]
    conn.commit()

    embed = discord.Embed(
            title = "Can you PUG?",
            description = "Respond to this message with ✅ if you can play.\nRespond to this message with ❌ if you can not play.",
            color = discord.Color.green() 
        )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Left4Dead2.jpg/220px-Left4Dead2.jpg")
    guild_id = ctx.guild.id
    try:
        c.execute("SELECT role FROM roleid WHERE guild = %s",(str(guild_id),))
        check = c.fetchall()
    except:
        check = ""

    if len(check) == 0:
        await ctx.send("NO ROLE SET ON THIS SERVER, USE !setroleid roleid EXAMPLE: !setroleid 734413050014203924, IN ORDER TO NOTIFY PLAYERS OF THE SCRIM")
    else:
        guild = bot.get_guild(guild_id)
        role = guild.get_role(int(check[0][0]))
        await ctx.send(role.mention)

    await ctx.send(embed=embed)

    embed2 = discord.Embed(
        description = "0/8 Players",
        color = discord.Color.green() 
    )
    embed2.add_field(name="✅ Playing", value="Waiting for responses", inline=False)
    embed2.add_field(name="❌ Not Playing", value="Waiting for responses", inline=False)
    embed2.set_footer(text=last_id)
    sentEmbed2 = await ctx.send(embed=embed2)
    await sentEmbed2.add_reaction(emoji='✅')
    await sentEmbed2.add_reaction(emoji='❌')

@bot.command(pass_context = True, name="csgo", aliases = ["csgogame","comp","competitive","cs"])
@commands.cooldown(1, 60*10, commands.BucketType.default)
async def csgo(ctx):
    time = "cs"
    teamname = "cs"
    conn = psycopg2.connect(credentials["PGURI"], sslmode='require')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scrim (id SERIAL PRIMARY KEY, team text,time text,people json)''')
    emptyJson = {"useridsplaying": [],"useridsnotplaying": []}
    c.execute("INSERT INTO scrim(team, time, people) VALUES (%s, %s, %s) RETURNING id",(teamname, time, json.dumps(emptyJson)))
    last_id = c.fetchone()[0]
    conn.commit()

    embed = discord.Embed(
            title = "CSGO?",
            description = "Respond to this message with ✅ if you can play.\nRespond to this message with ❌ if you can not play.",
            color = discord.Color.blue() 
        )
    embed.set_thumbnail(url="https://games.mxdwn.com/wp-content/uploads/2020/02/csgo-1.jpg")
    guild_id = ctx.guild.id
    
    guild = bot.get_guild(guild_id)
    role = guild.get_role(840751340280086580)
    await ctx.send(role.mention)

    await ctx.send(embed=embed)

    embed2 = discord.Embed(
        description = "0/5 Players",
        color = discord.Color.blue() 
    )
    embed2.add_field(name="✅ Playing", value="Waiting for responses", inline=False)
    embed2.add_field(name="❌ Not Playing", value="Waiting for responses", inline=False)
    embed2.set_footer(text=last_id)
    sentEmbed2 = await ctx.send(embed=embed2)
    await sentEmbed2.add_reaction(emoji='✅')
    await sentEmbed2.add_reaction(emoji='❌')

@bot.command(name="scrim")
async def scrim(ctx, teamname=None, *, time=None):
    conn = psycopg2.connect(credentials["PGURI"], sslmode='require')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scrim (id SERIAL PRIMARY KEY, team text,time text,people json)''')
    emptyJson = {"useridsplaying": [],"useridsnotplaying": []}
    if teamname == None and time == None:
        teamname = "scrim"
        time = "scrim"
        c.execute("INSERT INTO scrim(team, time, people) VALUES (%s, %s, %s) RETURNING id",(teamname, time, json.dumps(emptyJson)))
    else:
        c.execute("INSERT INTO scrim(team, time, people) VALUES (%s, %s, %s) RETURNING id",(teamname, time, json.dumps(emptyJson)))
    last_id = c.fetchone()[0]
    conn.commit()
    embed = discord.Embed(
            title = "Can you SCRIM?",
            description = "Respond to this message with ✅ if you can play.\nRespond to this message with ❌ if you can not play.",
            color = discord.Color.green() 
        )
    if teamname != "scrim" and time != "scrim":
        embed.add_field(name="Opponent:", value=teamname, inline=False)
        embed.add_field(name="When:", value=time, inline=False)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Left4Dead2.jpg/220px-Left4Dead2.jpg")
    guild_id = ctx.guild.id
    try:
        c.execute("SELECT role FROM roleid WHERE guild = %s",(str(guild_id),))
        check = c.fetchall()
    except:
        check = ""

    if len(check) == 0:
        await ctx.send("NO ROLE SET ON THIS SERVER, USE !setroleid roleid EXAMPLE: !setroleid 734413050014203924, IN ORDER TO NOTIFY PLAYERS OF THE SCRIM")
    else:
        guild = bot.get_guild(guild_id)
        role = guild.get_role(int(check[0][0]))
        await ctx.send(role.mention)

    await ctx.send(embed=embed)

    embed2 = discord.Embed(
        description = "0/4 Players",
        color = discord.Color.green() 
    )
    embed2.add_field(name="✅ Playing", value="Waiting for responses", inline=False)
    embed2.add_field(name="❌ Not Playing", value="Waiting for responses", inline=False)
    embed2.set_footer(text=last_id)
    sentEmbed2 = await ctx.send(embed=embed2)
    await sentEmbed2.add_reaction(emoji='✅')
    await sentEmbed2.add_reaction(emoji='❌')
@scrim.error
async def scrim_Error(ctx, error):
    embed = discord.Embed(
            title = "ERROR",
            color = discord.Color.red() 
        )
    embed.add_field(name="Example usage:",value="!scrim teamname time\nFOR EXAMPLE:\n!scrim frag4 10PM EST\n!scrim Evo In about 30 mins",inline=False)
    await ctx.send(embed=embed)

@bot.command(name="setroleid")
async def setRoleID(ctx, roleid):
    conn = psycopg2.connect(credentials["PGURI"], sslmode='require')
    guild = bot.get_guild(ctx.guild.id)
    if len(get(guild.roles, id=int(roleid)).name) > 0:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS roleid ( guild text, role text)''')
        c.execute("INSERT INTO roleid VALUES (%s, %s)",(ctx.guild.id,roleid))
        conn.commit()
        await ctx.send("✅ ROLEID UPDATED")
    else:
        await ctx.send("❌ ERROR ROLEID NOT UPDATED")
@setRoleID.error
async def setRoleID_Error(ctx, error):
    await ctx.send("❌ ERROR ROLEID NOT UPDATED")
    

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if payload.user_id != 734422687136481300 and message.author.id == 734422687136481300:
        conn = psycopg2.connect(credentials["PGURI"], sslmode='require')
        c = conn.cursor()
        if payload.emoji.name == '✅':
            c.execute("SELECT people FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
            peopleGrab = c.fetchall()
            peopleGrab = eval(str(peopleGrab[0][0]))
            if payload.user_id not in peopleGrab["useridsplaying"] and payload.user_id not in peopleGrab["useridsnotplaying"]:
                peopleGrab["useridsplaying"].append(payload.user_id)
                c.execute("UPDATE scrim SET people = %s WHERE id = %s", (json.dumps(peopleGrab),int(message.embeds[0].footer.text)))     
                conn.commit()
                c.execute("SELECT time FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
                checkPug = c.fetchall()
                checkPug = checkPug[0][0]
                if checkPug == "pug":
                     embed = discord.Embed(
                        description = str(len(peopleGrab["useridsplaying"]))+"/8 Players Ready",
                        color = discord.Color.green() 
                    )
                elif checkPug == "cs":
                        embed = discord.Embed(
                        description = str(len(peopleGrab["useridsplaying"]))+"/5 Players Ready",
                        color = discord.Color.blue() 
                    )
                else:
                    embed = discord.Embed(
                            description = str(len(peopleGrab["useridsplaying"]))+"/4 Players Ready",
                            color = discord.Color.green() 
                    )
                if not peopleGrab["useridsplaying"]:
                    pv = "Waiting for responses"
                else:
                    pv = ""
                    for uid in peopleGrab["useridsplaying"]:
                        ply = await bot.fetch_user(uid)
                        pv += "▫ "+ply.mention+"\n"
                
                if not peopleGrab["useridsnotplaying"]:
                    npv = "Waiting for responses"
                else:
                    npv = ""
                    for uid in peopleGrab["useridsnotplaying"]:
                        ply = await bot.fetch_user(uid)
                        npv += "▫ "+ply.mention+"\n"
               
                if checkPug == "pug" and len(peopleGrab["useridsplaying"]) == 8:
                    mens = ""
                    for uid in peopleGrab["useridsplaying"]:
                        ply = await bot.fetch_user(uid)
                        mens += ply.mention+"\n"
                    embed.add_field(name="✅ PUG READY", value= mens,inline=False)
                    embed.set_author(name="POST IP BELOW")
                elif checkPug == "cs" and len(peopleGrab["useridsplaying"]) == 5:
                    mens = ""
                    for uid in peopleGrab["useridsplaying"]:
                        ply = await bot.fetch_user(uid)
                        mens += ply.mention+"\n"
                    embed.add_field(name="✅ CSGO GAME READY", value= mens,inline=False)
                else:
                    embed.add_field(name="✅ Playing", value=pv, inline=False)
                    embed.add_field(name="❌ Not Playing", value=npv, inline=False)
                
                embed.set_footer(text=str(message.embeds[0].footer.text))
                await message.edit(embed=embed)
        elif payload.emoji.name == '❌':
            c.execute("SELECT people FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
            peopleGrab = c.fetchall()
            peopleGrab = eval(str(peopleGrab[0][0]))
            if payload.user_id not in peopleGrab["useridsplaying"] and payload.user_id not in peopleGrab["useridsnotplaying"]:
                peopleGrab["useridsnotplaying"].append(payload.user_id)
                c.execute("UPDATE scrim SET people = %s WHERE id = %s",(json.dumps(peopleGrab),int(message.embeds[0].footer.text)))
                conn.commit()
                c.execute("SELECT time FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
                checkPug = c.fetchall()
                checkPug = checkPug[0][0]
                if checkPug == "pug":
                     embed = discord.Embed(
                        description = str(len(peopleGrab["useridsplaying"]))+"/8 Players Ready",
                        color = discord.Color.green() 
                    )
                elif checkPug == "cs":
                    embed = discord.Embed(
                    description = str(len(peopleGrab["useridsplaying"]))+"/5 Players Ready",
                    color = discord.Color.blue() 
                    )   
                else:
                    embed = discord.Embed(
                            description = str(len(peopleGrab["useridsplaying"]))+"/4 Players Ready",
                            color = discord.Color.green() 
                    )
                if not peopleGrab["useridsplaying"]:
                    pv = "Waiting for responses"
                else:
                    pv = ""
                    for uid in peopleGrab["useridsplaying"]:
                        ply = await bot.fetch_user(uid)
                        pv += "▫ "+ply.mention+"\n"
                
                if not peopleGrab["useridsnotplaying"]:
                    npv = "Waiting for responses"
                else:
                    npv = ""
                    for uid in peopleGrab["useridsnotplaying"]:
                        ply = await bot.fetch_user(uid)
                        npv += "▫ "+ply.mention+"\n"
                
                embed.add_field(name="✅ Playing", value=pv, inline=False)
                embed.add_field(name="❌ Not Playing", value=npv, inline=False)
                embed.set_footer(text=str(message.embeds[0].footer.text))
                await message.edit(embed=embed)

@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if payload.user_id != 734422687136481300 and message.author.id == 734422687136481300:
        conn = psycopg2.connect(credentials["PGURI"], sslmode='require')
        c = conn.cursor()
        if payload.emoji.name == '✅':
            c.execute("SELECT people FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
            peopleGrab = c.fetchall()
            peopleGrab = eval(str(peopleGrab[0][0]))
            if payload.user_id in peopleGrab["useridsplaying"] and payload.user_id not in peopleGrab["useridsnotplaying"]:
                peopleGrab["useridsplaying"].remove(payload.user_id)
                c.execute("UPDATE scrim SET people = %s WHERE id = %s", (json.dumps(peopleGrab),int(message.embeds[0].footer.text)))     
                conn.commit()
                c.execute("SELECT time FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
                checkPug = c.fetchall()
                checkPug = checkPug[0][0]
                if checkPug == "pug":
                     embed = discord.Embed(
                        description = str(len(peopleGrab["useridsplaying"]))+"/8 Players Ready",
                        color = discord.Color.green() 
                    )
                elif checkPug == "cs":
                      embed = discord.Embed(
                        description = str(len(peopleGrab["useridsplaying"]))+"/5 Players Ready",
                        color = discord.Color.blue() 
                    )
                else:
                    embed = discord.Embed(
                            description = str(len(peopleGrab["useridsplaying"]))+"/4 Players Ready",
                            color = discord.Color.green() 
                    )
                if not peopleGrab["useridsplaying"]:
                    pv = "Waiting for responses"
                else:
                    pv = ""
                    for uid in peopleGrab["useridsplaying"]:
                        ply = await bot.fetch_user(uid)
                        pv += "▫ "+ply.mention+"\n"
                
                if not peopleGrab["useridsnotplaying"]:
                    npv = "Waiting for responses"
                else:
                    npv = ""
                    for uid in peopleGrab["useridsnotplaying"]:
                        ply = await bot.fetch_user(uid)
                        npv += "▫ "+ply.mention+"\n"
                
                embed.add_field(name="✅ Playing", value=pv, inline=False)
                embed.add_field(name="❌ Not Playing", value=npv, inline=False)
                embed.set_footer(text=str(message.embeds[0].footer.text))
                await message.edit(embed=embed)
        elif payload.emoji.name == '❌':
            c.execute("SELECT people FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
            peopleGrab = c.fetchall()
            peopleGrab = eval(str(peopleGrab[0][0]))
            if payload.user_id not in peopleGrab["useridsplaying"] and payload.user_id in peopleGrab["useridsnotplaying"]:
                peopleGrab["useridsnotplaying"].remove(payload.user_id)
                c.execute("UPDATE scrim SET people = %s WHERE id = %s",(json.dumps(peopleGrab),int(message.embeds[0].footer.text)))
                conn.commit()
                c.execute("SELECT time FROM scrim WHERE id = %s", (int(message.embeds[0].footer.text),))
                checkPug = c.fetchall()
                checkPug = checkPug[0][0]
                if checkPug == "pug":
                     embed = discord.Embed(
                        description = str(len(peopleGrab["useridsplaying"]))+"/8 Players Ready",
                        color = discord.Color.green() 
                    )
                elif checkPug == "cs":
                    embed = discord.Embed(
                        description = str(len(peopleGrab["useridsplaying"]))+"/5 Players Ready",
                        color = discord.Color.blue() 
                    )  
                else:
                    embed = discord.Embed(
                            description = str(len(peopleGrab["useridsplaying"]))+"/4 Players Ready",
                            color = discord.Color.green() 
                    )
                if not peopleGrab["useridsplaying"]:
                    pv = "Waiting for responses"
                else:
                    pv = ""
                    for uid in peopleGrab["useridsplaying"]:
                        ply = await bot.fetch_user(uid)
                        pv += "▫ "+ply.mention+"\n"
                
                if not peopleGrab["useridsnotplaying"]:
                    npv = "Waiting for responses"
                else:
                    npv = ""
                    for uid in peopleGrab["useridsnotplaying"]:
                        ply = await bot.fetch_user(uid)
                        npv += "▫ "+ply.mention+"\n"
                
                embed.add_field(name="✅ Playing", value=pv, inline=False)
                embed.add_field(name="❌ Not Playing", value=npv, inline=False)
                embed.set_footer(text=str(message.embeds[0].footer.text))
                await message.edit(embed=embed)


bot.run(credentials["TOKEN"])