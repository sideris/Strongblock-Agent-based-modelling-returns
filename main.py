from agent import Agent
from market import Market
from strategy import UpfrontInvestStrategy, SellWhenPriceMoonsStrategy, BuildNodesUntilLimitStrategy, \
    CoinFlipperStrategy

if __name__ == '__main__':
    days = 400
    print(f'Starting simulation for {days} days')
    market = Market()
    a1 = Agent(name='upfront_investor')
    a2 = Agent(name='upfront_investor_30', node_goal=30)
    a3 = Agent(name='upfront_investor_max', node_goal=200)
    a4 = Agent(name='moon_seller')
    a5 = Agent(name='moon_seller_30', node_goal=30)
    a6 = Agent(name='node_builder')
    a7 = Agent(name='node_builder_30', node_goal=30)
    a8 = Agent(name='node_builder_max', node_goal=200)
    a9 = Agent(name='coin_flipper')
    a10 = Agent(name='coin_flipper_30', node_goal=30)

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
    strategies = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    for i in range(1, days + 1):
        for s in strategies:
            s.agent.tick()
            s.post_agent_tick()
            market.tick()
