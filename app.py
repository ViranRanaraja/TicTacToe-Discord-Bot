import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv, find_dotenv

client = commands.Bot(command_prefix="!")

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    servernum = str(len(client.guilds))
    print('Currently in ' + servernum)


@client.command()
async def bot(ctx):
    await ctx.send("!tt @player1 @player2  -  Use this command to start a game of tictactoe with a friend.")
    await ctx.send("`\n`")
    await ctx.send("!place (number between 1 and 9)  -  Use this to place either an X or O on the board.")
    await ctx.send("`\n`")
    await ctx.send("!end -  Use this to end a game that has begun. But one of the two people playing the game must use this command.")


@client.command()
async def tt(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        members = ctx.guild.members

        for member in members:
            if p1 == member or p2 == member:
                await ctx.send("Still not smart enough to compete against your intellect.")
            elif p1 == p2:
                await ctx.send("Tag a friend, its no fun to play by yourself.")
            else:
                global board
                board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                         ":white_large_square:", ":white_large_square:", ":white_large_square:",
                         ":white_large_square:", ":white_large_square:", ":white_large_square:"]
                turn = ""
                gameOver = False
                count = 0

                player1 = p1
                player2 = p2

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                # determine who goes first
                num = random.randint(1, 2)
                if num == 1:
                    turn = player1
                    await ctx.send("You start first <@" + str(player1.id) + "> !!")
                elif num == 2:
                    turn = player2
                    await ctx.send("You start first <@" + str(player2.id) + "> !!")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")


@client.command()
async def end(ctx):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        if ctx.author.id == player1.id or ctx.author.id == player2.id:
            gameOver = True
            await ctx.send("<@" + str(ctx.author.id) + "> Has decided to stop the game.")
        else:
            await ctx.send("One of the two people who started the game can stop the game.")
    else:
        await ctx.send("This is impossible. How to stop a game that hasn't even begun.")


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                # print(count)
                if gameOver:
                    if mark == ":regional_indicator_x:":
                        await ctx.send("Congrats <@" + str(player1.id) + "> for winning! :tada: :tada:")
                    else:
                        await ctx.send("Congratulations <@" + str(player2.id) + "> for the win! :tada: :tada:")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")
                else:
                    if mark == ":regional_indicator_x:":
                        await ctx.send("Your turn <@" + str(player2.id) + ">!!")
                    else:
                        await ctx.send("Your turn <@" + str(player1.id) + ">!!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tt command.")


def checkWinner(winningchance, mark):
    global gameOver
    for condition in winningchance:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tt.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


load_dotenv(find_dotenv())

client.run(os.getenv('TOKEN'))
