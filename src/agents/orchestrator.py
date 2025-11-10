"""
Agent Orchestrator - Routes tasks to appropriate agents
"""
from typing import Any, Dict, List, Optional
from loguru import logger

from .base_agent import BaseAgent
from .etl_agent import ETLAgent
from .query_agent import QueryAgent
from .profiling_agent import ProfilingAgent
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_templates import PromptTemplates


class AgentOrchestrator:
    """Orchestrates multiple agents to handle complex workflows"""

    def __init__(self, llm_client: Optional[OllamaClient] = None):
        """
        Initialize orchestrator with agents

        Args:
            llm_client: Optional LLM client for query agent
        """
        self.llm_client = llm_client or OllamaClient()

        # Initialize all agents
        self.agents: List[BaseAgent] = [
            ETLAgent(),
            QueryAgent(self.llm_client),
            ProfilingAgent()
        ]

        self.context: Dict[str, Any] = {}
        logger.info(f"Initialized AgentOrchestrator with {len(self.agents)} agents")

    def route_task(self, task: Dict[str, Any]) -> Optional[BaseAgent]:
        """
        Route task to appropriate agent

        Args:
            task: Task to route

        Returns:
            Agent that can handle the task, or None
        """
        for agent in self.agents:
            if agent.can_handle(task):
                logger.info(f"Routing task to {agent.name}")
                return agent

        logger.warning(f"No agent found for task: {task.get('type', 'unknown')}")
        return None

    def execute_task(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a single task

        Args:
            task: Task to execute
            context: Optional execution context

        Returns:
            Execution result
        """
        agent = self.route_task(task)

        if not agent:
            return {
                "success": False,
                "data": None,
                "error": f"No agent available to handle task type: {task.get('type', 'unknown')}"
            }

        # Merge context
        execution_context = {**self.context, **(context or {})}

        result = agent.execute(task, execution_context)

        # Update shared context if task produced data
        if result.get("success") and result.get("data") is not None:
            self.context["df"] = result["data"]

        return result

    def execute_workflow(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute a sequence of tasks

        Args:
            tasks: List of tasks to execute in order

        Returns:
            List of execution results
        """
        results = []
        logger.info(f"Starting workflow with {len(tasks)} tasks")

        for i, task in enumerate(tasks, 1):
            logger.info(f"Executing task {i}/{len(tasks)}: {task.get('type', 'unknown')}")

            result = self.execute_task(task)
            results.append(result)

            # Stop workflow if task failed and it's marked as critical
            if not result["success"] and task.get("critical", False):
                logger.error(f"Critical task failed, stopping workflow: {result.get('error')}")
                break

        logger.success(f"Workflow completed: {len(results)} tasks executed")
        return results

    def parse_natural_language_workflow(self, user_request: str, model: str = "llama3") -> List[Dict[str, Any]]:
        """
        Parse natural language request into a workflow of tasks

        Args:
            user_request: User's natural language request
            model: LLM model to use

        Returns:
            List of tasks
        """
        available_agents = [agent.name for agent in self.agents]

        prompt = PromptTemplates.agent_routing_prompt(user_request, available_agents)

        try:
            response = self.llm_client.generate_structured_output(prompt, model=model)

            # Convert LLM response to task list
            tasks = []
            task_steps = response.get("task_breakdown", [])

            for step in task_steps:
                task = self._infer_task_from_step(step)
                if task:
                    tasks.append(task)

            logger.info(f"Parsed {len(tasks)} tasks from natural language request")
            return tasks

        except Exception as e:
            logger.error(f"Failed to parse workflow: {e}")
            # Fallback: create a simple query task
            return [{
                "type": "query",
                "description": user_request,
                "query": user_request
            }]

    def _infer_task_from_step(self, step: str) -> Optional[Dict[str, Any]]:
        """
        Infer task type from step description

        Args:
            step: Step description

        Returns:
            Task dictionary or None
        """
        step_lower = step.lower()

        if any(keyword in step_lower for keyword in ["load", "read", "import"]):
            return {"type": "etl", "operation": "load", "description": step}
        elif any(keyword in step_lower for keyword in ["filter", "select", "where"]):
            return {"type": "etl", "operation": "filter", "description": step}
        elif any(keyword in step_lower for keyword in ["save", "export", "write"]):
            return {"type": "etl", "operation": "save", "description": step}
        elif any(keyword in step_lower for keyword in ["profile", "report", "summary"]):
            return {"type": "profile", "description": step}
        elif any(keyword in step_lower for keyword in ["query", "find", "show", "get", "calculate"]):
            return {"type": "query", "description": step}
        else:
            return {"type": "query", "description": step}

    def get_agent_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all agents

        Returns:
            List of agent statistics
        """
        return [agent.get_stats() for agent in self.agents]

    def clear_context(self):
        """Clear shared context"""
        self.context.clear()
        logger.info("Context cleared")
