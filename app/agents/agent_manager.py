# app/agents/agent_manager.py
from app.agents.product_agent import ProductAgent
# from app.agents.cart_agent import CartAgent
# from app.agents.order_agent import OrderAgent


class AgentManager:
    """Central registry for all available agents."""

    def __init__(self):
        self.agents = {
            "product": ProductAgent(),
            # "cart": CartAgent(),
            # "order": OrderAgent(),
        }
        self.agent_map = self._build_agent_map()

    def _build_agent_map(self):
        """Flatten methods of all agents into a single callable map."""
        agent_map = {}
        for agent_name, agent_instance in self.agents.items():
            for attr in dir(agent_instance):
                if not attr.startswith("_") and callable(getattr(agent_instance, attr)):
                    agent_map[attr] = getattr(agent_instance, attr)
        return agent_map

    def get_agent_function(self, func_name: str):
        """Return a function reference by name."""
        return self.agent_map.get(func_name)
