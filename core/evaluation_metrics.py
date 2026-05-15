#!/usr/bin/env python3
"""
AI Agent Harness - 评估指标系统

提供标准化的评估方法和性能指标计算。
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict

class MetricType(Enum):
    """指标类型"""
    PERFORMANCE = "performance"
    ACCURACY = "accuracy"
    EFFICIENCY = "efficiency"
    USER_EXPERIENCE = "user_experience"
    COST_ANALYSIS = "cost_analysis"

class EvaluationStatus(Enum):
    """评估状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class PerformanceMetric:
    """性能指标"""
    metric_id: str
    name: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AccuracyResult:
    """准确性结果"""
    expected_answer: Any
    actual_answer: Any
    similarity_score: float
    confidence_score: float
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EfficiencyMetrics:
    """效率指标"""
    execution_time: float
    resource_usage: Dict[str, float]
    throughput: float
    latency_percentiles: Dict[str, float]

@dataclass
class UserExperienceScore:
    """用户体验评分"""
    clarity: float
    usefulness: float
    reliability: float
    overall_rating: float
    feedback: str = ""

class MetricsCollector:
    """指标收集器"""

    def __init__(self):
        self.metrics_store: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        self.session_data: Dict[str, Dict[str, Any]] = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """设置日志记录器"""
        import logging
        logger = logging.getLogger("MetricsCollector")
        logger.setLevel(logging.INFO)
        return logger

    def collect_metric(self, metric_type: str, name: str, value: float,
                      unit: str = "", metadata: Dict[str, Any] = None) -> str:
        """收集性能指标"""
        metric_id = f"{metric_type}_{name}_{int(datetime.now().timestamp())}"

        metric = PerformanceMetric(
            metric_id=metric_id,
            name=name,
            value=value,
            unit=unit,
            metadata=metadata or {}
        )

        self.metrics_store[metric_type].append(metric)
        return metric_id

    def start_session(self, session_id: str, config: Dict[str, Any] = None):
        """开始新的测试会话"""
        self.session_data[session_id] = {
            "start_time": datetime.now(),
            "config": config or {},
            "metrics": [],
            "events": []
        }

    def end_session(self, session_id: str) -> Dict[str, Any]:
        """结束测试会话并返回摘要"""
        if session_id not in self.session_data:
            return {}

        session = self.session_data[session_id]
        duration = (datetime.now() - session["start_time"]).total_seconds()

        summary = {
            "session_id": session_id,
            "duration": duration,
            "start_time": session["start_time"],
            "end_time": datetime.now(),
            "event_count": len(session["events"])
        }

        # 保存会话数据
        self.save_session_data(session_id, summary)
        return summary

    def record_event(self, session_id: str, event_type: str, data: Dict[str, Any]):
        """记录事件"""
        if session_id in self.session_data:
            self.session_data[session_id]["events"].append({
                "type": event_type,
                "data": data,
                "timestamp": datetime.now()
            })

    def get_session_metrics(self, session_id: str) -> List[PerformanceMetric]:
        """获取会话的所有指标"""
        # 这里应该从存储中检索会话相关的指标
        return []

    def calculate_average_metrics(self, metric_type: str, time_window: timedelta = None) -> Dict[str, float]:
        """计算指定时间窗口内的平均指标"""
        metrics = self.metrics_store.get(metric_type, [])

        if not metrics:
            return {}

        now = datetime.now()
        if time_window:
            cutoff_time = now - time_window
            metrics = [m for m in metrics if m.timestamp >= cutoff_time]

        if not metrics:
            return {}

        # 按名称分组计算平均值
        averages = defaultdict(list)
        for metric in metrics:
            averages[metric.name].append(metric.value)

        return {name: sum(values) / len(values) if values else 0.0
                for name, values in averages.items()}

    def save_session_data(self, session_id: str, summary: Dict[str, Any]):
        """保存会话数据到文件"""
        import os
        os.makedirs("data", exist_ok=True)

        filename = f"data/session_{session_id}.json"
        session_data = {
            "summary": summary,
            "metrics": dict(self.metrics_store),
            "created_at": datetime.now().isoformat()
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

class EvaluationEngine:
    """评估引擎"""

    def __init__(self, metrics_collector: MetricsCollector):
        self.collector = metrics_collector
        self.evaluators: Dict[str, Callable[[Any, Any], float]] = {}
        self._initialize_evaluators()

    def _initialize_evaluators(self):
        """初始化评估器"""
        self.evaluators.update({
            "exact_match": self._exact_match_evaluator,
            "fuzzy_match": self._fuzzy_match_evaluator,
            "semantic_similarity": self._semantic_similarity_evaluator,
            "completeness": self._completeness_evaluator
        })

    def evaluate_response(self, expected: Any, actual: Any,
                         evaluator_type: str = "fuzzy_match",
                         **kwargs) -> AccuracyResult:
        """评估响应准确性"""
        if evaluator_type not in self.evaluators:
            raise ValueError(f"Unknown evaluator type: {evaluator_type}")

        score = self.evaluators[evaluator_type](expected, actual, **kwargs)

        return AccuracyResult(
            expected_answer=expected,
            actual_answer=actual,
            similarity_score=score,
            confidence_score=min(score, 0.95)  # 限制最大置信度
        )

    def _exact_match_evaluator(self, expected: str, actual: str, **kwargs) -> float:
        """精确匹配评估器"""
        if isinstance(expected, str) and isinstance(actual, str):
            return 1.0 if expected.lower().strip() == actual.lower().strip() else 0.0
        return 0.0

    def _fuzzy_match_evaluator(self, expected: Any, actual: Any, threshold: float = 0.8, **kwargs) -> float:
        """模糊匹配评估器"""
        if isinstance(expected, str) and isinstance(actual, str):
            # 简单的字符串相似度（实际应用中应该使用更复杂的算法）
            expected_lower = expected.lower().strip()
            actual_lower = actual.lower().strip()

            if expected_lower == actual_lower:
                return 1.0

            # 计算编辑距离相似度
            distance = self._levenshtein_distance(expected_lower, actual_lower)
            max_len = max(len(expected_lower), len(actual_lower))
            similarity = 1.0 - (distance / max_len) if max_len > 0 else 1.0

            return similarity if similarity >= threshold else 0.0

        return 0.0

    def _semantic_similarity_evaluator(self, expected: str, actual: str, **kwargs) -> float:
        """语义相似度评估器（简化版）"""
        # 这是一个简化的实现，实际应该使用嵌入模型
        if isinstance(expected, str) and isinstance(actual, str):
            expected_words = set(expected.lower().split())
            actual_words = set(actual.lower().split())

            if not expected_words or not actual_words:
                return 0.0

            intersection = expected_words.intersection(actual_words)
            union = expected_words.union(actual_words)

            return len(intersection) / len(union) if union else 0.0

        return 0.0

    def _completeness_evaluator(self, expected: Dict[str, Any], actual: Dict[str, Any], **kwargs) -> float:
        """完整性评估器"""
        if not isinstance(expected, dict) or not isinstance(actual, dict):
            return 0.0

        required_keys = set(expected.keys())
        actual_keys = set(actual.keys())

        if not required_keys:
            return 1.0

        covered_keys = required_keys.intersection(actual_keys)
        completeness_ratio = len(covered_keys) / len(required_keys)

        return completeness_ratio

    def calculate_overall_performance(self, results: List[AccuracyResult],
                                    weights: Dict[str, float] = None) -> Dict[str, float]:
        """计算整体性能"""
        if not results:
            return {}

        # 默认权重
        if weights is None:
            weights = {
                "accuracy": 0.6,
                "efficiency": 0.2,
                "usability": 0.2
            }

        # 计算各维度得分
        accuracy_scores = [r.similarity_score for r in results]
        avg_accuracy = (sum(accuracy_scores) / len(accuracy_scores)
                        if accuracy_scores else 0.0)

        # 模拟效率和可用性得分（在实际应用中需要真实数据）
        efficiency_score = 0.7  # 假设值
        usability_score = 0.8   # 假设值

        overall_score = (
            avg_accuracy * weights["accuracy"] +
            efficiency_score * weights["efficiency"] +
            usability_score * weights["usability"]
        )

        return {
            "overall_score": overall_score,
            "accuracy_score": avg_accuracy,
            "efficiency_score": efficiency_score,
            "usability_score": usability_score,
            "test_count": len(results)
        }

    async def run_comprehensive_evaluation(self, agent_id: str,
                                         test_cases: List[Dict[str, Any]],
                                         evaluation_config: Dict[str, Any]) -> Dict[str, Any]:
        """运行综合评估"""
        self.collector.start_session(f"eval_{agent_id}_{int(datetime.now().timestamp())}")

        try:
            results = []
            evaluator_type = evaluation_config.get("evaluator_type", "fuzzy_match")

            console.print(f"[blue]Running comprehensive evaluation for agent: {agent_id}[/blue]")

            for i, test_case in enumerate(test_cases):
                console.print(f"  Processing test case {i+1}/{len(test_cases)}...")

                expected = test_case.get("expected")
                prompt = test_case.get("prompt")

                # 模拟代理响应（在实际应用中应该是真实的代理调用）
                await asyncio.sleep(0.1)  # 模拟处理时间
                actual_response = f"Response to: {prompt}" if prompt else "Default response"

                # 评估响应
                result = self.evaluate_response(expected, actual_response, evaluator_type)

                results.append(result)
                self.collector.record_event(
                    self.collector.session_data[-1][0],  # session_id
                    "test_case_completed",
                    {"test_index": i, "score": result.similarity_score}
                )

            # 计算最终得分
            performance_summary = self.calculate_overall_performance(results)

            # 添加详细结果
            performance_summary.update({
                "detailed_results": [
                    {
                        "expected": r.expected_answer,
                        "actual": r.actual_answer,
                        "similarity_score": r.similarity_score,
                        "confidence_score": r.confidence_score
                    }
                    for r in results
                ],
                "evaluation_timestamp": datetime.now().isoformat(),
                "agent_id": agent_id
            })

            self.collector.record_event(
                self.collector.session_data[-1][0],
                "evaluation_completed",
                performance_summary
            )

            return performance_summary

        except Exception as e:
            error_msg = f"Evaluation failed: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            self.collector.record_event(
                self.collector.session_data[-1][0],
                "evaluation_failed",
                {"error": error_msg}
            )
            raise

        finally:
            self.collector.end_session(self.collector.session_data[-1][0])

class BenchmarkSuite:
    """基准测试套件"""

    def __init__(self, evaluation_engine: EvaluationEngine):
        self.engine = evaluation_engine
        self.benchmarks: Dict[str, Dict[str, Any]] = {}
        self._load_benchmark_suites()

    def _load_benchmark_suites(self):
        """加载基准测试套件"""
        # 文本理解基准
        self.benchmarks["text_understanding"] = {
            "name": "Text Understanding Benchmark",
            "description": "Evaluate text comprehension and reasoning abilities",
            "test_cases": [
                {
                    "prompt": "What is the capital of France?",
                    "expected": "Paris",
                    "category": "geography"
                },
                {
                    "prompt": "Explain photosynthesis in simple terms.",
                    "expected": "Photosynthesis is how plants make food using sunlight.",
                    "category": "science"
                },
                {
                    "prompt": "Who wrote 'To Kill a Mockingbird'?",
                    "expected": "Harper Lee",
                    "category": "literature"
                }
            ]
        }

        # 问题解决基准
        self.benchmarks["problem_solving"] = {
            "name": "Problem Solving Benchmark",
            "description": "Evaluate logical reasoning and problem-solving skills",
            "test_cases": [
                {
                    "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
                    "expected": "No, this is not a valid conclusion from the premises given.",
                    "category": "logic"
                },
                {
                    "prompt": "Solve: 2x + 5 = 15",
                    "expected": "x = 5",
                    "category": "mathematics"
                }
            ]
        }

        # 信息检索基准
        self.benchmarks["information_retrieval"] = {
            "name": "Information Retrieval Benchmark",
            "description": "Evaluate information extraction and synthesis capabilities",
            "test_cases": [
                {
                    "prompt": "Summarize the key points about artificial intelligence from the provided text.",
                    "expected": "AI involves machine intelligence, intelligent agents, and goal-oriented systems.",
                    "category": "summarization"
                }
            ]
        }

    def get_benchmark(self, benchmark_name: str) -> Optional[Dict[str, Any]]:
        """获取指定的基准测试"""
        return self.benchmarks.get(benchmark_name)

    def list_available_benchmarks(self) -> List[str]:
        """列出所有可用的基准测试"""
        return list(self.benchmarks.keys())

    async def run_benchmark(self, benchmark_name: str, agent_id: str,
                           evaluation_engine: EvaluationEngine,
                           config: Dict[str, Any] = None) -> Dict[str, Any]:
        """运行指定的基准测试"""
        benchmark = self.get_benchmark(benchmark_name)
        if not benchmark:
            raise ValueError(f"Benchmark not found: {benchmark_name}")

        console.print(f"\n[bold blue]Running Benchmark: {benchmark['name']}[/bold blue]")
        console.print(f"Description: {benchmark['description']}")
        console.print(f"Test Cases: {len(benchmark['test_cases'])}")

        # 准备评估配置
        eval_config = config or {
            "evaluator_type": "fuzzy_match",
            "weights": {"accuracy": 0.7, "efficiency": 0.2, "usability": 0.1}
        }

        # 运行评估
        results = await evaluation_engine.run_comprehensive_evaluation(
            agent_id=agent_id,
            test_cases=benchmark["test_cases"],
            evaluation_config=eval_config
        )

        # 添加基准测试信息
        results["benchmark_info"] = {
            "name": benchmark["name"],
            "description": benchmark["description"],
            "test_count": len(benchmark["test_cases"])
        }

        return results

    def compare_agent_performance(self, agent_results: Dict[str, Dict[str, Any]],
                                 benchmark_name: str) -> Dict[str, Any]:
        """比较多个代理在相同基准上的表现"""
        comparison_data = {
            "benchmark": benchmark_name,
            "agents": {},
            "ranking": [],
            "analysis": {}
        }

        # 提取各代理的得分
        for agent_id, result in agent_results.items():
            overall_score = result.get("overall_score", 0.0)
            comparison_data["agents"][agent_id] = {
                "overall_score": overall_score,
                "accuracy_score": result.get("accuracy_score", 0.0),
                "test_count": result.get("test_count", 0)
            }

            comparison_data["ranking"].append({
                "agent_id": agent_id,
                "score": overall_score
            })

        # 按得分排序
        comparison_data["ranking"].sort(key=lambda x: x["score"], reverse=True)

        # 生成分析摘要
        scores = [data["score"] for data in comparison_data["ranking"]]
        if scores:
            comparison_data["analysis"] = {
                "highest_score": max(scores),
                "lowest_score": min(scores),
                "average_score": sum(scores) / len(scores),
                "score_range": max(scores) - min(scores),
                "consistency_rank": comparison_data["ranking"][0]["agent_id"] if comparison_data["ranking"] else None
            }

        return comparison_data

def create_sample_evaluation():
    """创建示例评估场景"""
    collector = MetricsCollector()
    engine = EvaluationEngine(collector)
    benchmark_suite = BenchmarkSuite(engine)

    # 示例：运行文本理解基准
    async def run_example():
        try:
            results = await benchmark_suite.run_benchmark(
                "text_understanding",
                "sample_agent",
                engine
            )

            print(f"\nBenchmark Results:")
            print(f"Overall Score: {results.get('overall_score', 0):.3f}")
            print(f"Test Count: {results.get('test_count', 0)}")

            # 显示详细结果
            detailed_results = results.get("detailed_results", [])
            for i, res in enumerate(detailed_results[:3]):  # 显示前3个结果
                print(f"\nTest {i+1}:")
                print(f"  Expected: {res['expected']}")
                print(f"  Actual: {res['actual']}")
                print(f"  Similarity: {res['similarity_score']:.3f}")

        except Exception as e:
            print(f"Error running benchmark: {e}")

    asyncio.run(run_example())

if __name__ == "__main__":
    create_sample_evaluation()