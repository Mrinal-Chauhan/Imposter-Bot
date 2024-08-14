import time
def inipoll(players: list):
    polltime = str(int(time.time())+61)
    emojis = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿'.split()
    totalp = len(players)
    msg = ''
    for i in range(totalp):
        msg = msg + emojis[i] +" "+ players[i] +'\n' + '⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛' + '\n\n'
    msg += "\n"+"Ends "+ '<t:'+polltime+':R>'
    return msg

        
def finipoll(votedata: dict):
    totalvotes = sum([j for _,j in votedata.items()])

    players_data = [i for i in votedata.items()]
    players_data.sort(key= lambda x:x[1], reverse=True)

    msg = 'Result of the poll\n\n'
    for i in range(len(players_data)):
        percentage = int(players_data[i][1]/totalvotes*100)
        msg += players_data[i][0] + ' : ' + str(players_data[i][1]) + '\n' + str(percentage) + '% ' + '⬜'*round(percentage/10) + '⬛'*(10-(round(percentage/10))) + '\n'
    return msg

