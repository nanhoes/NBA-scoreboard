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
        self.options.brightness = int(config['DEFAULT']['brightness'])
        self.options.row_address_type = int(
            config['DEFAULT']['row_address_type'])
        self.options.drop_privileges = int(
            config['DEFAULT']['drop_privileges'])

        self.path = '/home/pi/NBA-scoreboard/scoreboard/'

        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/NBA-scoreboard/Minimal-Mono-Bold-28.bdf") # TEAM NAME AND SCORES
        self.font2 = graphics.Font()
        self.font2.LoadFont(
            "/home/pi/NBA-scoreboard/Minimal-Mono-Bold-15.bdf") # RECORDS & ODDS
        self.font3 = graphics.Font()
        self.font3.LoadFont(
            "/home/pi/NBA-scoreboard/Minimal-Mono-Bold-19.bdf") # TIME
        self.font4 = graphics.Font()
        self.font4.LoadFont(
            "/home/pi/NBA-scoreboard/rpi-rgb-led-matrix/fonts/8x13B.bdf") # STATLINE
        self.team_colors = {'ATL': [[225, 58, 62], [255, 255, 255]], 'BOS': [[0, 131, 72], [255, 205, 112]], 'BKN': [[100, 100, 100], [0, 0, 0]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [0, 0, 0]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [196, 206, 211]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [196, 206, 211]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [0, 0, 0]], 'MIL': [[0, 71, 27], [
            240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 125, 197], [0, 0, 0]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [200, 200, 200]], 'SAS': [[186, 195, 201], [0, 0, 0]], 'TOR': [[206, 17, 65], [0, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}

    def Render_Games(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        date_range = []
        disp_live_odds = True
        try:
            for day in os.listdir(self.path):
                if day == '.DS_Store':
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

        x_offset_stats = 0
        y_offset_stats = 0
        x_offset_no_stats = 0
        y_offset_no_stats = 11

        if game_data == []:
            print('no games')
            graphics.DrawText(canvas, self.font, 192/2-21*8/2+2, 40, graphics.Color(150, 150, 150), 'NO GAMES')
            graphics.DrawText(canvas, self.font, 192/2-21*5/2, 96-18, graphics.Color(150, 150, 150), 'TODAY')

            # NBA Logo
            for line in range(55+y_offset_no_stats, 80+y_offset_no_stats):
                graphics.DrawLine(canvas, 178+x_offset_no_stats, line,
                                  188+x_offset_no_stats, line, graphics.Color(0, 0, 255))
                graphics.DrawLine(canvas, 188+x_offset_no_stats, line,
                                  188+x_offset_no_stats, line, graphics.Color(255, 0, 0))
            for line in range(55+y_offset_no_stats, 76+y_offset_no_stats):
                graphics.DrawLine(canvas, 185+x_offset_no_stats, line,
                                  187+x_offset_no_stats, line, graphics.Color(255, 0, 0))
            for line in range(63+y_offset_no_stats, 66+y_offset_no_stats):
                graphics.DrawLine(canvas, 178+x_offset_no_stats, line,
                                  178+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(60+y_offset_no_stats, 69+y_offset_no_stats):
                graphics.DrawLine(canvas, 179+x_offset_no_stats, line,
                                  179+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(59+y_offset_no_stats, 71+y_offset_no_stats):
                graphics.DrawLine(canvas, 180+x_offset_no_stats, line,
                                  180+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(59+y_offset_no_stats, 72+y_offset_no_stats):
                graphics.DrawLine(canvas, 181+x_offset_no_stats, line,
                                  181+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(58+y_offset_no_stats, 73+y_offset_no_stats):
                graphics.DrawLine(canvas, 182+x_offset_no_stats, line,
                                  182+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(55+y_offset_no_stats, 74+y_offset_no_stats):
                graphics.DrawLine(canvas, 183+x_offset_no_stats, line,
                                  183+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(55+y_offset_no_stats, 64+y_offset_no_stats):
                graphics.DrawLine(canvas, 184+x_offset_no_stats, line,
                                  184+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(64+y_offset_no_stats, 66+y_offset_no_stats):
                graphics.DrawLine(canvas, 184+x_offset_no_stats, line,
                                  184+x_offset_no_stats, line, graphics.Color(255, 0, 0))
            for line in range(66+y_offset_no_stats, 75+y_offset_no_stats):
                graphics.DrawLine(canvas, 184+x_offset_no_stats, line,
                                  184+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(59+y_offset_no_stats, 64+y_offset_no_stats):
                graphics.DrawLine(canvas, 185+x_offset_no_stats, line,
                                  185+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(71+y_offset_no_stats, 77+y_offset_no_stats):
                graphics.DrawLine(canvas, 185+x_offset_no_stats, line,
                                  185+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(72+y_offset_no_stats, 78+y_offset_no_stats):
                graphics.DrawLine(canvas, 186+x_offset_no_stats, line,
                                  186+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(60+y_offset_no_stats, 66+y_offset_no_stats):
                graphics.DrawLine(canvas, 186+x_offset_no_stats, line,
                                  186+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(67+y_offset_no_stats, 70+y_offset_no_stats):
                graphics.DrawLine(canvas, 186+x_offset_no_stats, line,
                                  186+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(63+y_offset_no_stats, 70+y_offset_no_stats):
                graphics.DrawLine(canvas, 187+x_offset_no_stats, line,
                                  187+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(75+y_offset_no_stats, 80+y_offset_no_stats):
                graphics.DrawLine(canvas, 187+x_offset_no_stats, line,
                                  187+x_offset_no_stats, line, graphics.Color(255, 255, 255))
            for line in range(67+y_offset_no_stats, 70+y_offset_no_stats):
                graphics.DrawLine(canvas, 188+x_offset_no_stats, line,
                                  188+x_offset_no_stats, line, graphics.Color(255, 255, 255))

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(3600*2)

        for game in game_data:
            hometeam = game['homeTeam']['teamTricode']
            awayteam = game['awayTeam']['teamTricode']

            home = (game['homeTeam']['teamCity'] + '-' +
                    game['homeTeam']['teamName']).replace(' ', '-').lower()
            away = (game['awayTeam']['teamCity'] + '-' +
                    game['awayTeam']['teamName']).replace(' ', '-').lower()
            if home == 'la-clippers':
                home = 'l-a-clippers'
            if away == 'la-clippers':
                away = 'l-a-clippers'

            gamelink = r'/basketball/nba/{0}-{1}-{2}'.format(
                away, home, game['gameCode'][0:game['gameCode'].find(r'/')])
            try:
                if disp_live_odds == True and game['gameStatus'] == 2 and spreads_data_live is not None:
                    spread = spreads_data_live[gamelink]['spread']
                    over_under = spreads_data_live[gamelink]['over_under']
                else:
                    spread = spreads_data[gamelink]['spread']
                    over_under = spreads_data[gamelink]['over_under']

            except KeyError:
                spread = ''
                over_under = ''
                print("Error")

            posx = 5
            len1 = 0

            while True:
                # CLEARING MATRIX
                for line in range(0, 96):
                    graphics.DrawLine(canvas, 0, line, 192, line, graphics.Color(
                        0, 0, 0))

                # TEAM COLOR SQUARE
                for line in range(31, 61):
                    try:
                        graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(self.team_colors[hometeam][0][0], self.team_colors[hometeam][0][1], self.team_colors[hometeam][0][2]))
                    except:
                        graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(255, 0, 0))
                for line in range(0, 30):
                    try:
                        graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(self.team_colors[awayteam][0][0], self.team_colors[awayteam][0][1], self.team_colors[awayteam][0][2]))
                    except:
                        graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(0, 0, 255))

                # TEAM NAMES
                try:
                    graphics.DrawText(canvas, self.font, 4, 57, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
                    graphics.DrawText(canvas, self.font, 4, 26, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
                except:
                    graphics.DrawText(canvas, self.font, 4, 57, graphics.Color(255, 255, 255), hometeam)
                    graphics.DrawText(canvas, self.font, 4, 26, graphics.Color(255, 255, 255), awayteam)

                # BETTING ODDS
                homescore = game['homeTeam']['score']
                awayscore = game['awayTeam']['score']
                if game['gameStatus'] != 1:
                    if spread != "":
                        if ((homescore-awayscore) >= float(spread)*(-1)):
                            graphics.DrawText(canvas, self.font2, 177 - len(str(over_under))
                                              * 8, 21, graphics.Color(0, 0, 255), over_under)
                            graphics.DrawText(canvas, self.font2, 177 - len(str(spread))
                                              * 8, 51, graphics.Color(0, 0, 255), spread)
                        else:
                            away_spread = float(spread)*(-1)
                            graphics.DrawText(canvas, self.font2, 177 - len(str(over_under))
                                              * 8, 51, graphics.Color(0, 0, 255), over_under)
                            graphics.DrawText(canvas, self.font2, 177 - len(str(away_spread))
                                              * 8, 21, graphics.Color(0, 0, 255), str(away_spread))
                    else:
                        graphics.DrawText(canvas, self.font2, 177 - len(str(over_under))
                                          * 8, 21, graphics.Color(0, 0, 255), over_under)
                        graphics.DrawText(canvas, self.font2, 177 - len(str(spread))
                                          * 8, 51, graphics.Color(0, 0, 255), spread)

                    for line in range(31, 61):
                        graphics.DrawLine(canvas, 65, line, 129,
                                          line, graphics.Color(255, 255, 255))
                    for line in range(0, 30):
                        graphics.DrawLine(canvas, 65, line, 129,
                                          line, graphics.Color(255, 255, 255))
                    # NBA Logo
                    for line in range(55+y_offset_stats, 80+y_offset_stats):
                        graphics.DrawLine(canvas, 178+x_offset_stats, line,
                                          188+x_offset_stats, line, graphics.Color(0, 0, 255))
                        graphics.DrawLine(canvas, 188+x_offset_stats, line,
                                          188+x_offset_stats, line, graphics.Color(255, 0, 0))
                    for line in range(55+y_offset_stats, 76+y_offset_stats):
                        graphics.DrawLine(canvas, 185+x_offset_stats, line,
                                          187+x_offset_stats, line, graphics.Color(255, 0, 0))
                    for line in range(63+y_offset_stats, 66+y_offset_stats):
                        graphics.DrawLine(canvas, 178+x_offset_stats, line,
                                          178+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(60+y_offset_stats, 69+y_offset_stats):
                        graphics.DrawLine(canvas, 179+x_offset_stats, line,
                                          179+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(59+y_offset_stats, 71+y_offset_stats):
                        graphics.DrawLine(canvas, 180+x_offset_stats, line,
                                          180+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(59+y_offset_stats, 72+y_offset_stats):
                        graphics.DrawLine(canvas, 181+x_offset_stats, line,
                                          181+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(58+y_offset_stats, 73+y_offset_stats):
                        graphics.DrawLine(canvas, 182+x_offset_stats, line,
                                          182+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(55+y_offset_stats, 74+y_offset_stats):
                        graphics.DrawLine(canvas, 183+x_offset_stats, line,
                                          183+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(55+y_offset_stats, 64+y_offset_stats):
                        graphics.DrawLine(canvas, 184+x_offset_stats, line,
                                          184+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(64+y_offset_stats, 66+y_offset_stats):
                        graphics.DrawLine(canvas, 184+x_offset_stats, line,
                                          184+x_offset_stats, line, graphics.Color(255, 0, 0))
                    for line in range(66+y_offset_stats, 75+y_offset_stats):
                        graphics.DrawLine(canvas, 184+x_offset_stats, line,
                                          184+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(59+y_offset_stats, 64+y_offset_stats):
                        graphics.DrawLine(canvas, 185+x_offset_stats, line,
                                          185+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(71+y_offset_stats, 77+y_offset_stats):
                        graphics.DrawLine(canvas, 185+x_offset_stats, line,
                                          185+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(72+y_offset_stats, 78+y_offset_stats):
                        graphics.DrawLine(canvas, 186+x_offset_stats, line,
                                          186+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(60+y_offset_stats, 66+y_offset_stats):
                        graphics.DrawLine(canvas, 186+x_offset_stats, line,
                                          186+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(67+y_offset_stats, 70+y_offset_stats):
                        graphics.DrawLine(canvas, 186+x_offset_stats, line,
                                          186+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(63+y_offset_stats, 70+y_offset_stats):
                        graphics.DrawLine(canvas, 187+x_offset_stats, line,
                                          187+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(75+y_offset_stats, 80+y_offset_stats):
                        graphics.DrawLine(canvas, 187+x_offset_stats, line,
                                          187+x_offset_stats, line, graphics.Color(255, 255, 255))
                    for line in range(67+y_offset_stats, 70+y_offset_stats):
                        graphics.DrawLine(canvas, 188+x_offset_stats, line,
                                          188+x_offset_stats, line, graphics.Color(255, 255, 255))

                else:
                    graphics.DrawText(canvas, self.font2, 177 - len(str(over_under))
                                      * 8, 21, graphics.Color(0, 0, 255), over_under)
                    graphics.DrawText(canvas, self.font2, 177 - len(str(spread))
                                      * 8, 51, graphics.Color(0, 0, 255), spread)

                timeremaining = game['gameStatusText']
                if timeremaining[0] == 'Q' and timeremaining[3] == '0':
                    timeremaining = timeremaining[:3] + timeremaining[4:]
                    if timeremaining[0] == 'Q' and timeremaining[3] == '0':
                        timeremaining = timeremaining[:3] + timeremaining[4:]
                if timeremaining[1] == '1':
                    timeremaining = '1ST' + timeremaining[2:]
                if timeremaining[1] == '2':
                    timeremaining = '2ND' + timeremaining[2:]
                if timeremaining[1] == '3':
                    timeremaining = '3RD' + timeremaining[2:]
                if timeremaining[1] == '4':
                    timeremaining = '4TH' + timeremaining[2:]
                if timeremaining[1] == '5':
                    timeremaining = 'OT' + timeremaining[2:]
                if timeremaining[1] == '6':
                    timeremaining = 'OT2' + timeremaining[2:]
                if timeremaining[1] == '7':
                    timeremaining = 'OT3' + timeremaining[2:]
                if timeremaining[1] == '8':
                    timeremaining = 'OT4' + timeremaining[2:]
                if timeremaining == 'Half':
                    timeremaining = 'HALFTIME'

                timeremaining = timeremaining.upper()

                if game['gameStatus'] == 2:  # GAME IS LIVE
                    graphics.DrawText(canvas, self.font, 126 - len(str(awayscore))
                                      * 19, 26, graphics.Color(0, 0, 0), str(awayscore))
                    graphics.DrawText(canvas, self.font, 126 - len(str(homescore))
                                      * 19, 57, graphics.Color(0, 0, 0), str(homescore))
                    # Q4 or OT < 5min remaining
                    if (game['gameStatusText'][0] == 'Q' and game['gameStatusText'][1] >= '4') and (game['gameStatusText'][3] == '0' and game['gameStatusText'][4] <= '4'):
                        if homescore > awayscore:
                            if (homescore - awayscore) <= 10:  # close game
                                graphics.DrawText(canvas, self.font3, 4, 79, graphics.Color(
                                    255, 255, 255), timeremaining)  # bright quarter and time remaining
                                for line in range(82, 84):
                                    graphics.DrawLine(canvas, 0, line, 191, line, graphics.Color(
                                        255, 0, 0))  # red line at bottom of screen
                            else:
                                graphics.DrawText(canvas, self.font3, 4, 80, graphics.Color(
                                    200, 200, 200), timeremaining)
                        else:
                            if (awayscore - homescore) <= 10:  # close game
                                graphics.DrawText(canvas, self.font3, 4, 79, graphics.Color(
                                    255, 255, 255), timeremaining)  # bright quarter and time remaining
                                for line in range(82, 84):
                                    graphics.DrawLine(canvas, 0, line, 191, line, graphics.Color(
                                        255, 0, 0))  # red line at bottom of screen
                            else:
                                graphics.DrawText(canvas, self.font3, 4, 80, graphics.Color(
                                    200, 200, 200), timeremaining)
                    else:  # not a close game or not under 4min
                        graphics.DrawText(canvas, self.font3, 4, 80, graphics.Color(
                            200, 200, 200), timeremaining)  # 2

                if game['gameStatus'] == 3:  # GAME IS FINISHED
                    if homescore < awayscore:
                        for line in range(31, 61):
                            graphics.DrawLine(
                                canvas, 65, line, 129, line, graphics.Color(75, 75, 75))
                    else:
                        for line in range(0, 30):
                            graphics.DrawLine(
                                canvas, 65, line, 129, line, graphics.Color(75, 75, 75))

                    graphics.DrawText(canvas, self.font3, 4, 80, graphics.Color(
                        200, 200, 200), game['gameStatusText'].upper())  # 56

                    graphics.DrawText(canvas, self.font, 126 - len(str(awayscore))
                                      * 19, 26, graphics.Color(0, 0, 0), str(awayscore))
                    graphics.DrawText(canvas, self.font, 126 - len(str(homescore))
                                      * 19, 57, graphics.Color(0, 0, 0), str(homescore))

                if game['gameStatus'] == 1:  # GAME IS UPCOMING
                    awayrecord = str(game['awayTeam']['wins']) + \
                        '-' + str(game['awayTeam']['losses'])
                    homerecord = str(game['homeTeam']['wins']) + \
                        '-' + str(game['homeTeam']['losses'])
                    graphics.DrawText(canvas, self.font2, 71, 21, graphics.Color(
                        200, 200, 200), awayrecord)  # away team record
                    graphics.DrawText(canvas, self.font2, 71, 51, graphics.Color(
                        200, 200, 200), homerecord)  # home team record
                    if game['gameStatusText'] != 'PPD':  # upcoming game
                        graphics.DrawText(canvas, self.font3, 4, 86, graphics.Color(
                            200, 200, 200), game['gameStatusText'][0:game['gameStatusText'].find('ET')].upper() + 'ET')
                    if game['gameStatusText'] == 'PPD':  # postponed game
                        graphics.DrawText(canvas, self.font3, 4, 86, graphics.Color(
                            200, 200, 200), 'POSTPONED')

                    # NBA Logo
                    for line in range(55+y_offset_no_stats, 80+y_offset_no_stats):
                        graphics.DrawLine(canvas, 178+x_offset_no_stats, line,
                                          188+x_offset_no_stats, line, graphics.Color(0, 0, 255))
                        graphics.DrawLine(canvas, 188+x_offset_no_stats, line,
                                          188+x_offset_no_stats, line, graphics.Color(255, 0, 0))
                    for line in range(55+y_offset_no_stats, 76+y_offset_no_stats):
                        graphics.DrawLine(canvas, 185+x_offset_no_stats, line,
                                          187+x_offset_no_stats, line, graphics.Color(255, 0, 0))
                    for line in range(63+y_offset_no_stats, 66+y_offset_no_stats):
                        graphics.DrawLine(canvas, 178+x_offset_no_stats, line,
                                          178+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(60+y_offset_no_stats, 69+y_offset_no_stats):
                        graphics.DrawLine(canvas, 179+x_offset_no_stats, line,
                                          179+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(59+y_offset_no_stats, 71+y_offset_no_stats):
                        graphics.DrawLine(canvas, 180+x_offset_no_stats, line,
                                          180+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(59+y_offset_no_stats, 72+y_offset_no_stats):
                        graphics.DrawLine(canvas, 181+x_offset_no_stats, line,
                                          181+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(58+y_offset_no_stats, 73+y_offset_no_stats):
                        graphics.DrawLine(canvas, 182+x_offset_no_stats, line,
                                          182+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(55+y_offset_no_stats, 74+y_offset_no_stats):
                        graphics.DrawLine(canvas, 183+x_offset_no_stats, line,
                                          183+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(55+y_offset_no_stats, 64+y_offset_no_stats):
                        graphics.DrawLine(canvas, 184+x_offset_no_stats, line,
                                          184+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(64+y_offset_no_stats, 66+y_offset_no_stats):
                        graphics.DrawLine(canvas, 184+x_offset_no_stats, line,
                                          184+x_offset_no_stats, line, graphics.Color(255, 0, 0))
                    for line in range(66+y_offset_no_stats, 75+y_offset_no_stats):
                        graphics.DrawLine(canvas, 184+x_offset_no_stats, line,
                                          184+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(59+y_offset_no_stats, 64+y_offset_no_stats):
                        graphics.DrawLine(canvas, 185+x_offset_no_stats, line,
                                          185+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(71+y_offset_no_stats, 77+y_offset_no_stats):
                        graphics.DrawLine(canvas, 185+x_offset_no_stats, line,
                                          185+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(72+y_offset_no_stats, 78+y_offset_no_stats):
                        graphics.DrawLine(canvas, 186+x_offset_no_stats, line,
                                          186+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(60+y_offset_no_stats, 66+y_offset_no_stats):
                        graphics.DrawLine(canvas, 186+x_offset_no_stats, line,
                                          186+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(67+y_offset_no_stats, 70+y_offset_no_stats):
                        graphics.DrawLine(canvas, 186+x_offset_no_stats, line,
                                          186+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(63+y_offset_no_stats, 70+y_offset_no_stats):
                        graphics.DrawLine(canvas, 187+x_offset_no_stats, line,
                                          187+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(75+y_offset_no_stats, 80+y_offset_no_stats):
                        graphics.DrawLine(canvas, 187+x_offset_no_stats, line,
                                          187+x_offset_no_stats, line, graphics.Color(255, 255, 255))
                    for line in range(67+y_offset_no_stats, 70+y_offset_no_stats):
                        graphics.DrawLine(canvas, 188+x_offset_no_stats, line,
                                          188+x_offset_no_stats, line, graphics.Color(255, 255, 255))

                homeleadername = game['gameLeaders']['homeLeaders']['name']
                awayleadername = game['gameLeaders']['awayLeaders']['name']

                if game['gameStatus'] != 1 and homeleadername is not None and awayleadername is not None:
                    homeleaderpoints = game['gameLeaders']['homeLeaders']['points']
                    homeleaderrebounds = game['gameLeaders']['homeLeaders']['rebounds']
                    homeleaderassists = game['gameLeaders']['homeLeaders']['assists']

                    def findhomelastname(homeleadername, n):
                        # Using ' ' as a separator, All_words is a list of all the words in the String
                        All_words = homeleadername.split(" ")
                        return All_words[n - 1]
                    homeleaderlastname = findhomelastname(homeleadername, 2)
                    homestatline = homeleadername[0] + '.' + str(homeleaderlastname) + ' ' + str(
                        homeleaderpoints) + '-' + str(homeleaderrebounds) + '-' + str(homeleaderassists)
                    awayleaderpoints = game['gameLeaders']['awayLeaders']['points']
                    awayleaderrebounds = game['gameLeaders']['awayLeaders']['rebounds']
                    awayleaderassists = game['gameLeaders']['awayLeaders']['assists']

                    def findawaylastname(awayleadername, n):
                        # Using ' ' as a separator, All_words is a list of all the words in the String
                        All_words2 = awayleadername.split(" ")
                        return All_words2[n - 1]
                    awayleaderlastname = findawaylastname(awayleadername, 2)
                    awaystatline = awayleadername[0] + '.' + str(awayleaderlastname) + ' ' + str(
                        awayleaderpoints) + '-' + str(awayleaderrebounds) + '-' + str(awayleaderassists)

                    for line in range(84, 96):  # statline background
                        graphics.DrawLine(canvas, 0, line, 191,
                                          line, graphics.Color(255, 255, 255))

                    len1 = graphics.DrawText(canvas, self.font4, posx, 95, graphics.Color(
                        0, 0, 0), awaystatline.upper() + '  ' + homestatline.upper())
                    if len1 <= canvas.width:
                        break
                    else:
                        posx -= 1
                        if (posx == canvas.width - len1 - 2):
                            break
                        time.sleep(0.06)
                        canvas = matrix.SwapOnVSync(canvas)
                else:
                    break

            if (posx == canvas.width - len1 - 2):
                time.sleep(2)
                canvas = matrix.SwapOnVSync(canvas)
            else:
                canvas = matrix.SwapOnVSync(canvas)
                time.sleep(5)


if __name__ == '__main__':
    while True:
        Render().Render_Games()
