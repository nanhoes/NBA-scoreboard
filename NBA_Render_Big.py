from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import os
import json
import datetime as dt
import time
import sys
from PIL import Image

class Render:
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False
        self.options.chain_length = 2
        self.options.parallel = 2
        self.options.disable_hardware_pulsing = True
                   
        now = dt.datetime.now()
        current_time = now.strftime("%H:%M") 
        if current_time[0] == '0' and (current_time[1] >= '23' and current_time[1] <= '7'):
            self.options.brightness = 10
        else:
            self.options.brightness = 100
        
        self.path = '/home/pi/My-NBA-scoreboard/'
        
        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/My-NBA-scoreboard/Minimal-Mono-Bold.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/My-NBA-scoreboard/rpi-rgb-led-matrix/fonts/8x13B.bdf")
        self.font3 = graphics.Font()
        self.font3.LoadFont("/home/pi/My-NBA-scoreboard/rpi-rgb-led-matrix/fonts/9x18B.bdf")
        self.team_colors = {'ATL': [[225, 58, 62], [100, 100, 100]], 'BOS': [[0, 131, 72], [187, 151, 83]], 'BKN': [[100, 100, 100], [0, 0, 0]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [0, 0, 0]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [196, 206, 211]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [196, 206, 211]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [0, 0, 0]], 'MIL': [[0, 71, 27], [240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 125, 197], [0, 0, 0]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [142, 144, 144]], 'SAS': [[186, 195, 201], [0, 0, 0]], 'TOR': [[206, 17, 65], [0, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}
            
    def Render_Games(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        date_range = []
        disp_live_odds = False
        try:
            for day in os.listdir(self.path):
                if day=='.DS_Store':
                    continue
                if day == 'DataTodayTest.json':
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
        image = Image.open("/home/pi/My-NBA-scoreboard/lal.png")
        image1 = Image.open("/home/pi/My-NBA-scoreboard/bkn.png")
                  
        for game in game_data:
            for line in range(0,64):
                graphics.DrawLine(canvas, 0, line, 128, line, graphics.Color(0, 0, 0))

                        
            # Make image fit our screen.
          #  image.thumbnail((30, matrix.height))
           # matrix.SetImage(image.convert('RGB'),5,0)
            #image1.thumbnail((30, matrix.height))
            #matrix.SetImage(image1.convert('RGB'),93,0)
                    
           # canvas = matrix.SwapOnVSync(canvas)
            
        
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
                #print('No spreads for this game.')
                spread = ''
                over_under = ''
                                    
            for line in range(20,38):
                graphics.DrawLine(canvas, 0, line, 38, line, graphics.Color(self.team_colors[hometeam][0][0], self.team_colors[hometeam][0][1], self.team_colors[hometeam][0][2]))
            for line in range(0,18):
                graphics.DrawLine(canvas, 0, line, 38, line, graphics.Color(self.team_colors[awayteam][0][0], self.team_colors[awayteam][0][1], self.team_colors[awayteam][0][2]))
            graphics.DrawText(canvas, self.font2, 127 - len(str('232.0'))*8, 14, graphics.Color(0, 0, 200), '232.0')#over_under)
            graphics.DrawText(canvas, self.font2, 127 - len(str('-5.5'))*8, 34, graphics.Color(0, 0, 200), '-5.5')#spread)
            graphics.DrawText(canvas, self.font, 2, 36, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
            graphics.DrawText(canvas, self.font, 2, 16, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
         
            
            homescore = game['homeTeam']['score']
            awayscore = game['awayTeam']['score']
            if game['gameStatus'] == 2: #game is live
                graphics.DrawText(canvas, self.font, 42, 16, graphics.Color(255, 255, 255), str(awayscore)) #bright score
                graphics.DrawText(canvas, self.font, 42, 36, graphics.Color(255, 255, 255), str(homescore)) #bright score
                timeremaining = game['gameStatusText']
                if timeremaining[0] == 'Q' and (timeremaining[1] >= '4' and (timeremaining[3] == '0' and timeremaining[4] <= '4')): #Q4 or OT < 5min remaining
                    if homescore > awayscore:
                        if (homescore - awayscore) <= 15: #close game
                            graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(255, 255, 255), game['gameStatusText']) #bright quarter and time remaining
                            graphics.DrawLine(canvas, 0, 62, 126, 62, graphics.Color(255, 0, 0)) #red line at bottom of screen
                        else:
                            graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(100, 100, 100), game['gameStatusText'])
                    else:
                        if (awayscore - homescore) <= 15: #close game
                            graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(255, 255, 255), game['gameStatusText']) #bright quarter and time remaining
                            graphics.DrawLine(canvas, 0, 62, 126, 62, graphics.Color(255, 0, 0)) #red line at bottom of screen
                        else:
                            graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(100, 100, 100), game['gameStatusText'])
                else: #not a close game or not under 4min
                    graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(100, 100, 100), game['gameStatusText'])
                
            if game['gameStatus'] == 3: #finished game
                graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(255, 0, 0), game['gameStatusText'].upper()) #red '"final" text
                if homescore > awayscore:
                    graphics.DrawText(canvas, self.font, 42, 36, graphics.Color(255, 255, 255), str(homescore)) #bright home winner score
                    graphics.DrawText(canvas, self.font, 42, 16, graphics.Color(100, 100, 100), str(awayscore)) #bright away winner score

                else:
                    graphics.DrawText(canvas, self.font, 42, 16, graphics.Color(255, 255, 255), str(awayscore)) #bright away winner score
                    graphics.DrawText(canvas, self.font, 42, 36, graphics.Color(100, 100, 100), str(homescore)) #bright home winner score

            if game['gameStatus'] == 1: #upcoming game
                awayrecord = str(game['awayTeam']['wins']) + '-' + str(game['awayTeam']['losses'])
                homerecord = str(game['homeTeam']['wins']) + '-' + str(game['homeTeam']['losses'])
                graphics.DrawText(canvas, self.font2, 41, 14, graphics.Color(100, 100, 100), awayrecord) #away team record
                graphics.DrawText(canvas, self.font2, 41, 34, graphics.Color(100, 100, 100), homerecord) #home team record
                if game['gameStatusText'] != 'PPD': #upcoming game
                    graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(100, 100, 100), game['gameStatusText'][0:len(game['gameStatusText']) - 3])
                if game['gameStatusText'] == 'PPD': #postponed game
                    graphics.DrawText(canvas, self.font3, 2, 58, graphics.Color(100, 100, 100), 'Postponed')
                      
            if game['gameStatus'] != 1 and game['period'] !=1:
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

        

              #  pos = 0
               # while True:         
                #    print(homestatline)
                 #   for x in range(0, canvas.width):
                  #      for y in range(20, canvas.height):
                   #         canvas.SetPixel(x, y, 0, 0, 0)
                    #len1 = graphics.DrawText(canvas, self.font2, pos, 31, graphics.Color(self.team_colors[hometeam][0][0], self.team_colors[hometeam][0][1], self.team_colors[hometeam][0][2]), homestatline)
              #      pos -= 1
               #     if (pos + len1 < 0):
                #        pos = canvas.width
                 #   
                  #  time.sleep(0.04)
                    

            canvas = matrix.SwapOnVSync(canvas)            
            time.sleep(4)
            #canvas = matrix.SwapOnVSync(canvas)            
           
            
            
if __name__=='__main__':
    while True:
        Render().Render_Games()
        
        
