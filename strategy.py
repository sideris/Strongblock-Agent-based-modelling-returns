import random

from agent import Agent
from constants import RATIONAL_NUMBER_OF_ACC_STRONG_TO_SELL, STRONG_TO_NODE
from market import Market


class Strategy:
    def __init__(self, agent: Agent, market: Market, start_nodes=1):
        self.agent = agent
        self.market = market
        self.start_nodes = start_nodes

    def start_agent(self):
        """ Buy 1 node """
        self.agent.buy_strong_and_add_nodes(
            self.market.get_current_price(),
            self.start_nodes
        )

    def post_agent_tick(self):
        raise Exception


class UpfrontInvestStrategy(Strategy):
    def start_agent(self):
        """ Buy all nodes upfront """
        self.agent.buy_strong_and_add_nodes(
            self.market.get_current_price(),
            self.agent.node_goal
        )

    def post_agent_tick(self):
        """ Just sell when you reach a good number """
        if self.agent.total_strong_accum >= RATIONAL_NUMBER_OF_ACC_STRONG_TO_SELL:
            self.agent.claim_and_sell(self.market.get_current_price())
        self.agent.prepare_next_tick()


class BuildNodesUntilLimitStrategy(Strategy):
    def post_agent_tick(self):
        """ Just sell when you reach after you collected all nodes else create a node """
        if self.agent.nodes <= self.agent.node_goal:
            self.agent.create_node()
        if self.agent.total_strong_accum >= RATIONAL_NUMBER_OF_ACC_STRONG_TO_SELL:
            self.agent.claim_and_sell(self.market.get_current_price())
        self.agent.prepare_next_tick()


class SellWhenPriceMoonsStrategy(Strategy):
    def __init__(self, agent: Agent, market: Market, start_nodes=1, pc_increase=10):
        super().__init__(agent, market, start_nodes)
        self.previous_price = 0
        self.pc_increase = pc_increase

    def start_agent(self):
        super().start_agent()
        self.previous_price = self.market.get_current_price()

    def post_agent_tick(self):
        """ Check price and if it has increased by % sell, else add a node """
        sell_price = ((100 + self.pc_increase) / 100) * self.previous_price
        will_try_add = self.market.get_current_price() < sell_price
        if self.agent.nodes <= self.agent.node_goal and will_try_add:
            added = self.agent.create_node()
            if added:
                self.previous_price = self.market.get_current_price()
        if self.agent.total_strong_accum >= RATIONAL_NUMBER_OF_ACC_STRONG_TO_SELL:
            self.agent.claim_and_sell(self.market.get_current_price())
        self.agent.prepare_next_tick()


class CoinFlipperStrategy(Strategy):
    def post_agent_tick(self):
        """ Flip a coin and decide if add or sell if enough strong """
        if self.agent.total_strong_accum >= STRONG_TO_NODE:
            coin = random.randint(0, 1)
            if coin == 0:
                self.agent.claim_and_sell(self.market.get_current_price())
            else:
                self.agent.create_node()
        self.agent.prepare_next_tick()
