'''
Description:
    - Plotting functions for 
    
TODO:
    - Cleanup
'''

import itertools
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

sys.path.insert(1, '../NBAFinancial')
import utils


def createTeamsCurrentCapPlot(season, teamsCurrentSalaryData, salayCapMin, luxuryTax, league_avg):

    ax = teamsCurrentSalaryData.plot(figsize=(10, 8), y=season, kind='bar', legend=None)

    ax.set_title("Teams Salary Cap: {} Season".format(season))
    ax.set_xlabel("Teams")
    ax.set_ylabel("Salary")
    ax.set_xticklabels(teamsCurrentSalaryData['Team'])
    plt.xticks(rotation=80)

    ax.set_ylim(ymin=100000000)
    ax.set_ylim(ymax=140000000)

    formatYAxisToCurrency(ax)

    # Format Axis Values Sizing
    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=7)

    textIncrement = 400000
    data_size = len(teamsCurrentSalaryData) - 0.55
    
    addTextWithLine(plt, ax, teamsCurrentSalaryData, 'Cap Minimum', salayCapMin,
                    linestyle='--', color='k')
    addTextWithLine(plt, ax, teamsCurrentSalaryData, 'League Average', league_avg,
                    linestyle=':', color='r')
    addTextWithLine(plt, ax, teamsCurrentSalaryData, 'Luxury Tax', luxuryTax,
                    linestyle='-.', color='m')

    plt.show()


def createCompareSubplots(teams_to_contracts, seasons, teams):

    season_itr = itertools.cycle(seasons)
    team_itr   = itertools.cycle(teams)

    fig, ax = plt.subplots(nrows=1, ncols=2, constrained_layout=True)
    fig.suptitle('Salary Cap Comparison', fontsize=12)

    for row in range(0, 1):
        for col in range(0, 2):
            salay_year = next(season_itr)
            team       = next(team_itr)

            contracts, players = zip(*sorted(zip(teams_to_contracts[team].seasons[salay_year].contracts, teams_to_contracts[team].seasons[salay_year].players), reverse=True))

            ax[col].pie(x=contracts, 
                        startangle=75,
                        labels=players,
                        rotatelabels = 25,
                        labeldistance=1.0,
                        textprops={'fontsize': 6},
                        autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                        shadow=False)

            ax[col].legend(loc = 'best', 
                           prop={'size': 6},
                           bbox_to_anchor=(1.05, 1),
                           borderaxespad=0,
                           labels=['%s - ${0:,.0f}'.format(s) % (l) for l, s in zip(players, contracts)])

            ax[col].set_title(team + ': ' + salay_year)

    plt.show()


def createLinePlot(teams_to_contracts, teams):

    players_to_contracts = dict()
    for team in teams:

        convertContracts(players_to_contracts, teams_to_contracts, team)

        fig, ax = plt.subplots()
        for player, contracts in players_to_contracts.items():
            plt.plot(getFutureSeasons(2019, 20)[1:len(contracts)+1], contracts, marker='', linewidth=2, alpha=0.9, label=player)

        ax.set_ylim(ymin=0)
        start, end = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(start, end, step=1000000))

        # Format Y-Axis Ticks to Display Currency ($)
        ax.set_yticks(list(ax.get_yticks()))
        a = ax.get_yticks().tolist()
        a = ['${0:,.0f}'.format(int(val)) for val in a]
        ax.set_yticklabels(a)

        plt.title("{}".format(team), fontsize=14)
        plt.xlabel("Season")
        plt.ylabel("Salary")

        plt.legend(loc='best')
        plt.grid(True)
        plt.show()


def createIndividualYearPlot(teams_to_contracts, seasons, teams):

    salay_year = seasons.pop(0)

    for team in teams:
        contracts, players = zip(*sorted(zip(teams_to_contracts[team].seasons[salay_year].contracts, teams_to_contracts[team].seasons[salay_year].players),
                                 reverse=True))

        fig, ax, junk = plt.pie(x=contracts,
                                startangle=75,
                                labels=players,
                                rotatelabels = 25,
                                labeldistance=1.0,
                                textprops={'fontsize': 7},
                                autopct='%1.1f%%',
                                shadow=False)

        plt.suptitle('Salary Cap Player Breakdown: {}'.format(team))
        plt.title('{}'.format(salay_year), fontsize=12)

        plt.legend(loc = 'best', 
                   prop={'size': 8},
                   bbox_to_anchor=(1.05, 1),
                   borderaxespad=0,
                   labels=['%s - ${0:,.0f}'.format(s) % (l) for l, s in zip(players, contracts)])

        plt.show()


def createMultiYearSubplots(teams_to_contracts, seasons, teams):

    season_itr = itertools.cycle(seasons)

    for team in teams:
        fig, ax = plt.subplots(nrows=3, ncols=3, constrained_layout=True)
        fig.suptitle('Salary Cap Player Breakdown - {}'.format(team), fontsize=12)

        for row in range(0, 3):
            for col in range(0, 3):

                if (row == 0) and (col == 1):
                    salay_year = next(season_itr)
                    ax[row, col].pie(x=teams_to_contracts[team].seasons[salay_year].contracts, 
                                     startangle=200,
                                     labels=teams_to_contracts[team].seasons[salay_year].players,
                                     rotatelabels = 25,
                                     labeldistance=1.0,
                                     textprops={'fontsize': 5},
                                     autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                                     shadow=False)[0]
                    ax[row, col].set_title(salay_year)
                elif (row != 0):
                    salay_year = next(season_itr)
                    ax[row, col].pie(x=teams_to_contracts[team].seasons[salay_year].contracts, 
                                     startangle=200,
                                     labels=teams_to_contracts[team].seasons[salay_year].players,
                                     rotatelabels = 25,
                                     labeldistance=1.0,
                                     textprops={'fontsize': 5},
                                     autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                                     shadow=False)[0]
                    ax[row, col].set_title(salay_year)
                else:
                    ax[row, col].axis('off')

        plt.show()



# TODO: MOVE TO SEPERATE UTILS FILE
def convertContracts(players_to_contracts, teams_to_contracts, team):

    players_to_contracts.clear()
    teams_to_contracts[team].seasons.pop("Guaranteed")

    for season in teams_to_contracts[team].seasons.values():

        if not any([season.contracts.empty, season.players.empty]):
            contracts, players = zip(*sorted(zip(season.contracts, season.players), reverse=True))

        for player, contract in zip(np.array(players), np.array(contracts)): 

            if player not in players_to_contracts.keys():
                players_to_contracts[player] = list()
            players_to_contracts[player].append(contract)


def addTextWithLine(plt, ax, data_df, text, value, linestyle, color):
    textIncrement = 400000
    data_size = len(data_df) - 0.55

    plt.axhline(y=value, linestyle=linestyle, linewidth=1, color=color)
    ax.text(data_size, int(value) + textIncrement, 
            '{} - ${:,.0f}'.format(text, int(value)),
            fontsize = 7,
            horizontalalignment="right")

def formatYAxisToCurrency(ax):
    ax.set_yticks(list(ax.get_yticks()))
    a = ax.get_yticks().tolist()
    a = ['${0:,.0f}'.format(int(val)) for val in a]
    ax.set_yticklabels(a)
