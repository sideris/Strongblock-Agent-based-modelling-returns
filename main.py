import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from agent import Agent
from market import Market
from strategy import UpfrontInvestStrategy, SellWhenPriceMoonsStrategy, BuildNodesUntilLimitStrategy, \
    CoinFlipperStrategy, SectionSellerBuilderStrategy, BuilderSellerStrategy
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--nodes', dest='nodes', default=10,
                    type=int,
                    help='Number of nodes for strategies')
parser.add_argument('--start_price', dest='start_price', default=400, type=int,
                    help='$STRONG start price')
parser.add_argument('--days', dest='days', default=365, type=int,
                    help='Number of days simulation runs')
args = parser.parse_args()


def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


if __name__ == '__main__':
    days = args.days
    print(f'Starting simulation for {days} days')
    market = Market(args.start_price)
    a1 = Agent(name='upfront_investor', node_goal=args.nodes)
    a4 = Agent(name='moon_seller', node_goal=args.nodes)
    a6_1 = Agent(name='node_builder', node_goal=args.nodes)
    a9 = Agent(name='coin_flipper', node_goal=args.nodes)
    a11 = Agent(name='section_seller', node_goal=args.nodes)
    a12 = Agent(name='builder_then_seller', node_goal=args.nodes)

    s1 = UpfrontInvestStrategy(a1, market)
    s4 = SellWhenPriceMoonsStrategy(a4, market)
    s6 = BuildNodesUntilLimitStrategy(a6_1, market)
    s9 = CoinFlipperStrategy(a9, market)
    s12 = SectionSellerBuilderStrategy(a11, market)
    s13 = BuilderSellerStrategy(a12, market)
    strategies = [
        # s1,
        s4,
        s6,
        s9,
        s12,
        s13,
    ]
    palette = plt.get_cmap('Set1')
    for s in strategies:
        s.agent.tick()
        s.start_agent()
    for day in range(1, days):
        for ind, s in enumerate(strategies):
            s.agent.tick()
            s.post_agent_tick()
            if day % 30 == 0:
                s.agent.pay_node_maintainance_fees()
        market.tick()
    fig, axs = plt.subplots(2, 2)
    dayseries = [i for i in range(1, days + 1)]
    for ind, s in enumerate(strategies):
        axs[0, 0].plot(dayseries[:-1],
                       s.agent.profit_sheet,
                       marker='',
                       color=palette(ind),
                       linewidth=1,
                       alpha=0.9,
                       label=s.agent.name)
    axs[0, 0].set_title('Profits')
    axs[0, 0].legend(loc="upper left")
    for ind, s in enumerate(strategies):
        axs[0, 1].plot(dayseries,
                       np.cumsum(s.agent.benefit_sheet),
                       marker='',
                       color=palette(ind),
                       linewidth=1,
                       alpha=0.9,
                       label=s.agent.name)
    axs[0, 1].set_title('Earnings')
    for ind, s in enumerate(strategies):
        axs[1, 0].plot(dayseries,
                       np.cumsum(s.agent.cost_sheet),
                       marker='',
                       color=palette(ind),
                       linewidth=1,
                       alpha=0.9,
                       label=s.agent.name)
    axs[1, 0].set_title('Costs')
    axs[1, 1].plot(dayseries, market.price_history)
    axs[1, 1].set_title('Strong price (sim)')
    formatter = FuncFormatter(human_format)
    plt.style.use('seaborn-darkgrid')
    axs[0, 0].yaxis.set_major_formatter(formatter)
    axs[0, 1].yaxis.set_major_formatter(formatter)
    axs[1, 0].yaxis.set_major_formatter(formatter)
    plt.xlabel("Days")
    plt.legend(loc=2, ncol=2)
    plt.show()
