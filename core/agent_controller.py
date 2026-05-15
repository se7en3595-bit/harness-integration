#!/usr/bin/env python3
"""
AI Agent Harness - 代理控制器

统一管理不同类型的AI代理，提供标准化的接口和生命周期管理。
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
from datetime import datetime
import uuid

# rich为可选依赖，未提供时使用标准输出
try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

class AgentType(Enum):
    """代理类型枚举"""
    TEXT_AGENT = "text_agent"
    BROWSER_AGENT = "browser_agent"
    SEARCH_AGENT = "search_agent"
    MULTIMODAL_AGENT = "multimodal_agent"

@dataclass
class AgentMetrics:
    """代理性能指标"""
    agent_id: str
    agent_type: AgentType
    execution_time: float = 0.0
    success_rate: float = 0.0
    accuracy_score: float = 0.0
    cost_per_execution: float = 0.0
    tokens_used: int = 0
    error_count: int = 0
    last_execution: datetime = field(default_factory=datetime.now)

@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    agent_id: str
    status: str  # "success", "failed", "timeout"
    result: Any = None
    error_message: str = ""
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class AgentInterface(ABC):
    """代理接口基类"""

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """执行任务"""
        pass

    @abstractmethod
    async def validate_response(self, response: Any, expected: Any) -> bool:
        """验证响应是否符合预期"""
        pass

    @abstractmethod
    async def get_metrics(self) -> AgentMetrics:
        """获取代理性能数据"""
        pass

class TextAgent(AgentInterface):
    """文本代理实现"""

    def __init__(self, agent_id: str, model: str = "claude-3-sonnet-20240229"):
        self.agent_id = agent_id
        self.model = model
        self.metrics = AgentMetrics(
            agent_id=agent_id,
            agent_type=AgentType.TEXT_AGENT
        )

    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        start_time = time.time()
        task_id = str(uuid.uuid4())

        try:
            # 模拟LLM调用
            prompt = task.get("prompt", "")
            system_prompt = task.get("system_prompt", "")

            # 这里应该集成实际的LLM API调用
            await asyncio.sleep(1)  # 模拟API延迟

            result = f"TextAgent Response to: {prompt[:50]}..."
            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="success",
                result=result,
                execution_time=execution_time,
                metadata={"model": self.model}
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="failed",
                error_message=str(e),
                execution_time=execution_time
            )

    async def validate_response(self, response: Any, expected: Any) -> bool:
        # 简化的验证逻辑
        return len(str(response)) > 0 if response else False

    async def get_metrics(self) -> AgentMetrics:
        return self.metrics

class BrowserAgent(AgentInterface):
    """浏览器代理实现"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.browser_profile = None
        self.metrics = AgentMetrics(
            agent_id=agent_id,
            agent_type=AgentType.BROWSER_AGENT
        )

    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        start_time = time.time()
        task_id = str(uuid.uuid4())

        try:
            url = task.get("url")
            actions = task.get("actions", [])

            # 模拟浏览器操作
            await asyncio.sleep(2)  # 模拟浏览器加载时间

            result = {
                "visited_urls": [url],
                "actions_performed": len(actions),
                "screenshots_taken": 1
            }

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="success",
                result=result,
                execution_time=execution_time,
                metadata={"actions": actions}
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="failed",
                error_message=str(e),
                execution_time=execution_time
            )

    async def validate_response(self, response: Any, expected: Any) -> bool:
        # 验证页面是否成功加载
        return isinstance(response, dict) and "visited_urls" in response

    async def get_metrics(self) -> AgentMetrics:
        return self.metrics

class SearchAgent(AgentInterface):
    """搜索代理实现"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.metrics = AgentMetrics(
            agent_id=agent_id,
            agent_type=AgentType.SEARCH_AGENT
        )

    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        start_time = time.time()
        task_id = str(uuid.uuid4())

        try:
            query = task.get("query", "")
            search_engine = task.get("engine", "google")

            # 模拟搜索操作
            await asyncio.sleep(1.5)

            # 模拟搜索结果
            results = [
                {"title": f"Result {i} for '{query}'", "url": f"https://example{i}.com"}
                for i in range(5)
            ]

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="success",
                result=results,
                execution_time=execution_time,
                metadata={"engine": search_engine, "query": query}
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="failed",
                error_message=str(e),
                execution_time=execution_time
            )

    async def validate_response(self, response: Any, expected: Any) -> bool:
        return isinstance(response, list) and len(response) > 0

    async def get_metrics(self) -> AgentMetrics:
        return self.metrics

class AgentController:
    """代理控制器主类"""

    def __init__(self):
        self.agents: Dict[str, AgentInterface] = {}
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.task_queue: List[Dict[str, Any]] = []
        self.metrics_history: List[TaskResult] = []
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("AgentController")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def register_agent(self, agent_type: AgentType, agent_config: Dict[str, Any]) -> str:
        """注册新的代理实例"""
        agent_id = f"{agent_type.value}_{len(self.agents) + 1}"

        if agent_type == AgentType.TEXT_AGENT:
            agent = TextAgent(agent_id, agent_config.get("model", "claude-3-sonnet-20240229"))
        elif agent_type == AgentType.BROWSER_AGENT:
            agent = BrowserAgent(agent_id)
        elif agent_type == AgentType.SEARCH_AGENT:
            agent = SearchAgent(agent_id)
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")

        self.agents[agent_id] = agent
        self.logger.info(f"Registered agent: {agent_id} ({agent_type.value})")
        return agent_id

    def unregister_agent(self, agent_id: str) -> bool:
        """注销代理实例"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.logger.info(f"Unregistered agent: {agent_id}")
            return True
        return False

    async def submit_task(self, task: Dict[str, Any], agent_id: Optional[str] = None) -> str:
        """提交任务到队列"""
        task_id = str(uuid.uuid4())
        task_data = {
            "id": task_id,
            "payload": task,
            "submitted_at": datetime.now(),
            "agent_id": agent_id
        }

        self.task_queue.append(task_data)
        self.logger.info(f"Submitted task {task_id} (agent: {agent_id or 'any'})")

        return task_id

    async def execute_task(self, task_id: str, agent_id: str) -> TaskResult:
        """执行指定任务"""
        task_data = next((t for t in self.task_queue if t["id"] == task_id), None)
        if not task_data:
            return TaskResult(task_id, agent_id, "failed", error_message="Task not found")

        if agent_id not in self.agents:
            return TaskResult(task_id, agent_id, "failed", error_message=f"Agent {agent_id} not found")

        agent = self.agents[agent_id]

        try:
            result = await agent.execute_task(task_data["payload"])
            self.metrics_history.append(result)
            return result

        except Exception as e:
            self.logger.error(f"Error executing task {task_id}: {e}")
            return TaskResult(
                task_id=task_id,
                agent_id=agent_id,
                status="failed",
                error_message=str(e)
            )

    async def execute_batch(self, tasks: List[Dict[str, Any]], max_concurrent: int = 3) -> List[TaskResult]:
        """批量执行任务"""
        results = []

        async def worker():
            while self.task_queue:
                task_data = self.task_queue.pop(0)
                agent_id = task_data.get("agent_id") or self._select_best_agent()
                result = await self.execute_task(task_data["id"], agent_id)
                results.append(result)

        # 创建并启动工作协程
        workers = [worker() for _ in range(min(max_concurrent, len(tasks)))]
        await asyncio.gather(*workers)

        return results

    def _select_best_agent(self, task_type: str = "general") -> str:
        """根据任务类型选择最佳代理"""
        # 简单的负载均衡策略
        available_agents = list(self.agents.keys())
        return available_agents[0] if available_agents else None

    def get_agent_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """获取指定代理的指标"""
        if agent_id in self.agents:
            return asyncio.run(self.agents[agent_id].get_metrics())
        return None

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态信息"""
        return {
            "total_agents": len(self.agents),
            "queued_tasks": len(self.task_queue),
            "completed_tasks": len(self.metrics_history),
            "active_tasks": len(self.active_tasks),
            "agents": {
                agent_id: {
                    "type": self.agents[agent_id].__class__.__name__,
                    "metrics": asyncio.run(self.agents[agent_id].get_metrics()) if agent_id in self.agents else None
                }
                for agent_id in self.agents
            }
        }

    def display_dashboard(self):
        """显示实时仪表板"""
        table = Table(title="AI Agent Harness Dashboard")

        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        status = self.get_system_status()
        table.add_row("Total Agents", str(status["total_agents"]))
        table.add_row("Queued Tasks", str(status["queued_tasks"]))
        table.add_row("Completed Tasks", str(status["completed_tasks"]))
        table.add_row("Active Tasks", str(status["active_tasks"]))

        console.print(table)

        # 显示每个代理的状态
        for agent_id, info in status["agents"].items():
            agent_table = Table(title=f"Agent {agent_id}")
            agent_table.add_column("Property", style="cyan")
            agent_table.add_column("Value", style="green")

            metrics = info["metrics"]
            if metrics:
                agent_table.add_row("Type", info["type"])
                agent_table.add_row("Execution Time", f"{metrics.execution_time:.2f}s")
                agent_table.add_row("Success Rate", f"{metrics.success_rate:.1%}")
                agent_table.add_row("Tokens Used", str(metrics.tokens_used))

            console.print(agent_table)

if __name__ == "__main__":
    # 示例用法
    controller = AgentController()

    # 注册代理
    text_agent_id = controller.register_agent(
        AgentType.TEXT_AGENT,
        {"model": "claude-3-sonnet-20240229"}
    )

    browser_agent_id = controller.register_agent(
        AgentType.BROWSER_AGENT,
        {}
    )

    search_agent_id = controller.register_agent(
        AgentType.SEARCH_AGENT,
        {}
    )

    # 提交任务
    task1 = {
        "prompt": "What is the capital of France?",
        "system_prompt": "You are a helpful assistant."
    }

    task2 = {
        "url": "https://example.com",
        "actions": ["navigate", "scroll"]
    }

    task3 = {
        "query": "latest AI research",
        "engine": "google"
    }

    asyncio.run(controller.submit_task(task1, text_agent_id))
    asyncio.run(controller.submit_task(task2, browser_agent_id))
    asyncio.run(controller.submit_task(task3, search_agent_id))

    # 显示仪表板
    controller.display_dashboard()