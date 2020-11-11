'''
Description:
    - Plotting functions for NBATrade

TODO:
    - Cleanup
'''


import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
sys.path.insert(1, '../NBAFinancial')
import utils


def createCompareTradeSubplots(before_teams_to_contracts, after_teams_to_contracts):

    # Get list of teams listed in trade
    teams = set(before_teams_to_contracts.keys()) & set(after_teams_to_contracts.keys())
    team_itr = itertools.cycle(teams)

    fig, big_axes = plt.subplots( figsize=(15.0, 15.0) , nrows=len(teams), ncols=2, sharey=True) 
    fig.suptitle('Trade Recap', fontsize=12)

    labels = ["Before", "After"]
    for ax, col in zip(big_axes[0], labels):
        ax.set_title(col)

    for ax, col in zip(big_axes[:,1], teams):
        turnOffTickMarks(ax)

    for ax, team in zip(big_axes[:,0], teams):
        turnOffTickMarks(ax)
        ax.set_ylabel(team, rotation=0, size='large')

    plot_count = 1
    for row in range(0, len(teams)):
        team = next(team_itr)
        for col in range(0, 2):

            if col == 0:
                players_to_contracts = {player: contract[0] for player, contract in sorted(before_teams_to_contracts[team].players.items(), key=lambda item: item[1], reverse=True)}
                tradedPlayers = set(before_teams_to_contracts[team].players.keys()).difference(set(after_teams_to_contracts[team].players.keys()))

            else:
                players_to_contracts = {player: contract[0] for player, contract in sorted(after_teams_to_contracts[team].players.items(), key=lambda item: item[1], reverse=True)}
                tradedPlayers = set(after_teams_to_contracts[team].players.keys()).difference(set(before_teams_to_contracts[team].players.keys()))

            ax = fig.add_subplot(len(teams), 2, plot_count)
            ax.pie(x=np.fromiter(players_to_contracts.values(), dtype=int),
                   startangle=75,
                   labels=players_to_contracts.keys(),
                   rotatelabels = 25,
                   labeldistance=1.0,
                   textprops={'fontsize': 6},
                   autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                   shadow=False)
            leg = ax.legend(loc = 'right', 
                            prop={'size': 7.5},
                            bbox_to_anchor=(1.70, 0.5),
                            borderaxespad=1,
                            labels=['%s - ${0:,.0f}'.format(s) % (l) for l, s in zip(players_to_contracts.keys(), players_to_contracts.values())])

            # Format traded players name in legend
            for text in leg.get_texts():
                res = [ele for ele in tradedPlayers if(ele in text.get_text())] 
                if res:
                    text.set_fontweight("semibold")
                    text.set_color("blue")

            plot_count += 1

    plt.show()


# TODO: Cool project would be to see how to place player's face above bar
def createInfoBarPlot(before_teams_to_contracts, after_teams_to_contracts, season):

    # Get list of teams listed in trade
    teams    = set(before_teams_to_contracts.keys()) & set(after_teams_to_contracts.keys())
    team_itr = itertools.cycle(teams)

    bar_width = 0.40

    fig, ax = plt.subplots()

    players_to_contracts = dict()

    # FIXME: Cleanup lines 324-367
    sorted_players_to_contracts1 = {player: contract[0] for player, contract in sorted(after_teams_to_contracts[next(team_itr)].players.items(), key=lambda item: item[1], reverse=True)}

    players_to_contracts.update(sorted_players_to_contracts1)
    ind1 = np.arange(len(sorted_players_to_contracts1.keys()))
    bar1 = ax.bar(ind1,
                  sorted_players_to_contracts1.values(),
                  bar_width)

    sorted_players_to_contracts2 = {player: contract[0] for player, contract in sorted(after_teams_to_contracts[next(team_itr)].players.items(), key=lambda item: item[1], reverse=True)}
    players_to_contracts.update(sorted_players_to_contracts2)
    ind2 = np.arange(len(sorted_players_to_contracts2.keys()))
    bar2 = ax.bar(ind2 + bar_width,
                  sorted_players_to_contracts2.values(),
                  bar_width)

    # Add contract above each team's player
    for rect in bar1 + bar2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, rect.get_height(),
                    '${0:,.0f}'.format(int(height)),
                    fontsize=7,
                    ha='center', va='bottom')

    # Labels
    ax.set_title("New Roster Salary Breakdown: {}".format(season))
    ax.set_xlabel("Players")
    ax.set_ylabel("Salary ($)")
    ax.legend((bar1[0], bar2[0]), (next(team_itr), next(team_itr)))

    formatYAxisToCurrency(ax)

    # Format X-Axis Labels to Display Players
    ax.set_xticks(ind1,minor=False)
    ax.set_xticks(ind2 + bar_width,minor=True)
    ax.set_xticklabels(sorted_players_to_contracts1.keys(), rotation=90, minor=False,ha='center', fontdict={'fontsize':7})
    ax.set_xticklabels(sorted_players_to_contracts2.keys(), rotation=90, minor=True, ha='center', fontdict={'fontsize':7})

    plt.grid(True)
    plt.show()


def createLinePlot(teams_to_contracts):

    for team in teams_to_contracts.keys():

        fig, ax = plt.subplots()

        for player, contracts in sorted(teams_to_contracts[team].players.items(), key=lambda x: x[1], reverse=True):
            plt.plot(utils.getFutureSeasons(2020, 21)[1:len(contracts)+1], contracts, marker='', linewidth=2, alpha=0.9, label=player)

        ax.set_ylim(ymin=0)
        start, end = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(start, end, step=1000000))

        formatYAxisToCurrency(ax)

        plt.title("{}".format(team), fontsize=14)
        plt.xlabel("Season")
        plt.ylabel("Salary")

        plt.legend(loc='best')
        plt.grid(True)
        plt.show()

        plt.show()


# TODO: MOVE TO SEPERATE UTILS FILE
def formatYAxisToCurrency(ax):
    ax.set_yticks(list(ax.get_yticks()))
    a = ax.get_yticks().tolist()
    a = ['${0:,.0f}'.format(int(val)) for val in a]
    ax.set_yticklabels(a)

def turnOffTickMarks(ax):
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    ax.set_frame_on(False)