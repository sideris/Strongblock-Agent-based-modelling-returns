import random

from agent import Agent
from constants import RATIONAL_NUMBER_OF_ACC_STRONG_TO_SELL, STRONG_TO_NODE, CLAIM_COST_WITH_GAS, SELL_STRONG_COST_GAS
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
    def __init__(self, agent: Agent, market: Market, start_nodes=1, pc_increase=15):
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


class SectionSellerBuilderStrategy(Strategy):
    def __init__(self, agent: Agent, market: Market, start_nodes=1, sections=3):
        super().__init__(agent, market, start_nodes)
        self.previous_price = 0
        self.cost = 0
        self.total_added = 0
        self.sections = sections
        self.remaining = self.agent.node_goal // sections

    def post_agent_tick(self):
        """ Buy until node_goal/section reached then sell until recoup costs """
        if self.remaining > 0 and self.total_added < self.agent.node_goal:
            created = self.agent.create_node()
            if created:
                self.cost += self.market.get_current_price() * STRONG_TO_NODE
                self.remaining -= 1
                self.total_added += 1
        elif self.remaining == 0 and self.cost >= 0 and self.agent.total_strong_accum >= STRONG_TO_NODE:
            self.agent.claim_and_sell(self.market.get_current_price())
            self.cost += CLAIM_COST_WITH_GAS + SELL_STRONG_COST_GAS - self.agent.profit_sheet[-1]
            if self.cost < 0:
                self.remaining = self.agent.node_goal // self.sections
                if self.remaining > (self.agent.node_goal - self.total_added):
                    self.remaining = (self.agent.node_goal - self.total_added)
        else:
            if self.agent.total_strong_accum >= STRONG_TO_NODE:
                self.agent.claim_and_sell(self.market.get_current_price())
        self.agent.prepare_next_tick()


class BuilderSellerStrategy(Strategy):
    def __init__(self, agent: Agent, market: Market, start_nodes=1):
        super().__init__(agent, market, start_nodes)
        self.sell_next = False

    def post_agent_tick(self):
        """ Buy node and then sell """
        if self.agent.total_strong_accum >= STRONG_TO_NODE and not self.sell_next:
            self.agent.create_node()
            self.sell_next = True
        elif self.sell_next and self.agent.total_strong_accum >= RATIONAL_NUMBER_OF_ACC_STRONG_TO_SELL:
            self.agent.claim_and_sell(self.market.get_current_price())
        self.agent.prepare_next_tick()
