#!/usr/bin/env python3
"""
AI Agent Harness - 主程序入口

提供命令行接口来运行测试、管理代理和生成报告。
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any

# rich为可选依赖
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

from agent_controller import AgentController, AgentType
from test_scenarios import ScenarioGenerator, TestExecutor, DifficultyLevel, ScenarioType
from evaluation_metrics import EvaluationEngine, MetricsCollector

def setup_directories():
    """创建必要的目录结构"""
    directories = ["data", "logs", "reports"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def create_sample_agents(controller: AgentController) -> Dict[str, str]:
    """创建示例代理"""
    agents = {}

    # 文本代理
    text_agent_id = controller.register_agent(
        AgentType.TEXT_AGENT,
        {
            "model": "claude-3-sonnet-20240229",
            "temperature": 0.7,
            "max_tokens": 1000
        }
    )
    agents["text"] = text_agent_id

    # 浏览器代理
    browser_agent_id = controller.register_agent(
        AgentType.BROWSER_AGENT,
        {
            "headless": False,
            "timeout": 30000,
            "viewport_width": 1200,
            "viewport_height": 800
        }
    )
    agents["browser"] = browser_agent_id

    # 搜索代理
    search_agent_id = controller.register_agent(
        AgentType.SEARCH_AGENT,
        {
            "engines": ["google", "bing", "duckduckgo"],
            "max_results": 10,
            "cache_enabled": True
        }
    )
    agents["search"] = search_agent_id

    return agents

async def run_basic_tests(controller: AgentController, executor: TestExecutor):
    """运行基础测试"""
    console.print("\n[bold blue]Running Basic Tests[/bold blue]")

    scenario_generator = executor.scenario_generator

    # 获取基础测试场景
    basic_scenarios = scenario_generator.list_scenarios(
        difficulty_filter=DifficultyLevel.BASIC
    )

    if not basic_scenarios:
        console.print("[yellow]No basic scenarios found[/yellow]")
        return

    console.print(f"Found {len(basic_scenarios)} basic scenarios")

    # 执行测试
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        task = progress.add_task("Executing tests...", total=len(basic_scenarios))

        for scenario in basic_scenarios:
            result = await executor.execute_test(scenario.scenario_id, "text_agent")
            progress.advance(task)

            console.print(f"  ✓ {scenario.name}: {result.status} (Score: {result.score:.1f})")

async def run_custom_scenario(controller: AgentController, args: argparse.Namespace):
    """运行自定义场景"""
    console.print("\n[bold blue]Running Custom Scenario[/bold blue]")

    # 创建自定义场景
    scenario_generator = ScenarioGenerator()
    custom_scenario = scenario_generator.generate_dynamic_scenario(
        ScenarioType(args.scenario_type),
        DifficultyLevel(args.difficulty),
        {"custom_param": args.custom_param}
    )

    console.print(f"Created custom scenario: {custom_scenario.name}")
    console.print(f"Description: {custom_scenario.description}")

    # 执行场景
    executor = TestExecutor(scenario_generator)
    result = await executor.execute_test(custom_scenario.scenario_id, "text_agent")

    console.print(f"\nCustom scenario result:")
    console.print(f"  Status: {result.status}")
    console.print(f"  Score: {result.score:.1f}")
    console.print(f"  Execution time: {result.execution_time:.1f}s")

async def generate_report(controller: AgentController, executor: TestExecutor, args: argparse.Namespace):
    """生成测试报告"""
    console.print("\n[bold blue]Generating Report[/bold blue]")

    # 收集所有结果
    all_results = executor.results

    if not all_results:
        console.print("[yellow]No test results available for report generation[/yellow]")
        return

    # 按代理分组结果
    results_by_agent = {}
    for result in all_results:
        if result.agent_id not in results_by_agent:
            results_by_agent[result.agent_id] = []
        results_by_agent[result.agent_id].append(result)

    # 生成详细报告
    report_data = {
        "timestamp": asyncio.get_event_loop().time(),
        "total_tests": len(all_results),
        "results_by_agent": {},
        "summary_statistics": {}
    }

    for agent_id, results in results_by_agent.items():
        summary = executor.get_performance_summary(agent_id)
        report_data["results_by_agent"][agent_id] = summary

        # 显示代理性能表格
        table = Table(title=f"Agent Performance: {agent_id}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Tests", str(summary.get("total_tests", 0)))
        table.add_row("Success Rate", f"{summary.get('success_rate', 0):.1%}")
        table.add_row("Average Score", f"{summary.get('average_score', 0):.1f}")
        table.add_row("Avg Execution Time", f"{summary.get('average_execution_time', 0):.1f}s")

        console.print(table)

    # 保存报告到文件
    report_path = f"reports/harness_report_{int(report_data['timestamp'])}.json"
    os.makedirs("reports", exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    console.print(f"\n[green]Report saved to: {report_path}[/green]")

async def display_dashboard(controller: AgentController):
    """显示实时仪表板"""
    while True:
        controller.display_dashboard()

        # 等待一段时间再更新
        await asyncio.sleep(5)

        # 检查是否应该退出（在实际应用中可能需要更复杂的退出逻辑）
        break  # 这里简化处理，实际可能需要用户输入或超时机制

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI Agent Harness System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 基础测试命令
    basic_parser = subparsers.add_parser("basic", help="Run basic tests")

    # 自定义场景命令
    custom_parser = subparsers.add_parser("custom", help="Run custom scenario")
    custom_parser.add_argument("--type", choices=[st.value for st in ScenarioType], default="text_processing",
                              help="Scenario type")
    custom_parser.add_argument("--difficulty", choices=[dl.value for dl in DifficultyLevel],
                              default="intermediate", help="Difficulty level")
    custom_parser.add_argument("--param", dest="custom_param", help="Custom parameter value")

    # 报告生成命令
    report_parser = subparsers.add_parser("report", help="Generate test report")

    # 仪表板命令
    dashboard_parser = subparsers.add_parser("dashboard", help="Display live dashboard")

    # 帮助命令
    subparsers.add_parser("help", help="Show this help message")

    args = parser.parse_args()

    if not args.command or args.command == "help":
        parser.print_help()
        return

    # 设置目录
    setup_directories()

    # 初始化组件
    controller = AgentController()
    scenario_generator = ScenarioGenerator()
    executor = TestExecutor(scenario_generator)

    # 创建示例代理
    agents = create_sample_agents(controller)

    console.print(Panel.fit(
        "[bold green]AI Agent Harness System[/bold green]\n"
        "A comprehensive testing framework for AI agents\n\n"
        f"[blue]Available Commands:[/blue]\n"
        "• basic     - Run basic tests\n"
        "• custom    - Run custom scenario\n"
        "• report    - Generate test report\n"
        "• dashboard - Display live dashboard\n"
        "• help      - Show this help message",
        title="Welcome"
    ))

    try:
        if args.command == "basic":
            asyncio.run(run_basic_tests(controller, executor))

        elif args.command == "custom":
            asyncio.run(run_custom_scenario(controller, args))

        elif args.command == "report":
            asyncio.run(generate_report(controller, executor, args))

        elif args.command == "dashboard":
            asyncio.run(display_dashboard(controller))

        else:
            console.print(f"[red]Unknown command: {args.command}[/red]")
            parser.print_help()

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())

if __name__ == "__main__":
    main()