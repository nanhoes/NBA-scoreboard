#!/usr/bin/python3

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import os
import json
import datetime as dt
import time
import sys
import signal
import configparser

class Render:
    def __init__(self):
        # Configuration file
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../config/matrix_options.ini')

        # Configuration for the matrix
        config = configparser.ConfigParser()
        config.read(filename)

        self.options = RGBMatrixOptions()
        self.options.rows = int(config['DEFAULT']['rows'])
        self.options.cols = int(config['DEFAULT']['columns'])
        self.options.chain_length = int(config['DEFAULT']['chain_length'])
        self.options.parallel = int(config['DEFAULT']['parallel'])
        self.options.hardware_mapping = config['DEFAULT']['hardware_mapping']
        self.options.gpio_slowdown = int(config['DEFAULT']['gpio_slowdown'])
        #self.options.brightness = int(config['DEFAULT']['brightness'])
        self.options.row_address_type = int(config['DEFAULT']['row_address_type'])
        self.options.drop_privileges = int(config['DEFAULT']['drop_privileges'])

        self.path = '/home/pi/NBA-scoreboard/scoreboard/'

        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/NBA-scoreboard/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/NBA-scoreboard/rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.font3 = graphics.Font()
        self.font3.LoadFont("/home/pi/NBA-scoreboard/rpi-rgb-led-matrix/fonts/5x8.bdf")
        self.team_colors = {'ATL': [[225, 58, 62], [255, 255, 255]], 'BOS': [[0, 131, 72], [255, 205, 112]], 'BKN': [[100, 100, 100], [0, 0, 0]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [0, 0, 0]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [255, 255, 255]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [196, 206, 211]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [0, 0, 0]], 'MIL': [[0, 71, 27], [240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 125, 197], [0, 0, 0]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [250, 250, 250]], 'SAS': [[186, 195, 201], [0, 0, 0]], 'TOR': [[206, 17, 65], [0, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}

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
            print('Error loading game data.')
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
        canvas2 = matrix.CreateFrameCanvas()

        if game_data == []:
            print('no games')
            graphics.DrawText(canvas, self.font, (63-6*7)/2-1, 14, graphics.Color(150,150,150), 'NO GAMES')
            graphics.DrawText(canvas, self.font, (63-6*5)/2+2, 25, graphics.Color(150,150,150), 'TODAY')

            # NBA Logo
            for line in range(20,30):
                graphics.DrawLine(canvas, 58, line, 60, line, graphics.Color(0, 0, 255))
                graphics.DrawLine(canvas, 60, line, 61, line, graphics.Color(255, 0, 0))
                graphics.DrawLine(canvas, 60, line, 60, line, graphics.Color(255, 255, 255))
            for line in range(22,26):
                graphics.DrawLine(canvas, 58, line, 58, line, graphics.Color(255, 255, 255))
            for line in range(21,27):
                graphics.DrawLine(canvas, 59, line, 59, line, graphics.Color(255, 255, 255))
            for line in range(24,26):
                graphics.DrawLine(canvas, 61, line, 61, line, graphics.Color(255, 255, 255))

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(3600*2)

        for game in game_data:
            hometeam = game['homeTeam']['teamTricode']
            awayteam = game['awayTeam']['teamTricode']

            awayrecord = str(game['awayTeam']['wins']) + '-' + str(game['awayTeam']['losses'])
            homerecord = str(game['homeTeam']['wins']) + '-' + str(game['homeTeam']['losses'])

            home = (game['homeTeam']['teamCity'] + '-' + game['homeTeam']['teamName']).replace(' ', '-').lower()
            away = (game['awayTeam']['teamCity'] + '-' + game['awayTeam']['teamName']).replace(' ', '-').lower()
            if home == 'la-clippers':
                home = 'l-a-clippers'
            if away == 'la-clippers':
                away = 'l-a-clippers'

            gamelink = r'/basketball/nba/{0}-{1}-{2}'.format(away, home, game['gameCode'][0:game['gameCode'].find(r'/')])
            print(awayteam,"@",hometeam)

            try:
                if disp_live_odds == True and game['gameStatus'] == 2 and spreads_data_live is not None:
                    spread = spreads_data_live[gamelink]['spread']
                    over_under = spreads_data_live[gamelink]['over_under']
                else:
                    spread = spreads_data[gamelink]['spread']
                    over_under = spreads_data[gamelink]['over_under']

            except KeyError:
                print('No spreads for this game.')
                spread = ''
                over_under = ''

            for line in range(0,32):
                graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(0, 0, 0))
            for line in range(10,19):
                try:
                    graphics.DrawLine(canvas, 0, line, 18, line, graphics.Color(self.team_colors[hometeam][0][0], self.team_colors[hometeam][0][1], self.team_colors[hometeam][0][2]))
                except:
                    graphics.DrawLine(canvas, 0, line, 18, line, graphics.Color(255, 0, 0))
            for line in range(0,9):
                try:
                    graphics.DrawLine(canvas, 0, line, 18, line, graphics.Color(self.team_colors[awayteam][0][0], self.team_colors[awayteam][0][1], self.team_colors[awayteam][0][2]))
                except:
                    graphics.DrawLine(canvas, 0, line, 18, line, graphics.Color(0, 0, 255))
            homescore = game['homeTeam']['score']
            awayscore = game['awayTeam']['score']

            if game['gameStatus'] != 1: #not upcoming game
                for line in range(10,19):
                    graphics.DrawLine(canvas, 19, line, 38, line, graphics.Color(255, 255, 255))
                for line in range(0,9):
                    graphics.DrawLine(canvas, 19, line, 38, line, graphics.Color(255, 255, 255))
                if spread != "":
                    if (homescore-awayscore) >= float(spread)*(-1):
                        graphics.DrawText(canvas, self.font2, 64 - len(str(over_under))*4, 7, graphics.Color(0, 0, 255), over_under)
                        graphics.DrawText(canvas, self.font2, 64 - len(str(spread))*4, 17, graphics.Color(0, 0, 255), spread)
                    else:
                        away_spread = float(spread)*(-1)
                        graphics.DrawText(canvas, self.font2, 64 - len(str(over_under))*4, 17, graphics.Color(0, 0, 255), over_under)
                        graphics.DrawText(canvas, self.font2, 64 - len(str(away_spread))*4, 7, graphics.Color(0, 0, 255), str(away_spread))
                else:
                    graphics.DrawText(canvas, self.font2, 64 - len(str(over_under))*4, 7, graphics.Color(0, 0, 255), over_under)
                    graphics.DrawText(canvas, self.font2, 64 - len(str(spread))*4, 17, graphics.Color(0, 0, 255), spread)
            else:
                graphics.DrawText(canvas, self.font2, 64 - len(str(over_under))*4, 7, graphics.Color(0, 0, 255), over_under)
                graphics.DrawText(canvas, self.font2, 64 - len(str(spread))*4, 17, graphics.Color(0, 0, 255), spread)

            try:
                graphics.DrawText(canvas, self.font, 1, 18, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
                graphics.DrawText(canvas, self.font, 1, 8, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
            except:
                graphics.DrawText(canvas, self.font, 1, 18, graphics.Color(255, 255, 255), hometeam)
                graphics.DrawText(canvas, self.font, 1, 8, graphics.Color(255, 255, 255), awayteam)

            # NBA Logo
            for line in range(20,30):
                graphics.DrawLine(canvas, 58, line, 60, line, graphics.Color(0, 0, 255))
                graphics.DrawLine(canvas, 60, line, 61, line, graphics.Color(255, 0, 0))
                graphics.DrawLine(canvas, 60, line, 60, line, graphics.Color(255, 255, 255))
            for line in range(22,26):
                graphics.DrawLine(canvas, 58, line, 58, line, graphics.Color(255, 255, 255))
            for line in range(21,27):
                graphics.DrawLine(canvas, 59, line, 59, line, graphics.Color(255, 255, 255))
            for line in range(24,26):
                graphics.DrawLine(canvas, 61, line, 61, line, graphics.Color(255, 255, 255))

            period = game['period']
            timeremaining = game['gameStatusText']
            if timeremaining[0] == 'Q' or timeremaining[0] == 'O':
                if period <= 5 and timeremaining[3] == '0':
                    timeremaining = timeremaining[:3] + timeremaining[4:]
                    if timeremaining[3] == '0':
                        timeremaining = timeremaining[:3] + timeremaining[4:]
                if period > 5 and timeremaining[4] == '0':
                    timeremaining = timeremaining[:4] + timeremaining[5:]
                    if timeremaining[4] == '0':
                        timeremaining = timeremaining[:4] + timeremaining[5:]
                if period == 1:
                    timeremaining = '1ST' + timeremaining[2:]
                if period == 2:
                    timeremaining = '2ND' + timeremaining[2:]
                if period == 3:
                    timeremaining = '3RD' + timeremaining[2:]
                if period == 4:
                    timeremaining = '4TH' + timeremaining[2:]
                if period == 5:
                    timeremaining = 'OT ' + timeremaining[3:]
                if period == 6:
                    timeremaining = 'OT2' + timeremaining[3:]
                if period == 7:
                    timeremaining = 'OT3' + timeremaining[3:]
                if period == 8:
                    timeremaining = 'OT4' + timeremaining[3:]
            if timeremaining == 'Half':
                timeremaining = 'HALFTIME'

            timeremaining = timeremaining.upper()

            if game['gameStatus'] == 2: #game is live
                graphics.DrawText(canvas, self.font, 35 - len(str(awayscore))*5, 8, graphics.Color(0, 0, 0), str(awayscore))
                graphics.DrawText(canvas, self.font, 35 - len(str(homescore))*5, 18, graphics.Color(0, 0, 0), str(homescore))
                if ((period >= 4) and (game['gameStatusText'][3] == '0' and game['gameStatusText'][4] <= '4')) or period > 4: #Q4 or OT < 5min remaining
                    if homescore > awayscore:
                        if (homescore - awayscore) <= 10: #close game
                            start_time = time.time()
                            seconds = 5
                            while True:
                                current_time = time.time()
                                elapsed_time = current_time - start_time
                                i = 50
                                for line in range(0,100):
                                    i += 2
                                    graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(i, i, i), timeremaining) #bright quarter and time remaining
                                    graphics.DrawLine(canvas2, 0, 31, line, 31, graphics.Color(255, 0, 0)) #red line at bottom of screen
                                    canvas2 = matrix.SwapOnVSync(canvas)
                                    time.sleep(.008)
                                for line2 in range(0,100):
                                    i -= 2
                                    graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(i, i, i), timeremaining) #bright quarter and time remaining
                                    graphics.DrawLine(canvas2, 0, 31, line2, 31, graphics.Color(0, 0, 0)) #red line at bottom of screen
                                    canvas2 = matrix.SwapOnVSync(canvas)
                                    time.sleep(.008)
                                if elapsed_time > seconds:
                                    break
                            continue
                        else:
                            if timeremaining[0] == '1':
                                graphics.DrawText(canvas, self.font3, 1, 28, graphics.Color(200, 200, 200), timeremaining)
                            else:
                                graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(200, 200, 200), timeremaining)
                    else:
                        if (awayscore - homescore) <= 10: #close game
                            start_time = time.time()
                            seconds = 5
                            while True:
                                current_time = time.time()
                                elapsed_time = current_time - start_time
                                i = 50
                                for line in range(0,100):
                                    i += 2
                                    graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(i, i, i), timeremaining) #pulse time remaining
                                    graphics.DrawLine(canvas2, 0, 31, line, 31, graphics.Color(255, 0, 0)) #red line at bottom of screen
                                    canvas2 = matrix.SwapOnVSync(canvas)
                                    time.sleep(.008)
                                for line2 in range(0,100):
                                    i -= 2
                                    graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(i, i, i), timeremaining) #pulse time remaining
                                    graphics.DrawLine(canvas2, 0, 31, line2, 31, graphics.Color(0, 0, 0)) #red line at bottom of screen
                                    canvas2 = matrix.SwapOnVSync(canvas)
                                    time.sleep(.008)
                                if elapsed_time > seconds:
                                    break
                            continue
                        else:
                            if timeremaining[0] == '1':
                                graphics.DrawText(canvas, self.font3, 1, 28, graphics.Color(200, 200, 200), timeremaining)
                            else:
                                graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(200, 200, 200), timeremaining)
                else: #not a close game or not under 4min
                    graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(200, 200, 200), timeremaining)

            if game['gameStatus'] == 3: #finished game
                if homescore < awayscore:
                    for line in range(10,19):
                        graphics.DrawLine(canvas, 19, line, 38, line, graphics.Color(75, 75, 75))
                else:
                    for line in range(0,9):
                        graphics.DrawLine(canvas, 19, line, 38, line, graphics.Color(75, 75, 75))
                graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(200, 200, 200), game['gameStatusText'].upper())
                graphics.DrawText(canvas, self.font, 35 - len(str(awayscore))*5, 8, graphics.Color(0, 0, 0), str(awayscore))
                graphics.DrawText(canvas, self.font, 35 - len(str(homescore))*5, 18, graphics.Color(0, 0, 0), str(homescore))


            if game['gameStatus'] == 1: #upcoming game
                graphics.DrawText(canvas, self.font2, 21, 7, graphics.Color(200, 200, 200), awayrecord) #away team record
                graphics.DrawText(canvas, self.font2, 21, 16, graphics.Color(200, 200, 200), homerecord) #home team record
                if game['gameStatusText'] != 'PPD': #upcoming game
                    if game['gameStatusText'][0] == '1':
                        graphics.DrawText(canvas, self.font3, 1, 28, graphics.Color(200, 200, 200), game['gameStatusText'][0:game['gameStatusText'].find('ET')].upper() + 'et'.upper())
                    else:
                        graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(200, 200, 200), game['gameStatusText'][0:game['gameStatusText'].find('ET')].upper() + 'et'.upper())
                if game['gameStatusText'] == 'PPD': #postponed game
                    graphics.DrawText(canvas, self.font3, 2, 28, graphics.Color(200, 200, 200), 'POSTPONED')


            for line in range(0,56):
                graphics.DrawLine(canvas, 121, line, 125, line, graphics.Color(255, 0, 0))


            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(5)

if __name__=='__main__':
    while True:
        Render().Render_Games()
