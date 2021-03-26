from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import os
import json
import datetime as dt
import time
import sys

class Render:
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.gpio_slowdown = 1
        self.options.rows = 64
        self.options.cols = 128
        self.options.drop_privileges = False
        self.options.hardware_mapping = 'adafruit-hat-pwm'
        self.options.row_address_type = 3
        self.options.panel_type = 'FM6126A'


        
        self.path = '/home/pi/My-NBA-scoreboard/'
        
        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/My-NBA-scoreboard/Minimal-Mono-Bold.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/My-NBA-scoreboard/rpi-rgb-led-matrix/fonts/8x13B.bdf")
        self.font3 = graphics.Font()
        self.font3.LoadFont("/home/pi/My-NBA-scoreboard/rpi-rgb-led-matrix/fonts/9x18B.bdf")
        self.font4 = graphics.Font()
        self.font4.LoadFont("/home/pi/My-NBA-scoreboard/rpi-rgb-led-matrix/fonts/5x8.bdf")
        self.team_colors = {'ATL': [[225, 58, 62], [255, 255, 255]], 'BOS': [[0, 131, 72], [255, 205, 112]], 'BKN': [[100, 100, 100], [0, 0, 0]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [0, 0, 0]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [196, 206, 211]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [196, 206, 211]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [0, 0, 0]], 'MIL': [[0, 71, 27], [240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 125, 197], [0, 0, 0]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [200, 200, 200]], 'SAS': [[186, 195, 201], [0, 0, 0]], 'TOR': [[206, 17, 65], [0, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}
                    
    def Render_Games(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        date_range = []
        disp_live_odds = True
        try:
            for day in os.listdir(self.path):
                if day=='.DS_Store':
                    continue
                if day == 'DataToday.json':
                    with open(self.path + day) as file:
                        game_data = json.load(file)
                
        except:
            print('Error loading spreads data.')
            game_data = {}
        
        try:
            with open(self.path + 'NBASpreads.json', 'r') as file:
                spreads_data = json.load(file)
            with open(self.path + 'NBASpreadsLive.json', 'r') as file:
                spreads_data_live = json.load(file)
                
        except:
            print('Error loading spreads data.')
            spreads_data = {}
            
        canvas = matrix.CreateFrameCanvas()
       
        for game in game_data:
            hometeam = game['homeTeam']['teamTricode']
            awayteam = game['awayTeam']['teamTricode']

            home = (game['homeTeam']['teamCity'] + '-' + game['homeTeam']['teamName']).replace(' ', '-').lower()
            away = (game['awayTeam']['teamCity'] + '-' + game['awayTeam']['teamName']).replace(' ', '-').lower()
            if home == 'la-clippers':
                home = 'l-a-clippers'
            if away == 'la-clippers':
                away = 'l-a-clippers'

            gamelink = r'/basketball/nba/{0}-{1}-{2}'.format(away, home, game['gameCode'][0:game['gameCode'].find(r'/')])
            print(gamelink)

            try:
                if disp_live_odds == True and game['gameStatus'] == 2:
                    spread = spreads_data_live[gamelink]['spread']
                    over_under = spreads_data_live[gamelink]['over_under']
                else:       
                    spread = spreads_data[gamelink]['spread']
                    over_under = spreads_data[gamelink]['over_under']

            except KeyError:
                spread = ''
                over_under = ''
            
            posx = 5
            len1 = 0
            while True:
                for line in range(0,64):	
                    graphics.DrawLine(canvas, 0, line, 128, line, graphics.Color(0, 0, 0)) #clearing matrix
                                                
                for line in range(20,38): #team color square
                    graphics.DrawLine(canvas, 0, line, 39, line, graphics.Color(self.team_colors[hometeam][0][0], self.team_colors[hometeam][0][1], self.team_colors[hometeam][0][2]))
                for line in range(0,18): #team color square
                    graphics.DrawLine(canvas, 0, line, 39, line, graphics.Color(self.team_colors[awayteam][0][0], self.team_colors[awayteam][0][1], self.team_colors[awayteam][0][2]))

                if game['gameStatus'] != 1: #white square for score
                    for line in range(20,38):
                        graphics.DrawLine(canvas, 40, line, 79, line, graphics.Color(255, 255, 255))
                    for line in range(0,18):
                        graphics.DrawLine(canvas, 40, line, 79, line, graphics.Color(255, 255, 255))

                graphics.DrawText(canvas, self.font2, 127 - len(str(over_under))*8, 14, graphics.Color(0, 0, 255), over_under)
                graphics.DrawText(canvas, self.font2, 127 - len(str(spread))*8, 34, graphics.Color(0, 0, 255), spread)
                graphics.DrawText(canvas, self.font, 2, 36, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
                graphics.DrawText(canvas, self.font, 2, 16, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)

                homescore = game['homeTeam']['score']
                awayscore = game['awayTeam']['score']
                timeremaining = game['gameStatusText']
                if timeremaining[0] == 'Q' and timeremaining[3] == '0':
                    timeremaining = game['gameStatusText'][:3] + game['gameStatusText'][4:]
                if timeremaining[0] == 'Q' and timeremaining[3] == '0' and timeremaining[4] == ':':
                    timeremaining = game['gameStatusText'][:3] + game['gameStatusText'][5:]



                if game['gameStatus'] == 2: #GAME IS LIVE
                    graphics.DrawText(canvas, self.font, 75 - len(str(awayscore))*11, 16, graphics.Color(0, 0, 0), str(awayscore)) 
                    graphics.DrawText(canvas, self.font, 75 - len(str(homescore))*11, 36, graphics.Color(0, 0, 0), str(homescore)) 
                    if timeremaining[0] == 'Q' and (timeremaining[1] >= '4' and (len(timeremaining) == 6 or (len(timeremaining) == 7 and timeremaining[3] <= '4'))): #Q4 or OT < 5min remaining
                        if homescore > awayscore:
                            if (homescore - awayscore) <= 15: #close game
                                graphics.DrawText(canvas, self.font3, 2, 51, graphics.Color(255, 255, 255), timeremaining) #bright quarter and time remaining
                                for line in range(54,56):   
                                    graphics.DrawLine(canvas, 0, line, 127, line, graphics.Color(255, 0, 0)) #red line at bottom of screen
                            else:
                                graphics.DrawText(canvas, self.font3, 2, 52, graphics.Color(200, 200, 200), timeremaining)
                        else:
                            if (awayscore - homescore) <= 15: #close game
                                graphics.DrawText(canvas, self.font3, 2, 51, graphics.Color(255, 255, 255), timeremaining) #bright quarter and time remaining
                                for line in range(54,56):   
                                    graphics.DrawLine(canvas, 0, line, 127, line, graphics.Color(255, 0, 0)) #red line at bottom of screen
                            else:
                                graphics.DrawText(canvas, self.font3, 2, 52, graphics.Color(200, 200, 200), timeremaining)
                    else: #not a close game or not under 4min
                        if timeremaining[1] == '1':
                            graphics.DrawText(canvas, self.font3, 2, 52, graphics.Color(200, 200, 200), timeremaining) #56
                        else:
                            graphics.DrawText(canvas, self.font3, 2, 52, graphics.Color(200, 200, 200), timeremaining)

                   

                if game['gameStatus'] == 3: #GAME IS FINISHED
                    graphics.DrawText(canvas, self.font3, 2, 52, graphics.Color(200, 200, 200), game['gameStatusText'].upper()) #56
                    graphics.DrawText(canvas, self.font, 75 - len(str(awayscore))*11, 16, graphics.Color(0, 0, 0), str(awayscore)) 
                    graphics.DrawText(canvas, self.font, 75 - len(str(homescore))*11, 36, graphics.Color(0, 0, 0), str(homescore)) 

                    if homescore > awayscore:
                        for line in range(21,37):
                            graphics.DrawLine(canvas, 81, line, 82, line, graphics.Color(100, 100, 100))
                    else:
                        for line in range(1,17):
                            graphics.DrawLine(canvas, 81, line, 82, line, graphics.Color(100, 100, 100))


                if game['gameStatus'] == 1: #GAME IS UPCOMING
                    awayrecord = str(game['awayTeam']['wins']) + '-' + str(game['awayTeam']['losses'])
                    homerecord = str(game['homeTeam']['wins']) + '-' + str(game['homeTeam']['losses'])
                    graphics.DrawText(canvas, self.font2, 41, 14, graphics.Color(200, 200, 200), awayrecord) #away team record
                    graphics.DrawText(canvas, self.font2, 41, 34, graphics.Color(200, 200, 200), homerecord) #home team record
                    if game['gameStatusText'] != 'PPD': #upcoming game
                        graphics.DrawText(canvas, self.font3, 2, 56, graphics.Color(200, 200, 200), game['gameStatusText'][0:game['gameStatusText'].find('ET')].upper() + 'ET')
                    if game['gameStatusText'] == 'PPD': #postponed game
                        graphics.DrawText(canvas, self.font3, 2, 56, graphics.Color(200, 200, 200), 'POSTPONED')



                if game['gameStatus'] != 1: #and game['period'] !=1:
                    homeleadername = game['gameLeaders']['homeLeaders']['name']
                    homeleaderpoints = game['gameLeaders']['homeLeaders']['points']
                    homeleaderrebounds = game['gameLeaders']['homeLeaders']['rebounds']
                    homeleaderassists = game['gameLeaders']['homeLeaders']['assists']
                    def findhomelastname(homeleadername,n):
                        #Using ' ' as a separator, All_words is a list of all the words in the String
                        All_words=homeleadername.split(" ")
                        return All_words[n-1]
                    homeleaderlastname = findhomelastname(homeleadername,2)
                    homestatline = homeleadername[0] + '.'+ str(homeleaderlastname) + ' ' + str(homeleaderpoints) + '-' + str(homeleaderrebounds) + '-' + str(homeleaderassists)

                    awayleadername = game['gameLeaders']['awayLeaders']['name']
                    awayleaderpoints = game['gameLeaders']['awayLeaders']['points']
                    awayleaderrebounds = game['gameLeaders']['awayLeaders']['rebounds']
                    awayleaderassists = game['gameLeaders']['awayLeaders']['assists']
                    def findawaylastname(awayleadername,n):
                        #Using ' ' as a separator, All_words is a list of all the words in the String
                        All_words2=awayleadername.split(" ")
                        return All_words2[n-1]
                    awayleaderlastname = findawaylastname(awayleadername,2) 
                    awaystatline = awayleadername[0] + '.' + str(awayleaderlastname) + ' ' + str(awayleaderpoints) + '-' + str(awayleaderrebounds) + '-' + str(awayleaderassists)
                    
                    for line in range(56,64): #statline background
                        graphics.DrawLine(canvas, 0, line, 127, line, graphics.Color(255, 255, 255))
                    
                    len1 = graphics.DrawText(canvas, self.font4, posx, 63, graphics.Color(0, 0, 0), awaystatline.upper() + '  ' + homestatline.upper())
                    if len1 <= canvas.width:
                        break
                    else:
                        posx -= 1
                        if (posx == canvas.width - len1 - 2):
                            break
                        time.sleep(0.02)
                        canvas = matrix.SwapOnVSync(canvas)
                else:
                    break
                               

                            
            if (posx == canvas.width - len1 - 2):
                time.sleep(2)
                canvas = matrix.SwapOnVSync(canvas)            
            else:
                canvas = matrix.SwapOnVSync(canvas)            
                time.sleep(5)
if __name__=='__main__':
    while True:
        Render().Render_Games()
      
