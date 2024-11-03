import discord
from discord.ext import commands
import random
import requests
import asyncio

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Define choices and winning combinations for RPS
choices = {"r": "Rock", "p": "Paper", "s": "Scissors"}
winning_combinations = {
    ("r", "s"): "Rock beats Scissors!",
    ("p", "r"): "Paper beats Rock!",
    ("s", "p"): "Scissors beats Paper!"
}

# List of allowed role IDs
allowed_role_ids = [
    1298340756112539706,  # Owner
    1298341985060524042,  # Admin
    1298342126609764412   # Moderator
]

def has_roles():
    def predicate(ctx):
        return any(role.id in allowed_role_ids for role in ctx.author.roles)
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command(name="cmds", help="Lists all available commands.")
async def cmds(ctx):
    commands_list = [
        "🔧 **!kick @user** - Kicks a specified user from the server.",
        "🔨 **!ban @user** - Bans a specified user from the server.",
        "🔇 **!mute @user [duration]** - Mutes a specified user for a duration.",
        "🔈 **!unmute @user** - Unmutes a specified user.",
        "⚠️ **!warn @user [reason]** - Issues a warning to a specified user.",
        "🗑️ **!clear [number]** - Deletes a specified number of messages.",
        "🗳️ **!poll [question] [option1] [option2]** - Creates a poll.",
        "🌤️ **!weather [location]** - Provides current weather for a location.",
        "😂 **!joke** - Tells a random joke.",
        "🎨 **!meme [query]** - Fetches a meme related to a query.",
        "👤 **!userinfo [@user]** - Shows info about a specified user.",
        "🏢 **!serverinfo [server_id]** - Displays information about the server.",
        "📚 **!fact** - Shares a random fun fact.",
        "✂️ **!rps @user** - Plays Rock-Paper-Scissors with another member.",
        "📊 **!ping** - Checks the bot's latency."
    ]

    embed = discord.Embed(
        title="✨ **Available Commands** ✨",
        description="\n".join(commands_list),
        color=discord.Color.blue()
    )
    embed.set_footer(text="Use the commands wisely! 🤖")
    await ctx.send(embed=embed)

@bot.command(name="kick", help="Kicks a specified user from the server.")
@has_roles()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(
        title="🚫 **User Kicked**",
        description=f"{member.mention} has been kicked from the server. 👋",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command(name="ban", help="Bans a specified user from the server.")
@has_roles()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title="🔨 **User Banned**",
        description=f"{member.mention} has been banned from the server. ❌",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command(name="mute", help="Mutes a specified user for a duration.")
@has_roles()
async def mute(ctx, member: discord.Member, duration: int):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False)
    
    await member.add_roles(role)
    embed = discord.Embed(
        title="🔇 **User Muted**",
        description=f"{member.mention} has been muted for {duration} seconds. 🤫",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)
    
    await asyncio.sleep(duration)
    await member.remove_roles(role)
    embed = discord.Embed(
        title="🔈 **User Unmuted**",
        description=f"{member.mention} has been unmuted! 🎉",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name="clear", help="Deletes a specified number of messages.")
@has_roles()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        title="🗑️ **Messages Cleared**",
        description=f"Deleted {amount} messages. ✨",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name="poll", help="Creates a poll with two options.")
async def poll(ctx, question: str, option1: str, option2: str):
    embed = discord.Embed(
        title="🗳️ **Poll**",
        description=f"**{question}**\n\nReact with:\n1️⃣ for {option1}\n2️⃣ for {option2}",
        color=discord.Color.green()
    )
    message = await ctx.send(embed=embed)
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')

@bot.command(name="joke", help="Tells a random joke.")
async def joke(ctx):
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
        "Why don’t scientists trust atoms? Because they make up everything! ⚛️",
        "What do you call fake spaghetti? An impasta! 🍝",
        "Why did the bicycle fall over? Because it was two-tired! 🚴‍♂️",
        "I told my wife she was drawing her eyebrows too high. She looked surprised! 😲",
        "Why don't skeletons fight each other? They don't have the guts! 💀",
        "What do you call cheese that isn't yours? Nacho cheese! 🧀",
        "Why did the math book look sad? Because it had too many problems! 📚",
        "What do you call a fish wearing a bowtie? Sofishticated! 🎩🐟",
        "Why did the computer go to the doctor? Because it had a virus! 💻🤒",
        "Why are ghosts such bad liars? Because you can see right through them! 👻",
        "What’s orange and sounds like a parrot? A carrot! 🥕",
        "How does a penguin build its house? Igloos it together! 🐧",
        "Why don’t programmers like nature? It has too many bugs! 🐞",
        "Why did the chicken join a band? Because it had the drumsticks! 🐔🥁"
    ]
    embed = discord.Embed(
        title="😂 **Here's a Joke for You!**",
        description=random.choice(jokes),
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed)

@bot.command(name="meme", help="Fetches a random meme based on a search term.")
async def meme(ctx, query: str = "funny"):
    url = f"https://api.giphy.com/v1/gifs/search?api_key=7010losSxTtXlgRQnwgDMjsG7uF7mkLa&q={query}&limit=1"
    response = requests.get(url).json()
    if response['data']:
        meme_url = response['data'][0]['images']['original']['url']
        embed = discord.Embed(
            title="😂 **Here's a Meme!**",
            color=discord.Color.magenta()
        )
        embed.set_image(url=meme_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ No memes found.")

@bot.command(name="userinfo", help="Shows detailed information about a specified user.")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title=f"👤 **User Information for {member.display_name}**",
        description=(
            f"**ID:** {member.id}\n"
            f"**Joined:** {member.joined_at.strftime('%Y-%m-%d')}\n"
            f"**Top Role:** {member.top_role.mention}\n"
            f"**Status:** {member.status}\n"
            f"**Account Created:** {member.created_at.strftime('%Y-%m-%d')}"
        ),
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="serverinfo", help="Displays information about a server by ID.")
async def serverinfo(ctx, server_id: int):
    guild = bot.get_guild(server_id)
    if guild:
        embed = discord.Embed(
            title=f"🏢 **Server Information for {guild.name}**",
            description=(
                f"**ID:** {guild.id}\n"
                f"**Owner:** {guild.owner.mention}\n"
                f"**Member Count:** {guild.member_count}\n"
                f"**Region:** {guild.region}\n"
                f"**Created On:** {guild.created_at.strftime('%Y-%m-%d')}"
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Server not found.")

@bot.command(name="fact", help="Shares a random fun fact.")
async def fact(ctx):
    facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
        "Bananas are berries, but strawberries aren't. 🍌🍓",
        "Octopuses have three hearts and blue blood. 🐙💙",
        "A group of flamingos is called a 'flamboyance.' 🦩",
        "Wombat poop is cube-shaped. 🐾",
        "Cows have best friends and can become stressed when separated. 🐄",
        "A day on Venus is longer than a year on Venus. 🌍",
        "The inventor of the frisbee was turned into a frisbee after he died. 🥏",
        "Humans share 50% of their DNA with bananas. 🍌",
        "The world's largest desert is Antarctica. ❄️"
    ]
    embed = discord.Embed(
        title="📚 **Did You Know?**",
        description=random.choice(facts),
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

@bot.command(name="rps", help="🪨 Play Rock-Paper-Scissors against a member!")
async def rps(ctx, opponent: discord.Member):
    if opponent == ctx.author:
        await ctx.send("You can't play against yourself!")
        return

    # Prompt both players to choose
    await ctx.send(f"{ctx.author.mention} has challenged {opponent.mention} to Rock-Paper-Scissors! Both players, please choose: r (Rock), p (Paper), or s (Scissors).")

    def check(message):
        return message.author in [ctx.author, opponent] and message.content.lower() in choices.keys()

    try:
        # Wait for both players' responses
        author_choice_msg = await bot.wait_for("message", check=check, timeout=30.0)
        opponent_choice_msg = await bot.wait_for("message", check=check, timeout=30.0)

        # Get the choices
        author_choice = author_choice_msg.content.lower()
        opponent_choice = opponent_choice_msg.content.lower()

        # Show players' choices
        await ctx.send(f"{ctx.author.mention} chose {choices[author_choice]} and {opponent.mention} chose {choices[opponent_choice]}!")

        # Determine the result
        if author_choice == opponent_choice:
            await ctx.send("It's a tie!")
        elif (author_choice, opponent_choice) in winning_combinations:
            await ctx.send(f"{ctx.author.mention} wins! {winning_combinations[(author_choice, opponent_choice)]}")
        else:
            await ctx.send(f"{opponent.mention} wins! {winning_combinations[(opponent_choice, author_choice)]}")

    except asyncio.TimeoutError:
        await ctx.send("Time's up! The game has been canceled as one or both players did not respond in time.")

@bot.command(name="ping", help="Checks the bot's latency.")
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert to milliseconds
    embed = discord.Embed(
        title="🏓 **Pong!**",
        description=f"Latency: **{latency}ms**",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Run the bot with your token
bot.run("MTMwMjMyNzQyNDQ5MDU0MTE1OA.G4V3NL.OtJdTu3Xpfx9NDqC-dfcp-ZM9SZlgVnnn4vaes")

