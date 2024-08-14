TEXT_GAME = """
In this game, All the players are given a word by the operator except one player (who is the imposter)
The game starts with all players saying something related to the given word. The order of speaking is given by the operator.
The Players try to guess and identify who the imposter is. They can do so by calling for a vote.
The vote can only be called after the first round and requires atleast two players wanting to vote.
Every player has the right to justify themselves during the voting.
The one with the majority of votes will be considered the loser if he was the imposter,else everyone else loses and the imposter wins."""
TEXT_FEATURES = """
⇒ **Features**
• Acts as the operator
• Tells the players their words
• Decides an imposter randomly
• Launch a pole for voting
• Multiple gamemodes
• Custom wordlist and time customization.

⇒ **Working**
• call the Bot by "/startgame" 
• Bot will ask the players to react to a message.
• Reacted Players proceed to the game.
• A random word is given to all the players except the imposter (random)
• Gives the list containing the order of speaking.
• Each player is given "30 seconds" (Default) for their turn.
• Verifies that everyone is done with their chances of speaking,and starts the next round.
• After the first round is done, the players can use the command"/vote"
• If two users use their turns to vote in the same round, a pole is initiated and all theplayers have to vote.
• The voting window will be opened for "60 seconds" (Default)
• If there's a tie or there are no votes, another round begins.
• If not, the results are shown."""
TEXT_COMMANDS = """
• **/startgame**
Start the game 

• **/endgame**
End the game

• **/vote**
Initiate voting poll

• **/alter**
change default turn time and voting time

• **/set_wordlist**
Set custom word list  *(comma separated) (upto 10 words)*"""
TEXT_JOIN = """
React with ✅ emoji to join the game.
• **Game Mode**: {}
• **Starting**: {}
"""
TEXT_ORDER = """
Start the game in the order mentioned below!

**Players:**
{}
"""
TEXT_POLL = """
Vote out the imposter(s) to win!
{}
"""