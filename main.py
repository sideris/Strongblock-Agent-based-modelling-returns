import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from agent import Agent
from market import Market
from strategy import UpfrontInvestStrategy, SellWhenPriceMoonsStrategy, BuildNodesUntilLimitStrategy, \
    CoinFlipperStrategy, SectionSellerBuilderStrategy, BuilderSellerStrategy


def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


if __name__ == '__main__':
    days = 720
    print(f'Starting simulation for {days} days')
    market = Market(500)
    a1 = Agent(name='upfront_investor_10')
    a2 = Agent(name='upfront_investor_30', node_goal=30)
    a3 = Agent(name='upfront_investor_max', node_goal=200)
    a4 = Agent(name='moon_seller_10')
    a5 = Agent(name='moon_seller_30', node_goal=30)
    a6_1 = Agent(name='node_builder_3', node_goal=3)
    a6 = Agent(name='node_builder_10')
    a7 = Agent(name='node_builder_30', node_goal=30)
    a8 = Agent(name='node_builder_max', node_goal=200)
    a9 = Agent(name='coin_flipper_10')
    a10 = Agent(name='coin_flipper_30', node_goal=30)
    a11 = Agent(name='section_seller_30', node_goal=30)
    a12 = Agent(name='builder_then_seller_10')
    a13 = Agent(name='builder_then_seller_30', node_goal=30)

    s1 = UpfrontInvestStrategy(a1, market)
    s2 = UpfrontInvestStrategy(a2, market)
    s3 = UpfrontInvestStrategy(a3, market)
    s4 = SellWhenPriceMoonsStrategy(a4, market)
    s5 = SellWhenPriceMoonsStrategy(a5, market)
    s6 = BuildNodesUntilLimitStrategy(a6, market)
    s7 = BuildNodesUntilLimitStrategy(a7, market)
    s8 = BuildNodesUntilLimitStrategy(a8, market)
    s9 = CoinFlipperStrategy(a9, market)
    s10 = CoinFlipperStrategy(a10, market)
    s11 = CoinFlipperStrategy(a6_1, market)
    s12 = SectionSellerBuilderStrategy(a11, market)
    s13 = BuilderSellerStrategy(a12, market)
    s14 = BuilderSellerStrategy(a13, market)
    strategies = [
        # s1,
        # s2,
        # s3,
        # s4,
        s5,
        s6,
        s7,
        s8,
        s9,
        s10,
        s11,
        s12,
        s13,
        s14
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
