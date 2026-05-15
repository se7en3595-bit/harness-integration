#!/usr/bin/env python3
"""
AI Agent Harness - 测试场景引擎

提供标准化的测试用例和动态场景生成，用于评估AI代理在各种条件下的表现。
"""

import asyncio
import random
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid

# rich为可选依赖
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

class DifficultyLevel(Enum):
    """难度等级"""
    BASIC = "basic"        # 基础测试
    INTERMEDIATE = "intermediate"  # 中级测试
    ADVANCED = "advanced"  # 高级测试
    EXPERT = "expert"      # 专家级测试

class ScenarioType(Enum):
    """场景类型"""
    TEXT_PROCESSING = "text_processing"
    WEB_NAVIGATION = "web_navigation"
    INFORMATION_RETRIEVAL = "information_retrieval"
    MULTIMODAL_ANALYSIS = "multimodal_analysis"
    COORDINATION_TASKS = "coordination_tasks"

@dataclass
class TestScenario:
    """测试场景定义"""
    scenario_id: str
    name: str
    description: str
    type: ScenarioType
    difficulty: DifficultyLevel
    expected_duration: int  # 秒数
    success_criteria: Dict[str, Any]
    input_data: Dict[str, Any]
    validation_rules: List[Callable[[Any], bool]]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestResult:
    """测试执行结果"""
    test_id: str
    scenario_id: str
    agent_id: str
    status: str  # "passed", "failed", "partial", "timeout"
    score: float  # 0-100
    execution_time: float
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class ScenarioGenerator:
    """测试场景生成器"""

    def __init__(self):
        self.scenarios: Dict[str, TestScenario] = {}
        self._initialize_default_scenarios()

    def _initialize_default_scenarios(self):
        """初始化默认测试场景"""
        scenarios = [
            # 文本处理场景
            TestScenario(
                scenario_id="text_qa_basic",
                name="基础问答测试",
                description="测试代理对简单问题的理解和回答能力",
                type=ScenarioType.TEXT_PROCESSING,
                difficulty=DifficultyLevel.BASIC,
                expected_duration=30,
                success_criteria={
                    "accuracy_threshold": 0.8,
                    "response_length_min": 50,
                    "contains_key_info": True
                },
                input_data={
                    "question": "What is the capital of France?",
                    "context": "Geography and world capitals"
                },
                validation_rules=[
                    lambda response: len(str(response)) > 50,
                    lambda response: "paris" in str(response).lower()
                ]
            ),

            TestScenario(
                scenario_id="text_summarization_intermediate",
                name="文本摘要测试",
                description="测试代理从长文本中提取关键信息并生成摘要的能力",
                type=ScenarioType.TEXT_PROCESSING,
                difficulty=DifficultyLevel.INTERMEDIATE,
                expected_duration=60,
                success_criteria={
                    "summary_length_ratio": 0.2,
                    "key_points_coverage": 0.7,
                    "coherence_score": 0.6
                },
                input_data={
                    "text": """
                    Artificial Intelligence (AI) is intelligence demonstrated by machines,
                    as opposed to the natural intelligence displayed by humans or animals.
                    Leading AI textbooks define the field as the study of intelligent agents:
                    any system that perceives its environment and takes actions that maximize
                    its chance of achieving its goals.
                    """,
                    "target_length": "short"
                },
                validation_rules=[
                    lambda summary: len(str(summary)) < 100,
                    lambda summary: "intelligence" in str(summary).lower(),
                    lambda summary: "machines" in str(summary).lower()
                ]
            ),

            # 网页导航场景
            TestScenario(
                scenario_id="web_search_basic",
                name="网页搜索测试",
                description="测试代理搜索和提取网页信息的能力",
                type=ScenarioType.WEB_NAVIGATION,
                difficulty=DifficultyLevel.BASIC,
                expected_duration=45,
                success_criteria={
                    "page_loaded": True,
                    "relevant_content_found": True,
                    "navigation_successful": True
                },
                input_data={
                    "url": "https://example.com",
                    "search_query": "AI technology trends",
                    "actions": ["load_page", "extract_title", "find_links"]
                },
                validation_rules=[
                    lambda result: isinstance(result, dict),
                    lambda result: "visited_urls" in result,
                    lambda result: len(result.get("visited_urls", [])) > 0
                ]
            ),

            # 信息检索场景
            TestScenario(
                scenario_id="info_retrieval_advanced",
                name="复杂信息检索测试",
                description="测试代理在多源信息中定位和整合特定信息的能力",
                type=ScenarioType.INFORMATION_RETRIEVAL,
                difficulty=DifficultyLevel.ADVANCED,
                expected_duration=120,
                success_criteria={
                    "sources_accessed": 3,
                    "information_accuracy": 0.85,
                    "synthesis_quality": 0.75
                },
                input_data={
                    "query": "latest developments in quantum computing",
                    "required_sources": ["academic", "news", "technical_blogs"],
                    "time_range": "last_6_months"
                },
                validation_rules=[
                    lambda result: isinstance(result, list),
                    lambda result: len(result) >= 3,
                    lambda result: any("quantum" in str(r).lower() for r in result)
                ]
            ),

            # 多模态分析场景
            TestScenario(
                scenario_id="multimodal_analysis_expert",
                name="多模态综合分析测试",
                description="测试代理处理和分析多种类型输入数据的能力",
                type=ScenarioType.MULTIMODAL_ANALYSIS,
                difficulty=DifficultyLevel.EXPERT,
                expected_duration=180,
                success_criteria={
                    "cross_modal_consistency": 0.8,
                    "comprehensive_analysis": True,
                    "insight_depth": 0.9
                },
                input_data={
                    "text_input": "Describe the image content",
                    "image_url": "https://example.com/sample.jpg",
                    "audio_url": "https://example.com/sample.mp3"
                },
                validation_rules=[
                    lambda result: isinstance(result, dict),
                    lambda result: all(key in result for key in ["text_analysis", "visual_analysis", "audio_analysis"])
                ]
            )
        ]

        for scenario in scenarios:
            self.scenarios[scenario.scenario_id] = scenario

    def get_scenario(self, scenario_id: str) -> Optional[TestScenario]:
        """获取指定场景"""
        return self.scenarios.get(scenario_id)

    def list_scenarios(self, type_filter: Optional[ScenarioType] = None,
                      difficulty_filter: Optional[DifficultyLevel] = None) -> List[TestScenario]:
        """列出符合条件的场景"""
        scenarios = list(self.scenarios.values())

        if type_filter:
            scenarios = [s for s in scenarios if s.type == type_filter]

        if difficulty_filter:
            scenarios = [s for s in scenarios if s.difficulty == difficulty_filter]

        return scenarios

    def generate_dynamic_scenario(self, base_type: ScenarioType,
                                difficulty: DifficultyLevel,
                                custom_params: Dict[str, Any]) -> TestScenario:
        """生成动态测试场景"""
        scenario_id = f"dynamic_{base_type.value}_{difficulty.value}_{uuid.uuid4().hex[:8]}"

        # 根据类型和难度生成不同的参数
        if base_type == ScenarioType.TEXT_PROCESSING:
            scenario = self._generate_text_scenario(difficulty, custom_params)
        elif base_type == ScenarioType.WEB_NAVIGATION:
            scenario = self._generate_web_scenario(difficulty, custom_params)
        elif base_type == ScenarioType.INFORMATION_RETRIEVAL:
            scenario = self._generate_search_scenario(difficulty, custom_params)
        else:
            scenario = self._generate_generic_scenario(base_type, difficulty, custom_params)

        scenario.scenario_id = scenario_id
        self.scenarios[scenario_id] = scenario
        return scenario

    def _generate_text_scenario(self, difficulty: DifficultyLevel,
                               params: Dict[str, Any]) -> TestScenario:
        """生成文本处理场景"""
        questions = {
            DifficultyLevel.BASIC: [
                "What is photosynthesis?",
                "Who wrote Romeo and Juliet?",
                "What is the speed of light?"
            ],
            DifficultyLevel.INTERMEDIATE: [
                "Explain the concept of machine learning in simple terms.",
                "Compare and contrast renewable and non-renewable energy sources.",
                "What are the main principles of object-oriented programming?"
            ],
            DifficultyLevel.ADVANCED: [
                "Analyze the ethical implications of autonomous weapons systems.",
                "Discuss the potential impacts of quantum computing on cybersecurity.",
                "Evaluate the effectiveness of different climate change mitigation strategies."
            ],
            DifficultyLevel.EXPERT: [
                "Propose a novel approach to solving the protein folding problem.",
                "Design an algorithm for real-time traffic optimization in megacities.",
                "Develop a comprehensive framework for AI alignment research."
            ]
        }

        question = random.choice(questions[difficulty])
        return TestScenario(
            scenario_id="",
            name=f"{difficulty.value.title()} Text Analysis",
            description=f"Test text understanding and reasoning at {difficulty.value} level",
            type=ScenarioType.TEXT_PROCESSING,
            difficulty=difficulty,
            expected_duration=difficulty.value.count("advanced") * 60 + 30,
            success_criteria={
                "answer_relevance": 0.8,
                "factual_accuracy": 0.9,
                "reasoning_depth": 0.7
            },
            input_data={
                "prompt": question,
                "max_tokens": 500,
                "temperature": 0.7
            },
            validation_rules=[
                lambda response: len(str(response)) > 20,
                lambda response: any(word in str(response).lower() for word in question.lower().split()[:3])
            ]
        )

    def _generate_web_scenario(self, difficulty: DifficultyLevel,
                              params: Dict[str, Any]) -> TestScenario:
        """生成网页导航场景"""
        urls = {
            DifficultyLevel.BASIC: [
                "https://httpbin.org/html",
                "https://www.wikipedia.org",
                "https://developer.mozilla.org/en-US/docs/Web/HTML"
            ],
            DifficultyLevel.INTERMEDIATE: [
                "https://github.com/topics/machine-learning",
                "https://arxiv.org/list/cs.AI/recent",
                "https://www.reddit.com/r/artificial/"
            ],
            DifficultyLevel.ADVANCED: [
                "https://news.ycombinator.com",
                "https://techcrunch.com",
                "https://medium.com/towards-data-science"
            ],
            DifficultyLevel.EXPERT: [
                "https://www.nature.com/articles/s41586-023-xxxxx",  # 示例学术论文
                "https://github.com/pytorch/pytorch",
                "https://kubernetes.io/docs/home/"
            ]
        }

        url = random.choice(urls[difficulty])
        actions = ["load_page", "extract_content", "find_links"]

        return TestScenario(
            scenario_id="",
            name=f"{difficulty.value.title()} Web Navigation",
            description=f"Navigate and extract information from complex web pages",
            type=ScenarioType.WEB_NAVIGATION,
            difficulty=difficulty,
            expected_duration=difficulty.value.count("advanced") * 30 + 45,
            success_criteria={
                "page_loaded": True,
                "content_extracted": True,
                "links_identified": True
            },
            input_data={
                "url": url,
                "actions": actions,
                "extract_elements": ["title", "main_content", "navigation_links"]
            },
            validation_rules=[
                lambda result: isinstance(result, dict),
                lambda result: "extracted_content" in result,
                lambda result: len(result.get("found_links", [])) > 0
            ]
        )

    def _generate_search_scenario(self, difficulty: DifficultyLevel,
                                 params: Dict[str, Any]) -> TestScenario:
        """生成搜索场景"""
        queries = {
            DifficultyLevel.BASIC: [
                "what is artificial intelligence",
                "how does machine learning work",
                "benefits of renewable energy"
            ],
            DifficultyLevel.INTERMEDIATE: [
                "recent advances in neural networks",
                "climate change impact on biodiversity",
                "blockchain technology applications"
            ],
            DifficultyLevel.ADVANCED: [
                "emergent properties in large language models",
                "quantum supremacy experimental verification",
                "sustainable urban planning strategies"
            ],
            DifficultyLevel.EXPERT: [
                "topological quantum error correction codes",
                "consciousness emergence in artificial systems",
                "post-quantum cryptography standardization"
            ]
        }

        query = random.choice(queries[difficulty])

        return TestScenario(
            scenario_id="",
            name=f"{difficulty.value.title()} Information Retrieval",
            description=f"Search and synthesize information from multiple sources",
            type=ScenarioType.INFORMATION_RETRIEVAL,
            difficulty=difficulty,
            expected_duration=difficulty.value.count("advanced") * 45 + 90,
            success_criteria={
                "sources_diversified": True,
                "information_current": True,
                "synthesis_coherent": True
            },
            input_data={
                "query": query,
                "max_results": 10,
                "required_domains": ["academic", "news", "technical"],
                "time_constraint": "recent"
            },
            validation_rules=[
                lambda result: isinstance(result, list),
                lambda result: len(result) >= 3,
                lambda result: any(query.lower() in str(r).lower() for r in result)
            ]
        )

    def _generate_generic_scenario(self, scenario_type: ScenarioType,
                                  difficulty: DifficultyLevel,
                                  params: Dict[str, Any]) -> TestScenario:
        """生成通用场景"""
        base_name = scenario_type.value.replace("_", " ").title()
        scenario_name = f"{difficulty.value.title()} {base_name}"

        return TestScenario(
            scenario_id="",
            name=scenario_name,
            description=f"Generic {scenario_name.lower()} test scenario",
            type=scenario_type,
            difficulty=difficulty,
            expected_duration=60,
            success_criteria={"basic_completion": True},
            input_data={"task_description": f"Complete a {scenario_name.lower()} task"},
            validation_rules=[lambda result: result is not None]
        )

class TestExecutor:
    """测试执行器"""

    def __init__(self, scenario_generator: ScenarioGenerator):
        self.scenario_generator = scenario_generator
        self.results: List[TestResult] = []

    async def execute_test(self, scenario_id: str, agent_id: str,
                          timeout: int = 300) -> TestResult:
        """执行单个测试"""
        scenario = self.scenario_generator.get_scenario(scenario_id)
        if not scenario:
            return TestResult(
                test_id=str(uuid.uuid4()),
                scenario_id=scenario_id,
                agent_id=agent_id,
                status="failed",
                score=0.0,
                execution_time=0.0,
                details={"error": "Scenario not found"}
            )

        start_time = datetime.now()
        test_id = str(uuid.uuid4())

        try:
            # 模拟测试执行
            await asyncio.sleep(min(scenario.expected_duration / 10, 5))  # 加速演示

            # 验证响应
            mock_response = {"test_result": "completed", "data": scenario.input_data}

            passed_rules = sum(1 for rule in scenario.validation_rules if rule(mock_response))
            total_rules = len(scenario.validation_rules)

            # 计算得分
            accuracy_score = passed_rules / max(total_rules, 1)
            time_efficiency = min(1.0, scenario.expected_duration / (datetime.now() - start_time).total_seconds())
            overall_score = (accuracy_score * 0.7 + time_efficiency * 0.3) * 100

            status = "passed" if accuracy_score >= 0.8 else "partial" if accuracy_score >= 0.5 else "failed"

            execution_time = (datetime.now() - start_time).total_seconds()

            result = TestResult(
                test_id=test_id,
                scenario_id=scenario_id,
                agent_id=agent_id,
                status=status,
                score=overall_score,
                execution_time=execution_time,
                details={
                    "accuracy_score": accuracy_score,
                    "time_efficiency": time_efficiency,
                    "rules_passed": passed_rules,
                    "total_rules": total_rules,
                    "scenario_difficulty": scenario.difficulty.value
                }
            )

            self.results.append(result)
            return result

        except asyncio.TimeoutError:
            return TestResult(
                test_id=test_id,
                scenario_id=scenario_id,
                agent_id=agent_id,
                status="timeout",
                score=0.0,
                execution_time=timeout,
                details={"error": "Test timed out"}
            )
        except Exception as e:
            return TestResult(
                test_id=test_id,
                scenario_id=scenario_id,
                agent_id=agent_id,
                status="failed",
                score=0.0,
                execution_time=(datetime.now() - start_time).total_seconds(),
                details={"error": str(e)}
            )

    async def execute_batch_tests(self, scenario_ids: List[str],
                                 agent_id: str,
                                 batch_size: int = 5) -> List[TestResult]:
        """批量执行测试"""
        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            task = progress.add_task(f"Executing {len(scenario_ids)} tests...", total=len(scenario_ids))

            # 分批执行
            for i in range(0, len(scenario_ids), batch_size):
                batch = scenario_ids[i:i + batch_size]
                batch_results = await asyncio.gather(
                    *[self.execute_test(scid, agent_id) for scid in batch],
                    return_exceptions=True
                )

                for result in batch_results:
                    if isinstance(result, TestResult):
                        results.append(result)

                progress.advance(task)

        return results

    def get_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """获取性能摘要"""
        agent_results = [r for r in self.results if r.agent_id == agent_id]

        if not agent_results:
            return {"error": "No results found for this agent"}

        total_tests = len(agent_results)
        passed_tests = len([r for r in agent_results if r.status == "passed"])
        partial_tests = len([r for r in agent_results if r.status == "partial"])
        failed_tests = len([r for r in agent_results if r.status == "failed"])

        avg_score = sum(r.score for r in agent_results) / total_tests
        avg_execution_time = sum(r.execution_time for r in agent_results) / total_tests

        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "partial": partial_tests,
            "failed": failed_tests,
            "success_rate": passed_tests / total_tests,
            "average_score": avg_score,
            "average_execution_time": avg_execution_time,
            "results_by_difficulty": self._analyze_by_difficulty(agent_results)
        }

    def _analyze_by_difficulty(self, results: List[TestResult]) -> Dict[str, Dict[str, Any]]:
        """按难度分析结果"""
        analysis = {}

        for difficulty in DifficultyLevel:
            difficulty_results = [r for r in results if difficulty.value in r.details.get("scenario_difficulty", "")]

            if difficulty_results:
                analysis[difficulty.value] = {
                    "count": len(difficulty_results),
                    "avg_score": sum(r.score for r in difficulty_results) / len(difficulty_results),
                    "success_rate": len([r for r in difficulty_results if r.status == "passed"]) / len(difficulty_results)
                }

        return analysis

    def display_results_table(self):
        """显示结果表格"""
        table = Table(title="Test Execution Results")

        table.add_column("Test ID", style="cyan", no_wrap=True)
        table.add_column("Scenario", style="green")
        table.add_column("Agent", style="yellow")
        table.add_column("Status", style="red")
        table.add_column("Score", style="blue")
        table.add_column("Time (s)", style="magenta")

        for result in self.results[-10:]:  # 显示最近10个结果
            table.add_row(
                result.test_id[:8] + "...",
                result.scenario_id,
                result.agent_id,
                result.status,
                f"{result.score:.1f}",
                f"{result.execution_time:.1f}"
            )

        console.print(table)

if __name__ == "__main__":
    # 示例使用
    generator = ScenarioGenerator()
    executor = TestExecutor(generator)

    # 显示可用场景
    basic_scenarios = generator.list_scenarios(
        difficulty_filter=DifficultyLevel.BASIC
    )

    console.print("\nAvailable Basic Scenarios:")
    for scenario in basic_scenarios:
        console.print(f"  • {scenario.scenario_id}: {scenario.name}")

    # 生成动态场景
    dynamic_scenario = generator.generate_dynamic_scenario(
        ScenarioType.TEXT_PROCESSING,
        DifficultyLevel.INTERMEDIATE,
        {"custom_param": "value"}
    )

    print(f"\nGenerated dynamic scenario: {dynamic_scenario.scenario_id}")
    print(f"Description: {dynamic_scenario.description}")

    # 执行测试示例
    async def run_example():
        # 执行单个测试
        result = await executor.execute_test("text_qa_basic", "agent_123")
        print(f"\nSingle test result: {result.status}, Score: {result.score}")

        # 执行批量测试
        scenario_ids = ["text_qa_basic", "text_summarization_intermediate"]
        batch_results = await executor.execute_batch_tests(scenario_ids, "agent_123")
        print(f"\nBatch test completed: {len(batch_results)} results")

        # 显示性能摘要
        summary = executor.get_performance_summary("agent_123")
        print(f"\nPerformance Summary: {summary}")

        # 显示结果表格
        executor.display_results_table()

    asyncio.run(run_example())