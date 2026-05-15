#!/usr/bin/env python3
"""
AI Agent Harness - 可视化仪表板

提供实时系统监控、性能可视化和交互式报告功能。
rich和matplotlib为可选依赖，未提供时自动降级为标准输出。
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# rich为可选依赖
try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich.columns import Columns
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# matplotlib为可选依赖
try:
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def _get_console():
    """获取console实例（延迟初始化）"""
    if HAS_RICH:
        return Console()
    return None


def _print_rich_or_plain(rich_obj, plain_text: str):
    """根据rich是否可用选择输出方式"""
    if HAS_RICH and rich_obj is not None:
        _get_console().print(rich_obj)
    else:
        print(plain_text)


class DataVisualization:
    """数据可视化类"""

    def __init__(self):
        self.data_dir = Path("data")
        self.reports_dir = Path("reports")
        self._ensure_directories()

    def _ensure_directories(self):
        """确保必要的目录存在"""
        self.data_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)

    def load_historical_data(self, data_type: str) -> List[Dict[str, Any]]:
        """加载历史数据"""
        data_file = self.data_dir / f"{data_type}_history.json"
        if not data_file.exists():
            return []
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据失败 {data_type}: {e}")
            return []

    def save_visualization(self, plot_data: Dict[str, Any], filename: str):
        """保存可视化图表"""
        if not HAS_MATPLOTLIB:
            print("可视化功能需要 matplotlib 和 seaborn: pip install matplotlib seaborn")
            return
        try:
            plt.figure(figsize=(12, 8))
            if "performance" in plot_data:
                self._create_performance_chart(plot_data["performance"])
            elif "comparison" in plot_data:
                self._create_comparison_chart(plot_data["comparison"])
            else:
                self._create_generic_chart(plot_data)
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"可视化图表已保存: {filename}")
        except Exception as e:
            print(f"生成可视化图表失败: {e}")

    def _create_performance_chart(self, performance_data: Dict[str, Any]):
        """创建性能指标图表"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        if "success_rate_trend" in performance_data:
            axes[0, 0].plot(performance_data["success_rate_trend"]["dates"],
                           performance_data["success_rate_trend"]["rates"])
            axes[0, 0].set_title("Success Rate Trend")
        if "execution_time_distribution" in performance_data:
            axes[0, 1].hist(performance_data["execution_time_distribution"], bins=20)
            axes[0, 1].set_title("Execution Time Distribution")
        if "agent_comparison" in performance_data:
            agents = list(performance_data["agent_comparison"].keys())
            scores = list(performance_data["agent_comparison"].values())
            axes[1, 0].bar(agents, scores)
            axes[1, 0].set_title("Agent Performance Comparison")
        if "resource_usage" in performance_data:
            rd = performance_data["resource_usage"]
            axes[1, 1].pie(rd.values(), labels=rd.keys(), autopct='%1.1f%%')
            axes[1, 1].set_title("Resource Usage")
        plt.suptitle("AI Agent Harness Performance Dashboard", fontsize=16, fontweight='bold')

    def _create_comparison_chart(self, comparison_data: Dict[str, Any]):
        """创建对比分析图表"""
        fig, ax = plt.subplots(figsize=(10, 6))
        agents = list(comparison_data.get("agents", {}).keys())
        scores = [comparison_data["agents"][agent]["overall_score"] for agent in agents]
        ax.bar(agents, scores)
        ax.set_title("Agent Performance Comparison")
        ax.set_ylabel("Overall Score")
        plt.xticks(rotation=45)
        plt.tight_layout()

    def _create_generic_chart(self, plot_data: Dict[str, Any]):
        """创建通用图表"""
        plt.figure(figsize=(10, 6))
        plt.plot(list(plot_data.keys()), list(plot_data.values()))
        plt.title("Generic Data Visualization")
        plt.xlabel("Metric")
        plt.ylabel("Value")


class RealTimeMonitor:
    """实时监控器"""

    def __init__(self):
        self.monitor_data = {
            "system_status": {},
            "agent_metrics": {},
            "task_queue": [],
            "performance_trends": []
        }

    def update_system_status(self, controller_data: Dict[str, Any]):
        """更新系统状态"""
        self.monitor_data["system_status"] = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": controller_data.get("total_agents", 0),
            "queued_tasks": controller_data.get("queued_tasks", 0),
            "completed_tasks": controller_data.get("completed_tasks", 0),
            "active_tasks": controller_data.get("active_tasks", 0)
        }

    def update_agent_metrics(self, metrics: Dict[str, Any]):
        """更新代理指标"""
        self.monitor_data["agent_metrics"] = metrics

    def add_task_event(self, task_id: str, event_type: str, status: str):
        """添加任务事件"""
        self.monitor_data["task_queue"].append({
            "task_id": task_id,
            "event_type": event_type,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.monitor_data["task_queue"]) > 50:
            self.monitor_data["task_queue"] = self.monitor_data["task_queue"][-50:]

    def generate_performance_summary(self) -> Dict[str, Any]:
        """生成性能摘要"""
        summary = {}
        if self.monitor_data["system_status"]:
            status = self.monitor_data["system_status"]
            total_tasks = status.get("queued_tasks", 0) + status.get("completed_tasks", 0)
            completion_rate = (status.get("completed_tasks", 0) / max(total_tasks, 1)) * 100
            summary.update({
                "completion_rate": round(completion_rate, 2),
                "system_load": "High" if status.get("queued_tasks", 0) > 10 else "Normal"
            })
        return summary


class InteractiveDashboard:
    """交互式仪表板主类"""

    def __init__(self):
        self.visualizer = DataVisualization()
        self.monitor = RealTimeMonitor()
        self.is_running = False
        self.dashboard_layout = None

    def create_dashboard_layout(self):
        """创建仪表板布局"""
        if not HAS_RICH:
            print("实时仪表板需要 rich 库: pip install rich")
            return None
        layout = Layout()
        layout.split_column(Layout(name="header", size=3), Layout(name="main", ratio=1))
        layout["main"].split_row(Layout(name="left_panel", ratio=1), Layout(name="right_panel", ratio=1))
        layout["left_panel"].split_column(Layout(name="system_status"), Layout(name="agent_overview"))
        layout["right_panel"].split_column(Layout(name="performance_metrics"), Layout(name="recent_events"))
        self.dashboard_layout = layout
        return layout

    def update_header(self):
        """更新标题区域"""
        if not HAS_RICH or self.dashboard_layout is None:
            return
        header_text = Text.assemble(
            ("AI Agent Harness Dashboard", "bold blue"),
            (" | ", "white"),
            (f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "dim")
        )
        self.dashboard_layout["header"].update(Panel(header_text, style="blue"))

    def update_system_status_panel(self, controller_data: Dict[str, Any]):
        """更新系统状态面板"""
        if not HAS_RICH or self.dashboard_layout is None:
            status = controller_data.get("system_status", {})
            print(f"系统状态: Agents={status.get('total_agents', 0)}, "
                  f"Queued={status.get('queued_tasks', 0)}, "
                  f"Completed={status.get('completed_tasks', 0)}")
            return
        status = controller_data.get("system_status", {})
        table = Table(title="System Status", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="green")
        table.add_row("Total Agents", str(status.get("total_agents", 0)))
        table.add_row("Queued Tasks", str(status.get("queued_tasks", 0)))
        table.add_row("Completed Tasks", str(status.get("completed_tasks", 0)))
        table.add_row("Active Tasks", str(status.get("active_tasks", 0)))
        self.dashboard_layout["system_status"].update(table)

    def update_agent_overview_panel(self, controller_data: Dict[str, Any]):
        """更新代理概览面板"""
        if not HAS_RICH or self.dashboard_layout is None:
            return
        agents_info = controller_data.get("agents", {})
        table = Table(title="Agent Overview", show_header=True, header_style="bold green")
        table.add_column("Agent ID", style="yellow", width=15)
        table.add_column("Type", style="cyan")
        table.add_column("Status", style="green")
        for agent_id, info in agents_info.items():
            table.add_row(agent_id[:12] + "...", info.get("type", "Unknown"), "Active")
        self.dashboard_layout["agent_overview"].update(table)

    def update_performance_metrics_panel(self, performance_data: Dict[str, Any]):
        """更新性能指标面板"""
        if not HAS_RICH or self.dashboard_layout is None:
            return
        summary = self.monitor.generate_performance_summary()
        table = Table(title="Performance Metrics", show_header=True, header_style="bold red")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        for metric, value in summary.items():
            table.add_row(metric.replace("_", " ").title(), str(value))
        self.dashboard_layout["performance_metrics"].update(table)

    def update_recent_events_panel(self):
        """更新最近事件面板"""
        if not HAS_RICH or self.dashboard_layout is None:
            return
        recent_events = self.monitor.monitor_data["task_queue"][-10:]
        if recent_events:
            table = Table(title="Recent Events", show_header=True, header_style="bold yellow")
            table.add_column("Task ID", style="cyan", width=15)
            table.add_column("Event", style="green", width=15)
            table.add_column("Status", style="red", width=10)
            table.add_column("Time", style="dim", width=15)
            for event in reversed(recent_events):
                table.add_row(
                    event["task_id"][:8] + "...",
                    event["event_type"],
                    event["status"],
                    event["timestamp"][11:19]
                )
            self.dashboard_layout["recent_events"].update(table)
        else:
            self.dashboard_layout["recent_events"].update("No recent events")

    async def refresh_dashboard(self):
        """刷新仪表板数据"""
        mock_controller_data = {
            "system_status": {
                "total_agents": 3, "queued_tasks": 5,
                "completed_tasks": 15, "active_tasks": 2,
                "agents": {
                    "text_agent_1": {"type": "TextAgent"},
                    "browser_agent_1": {"type": "BrowserAgent"},
                    "search_agent_1": {"type": "SearchAgent"}
                }
            }
        }
        self.update_header()
        self.update_system_status_panel(mock_controller_data)
        self.update_agent_overview_panel(mock_controller_data)
        self.update_performance_metrics_panel({})
        self.update_recent_events_panel()

    async def run_live_dashboard(self):
        """运行实时仪表板"""
        if not HAS_RICH:
            print("实时仪表板需要 rich 库: pip install rich")
            return
        console = _get_console()
        console.print("[bold green]Starting AI Agent Harness Dashboard[/bold green]")
        console.print("[dim]Press Ctrl+C to exit[/dim]\n")
        self.create_dashboard_layout()
        with Live(self.dashboard_layout, refresh_per_second=1, screen=True) as live:
            self.is_running = True
            while self.is_running:
                try:
                    await self.refresh_dashboard()
                    await asyncio.sleep(2)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]仪表板更新错误: {e}[/red]")
                    await asyncio.sleep(5)
        console.print("[yellow]Dashboard stopped.[/yellow]")

    def generate_static_report(self):
        """生成静态报告"""
        report_data = {
            "generation_time": datetime.now().isoformat(),
            "system_summary": {
                "total_tests_run": 100, "successful_tests": 85,
                "failed_tests": 10, "pending_tests": 5,
                "average_execution_time": 3.2, "overall_success_rate": 0.85
            },
            "agent_performance": {
                "text_agent_1": {"score": 0.92, "tests_passed": 18, "tests_total": 20},
                "browser_agent_1": {"score": 0.78, "tests_passed": 15, "tests_total": 20},
                "search_agent_1": {"score": 0.88, "tests_passed": 17, "tests_total": 20}
            },
            "performance_trends": {
                "daily_success_rate": [0.8, 0.85, 0.82, 0.88, 0.9],
                "execution_times": [2.1, 2.3, 1.9, 2.0, 1.8]
            }
        }
        report_filename = f"reports/static_report_{int(datetime.now().timestamp())}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"静态报告已生成: {report_filename}")

        if HAS_MATPLOTLIB:
            visualization_data = {
                "performance": {
                    "success_rate_trend": {
                        "dates": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
                        "rates": [0.8, 0.85, 0.82, 0.88, 0.9]
                    },
                    "agent_comparison": report_data["agent_performance"],
                    "resource_usage": {"CPU": 45, "Memory": 60, "Network": 25, "Storage": 30}
                }
            }
            chart_filename = f"reports/performance_chart_{int(datetime.now().timestamp())}.png"
            self.visualizer.save_visualization(visualization_data, chart_filename)
        else:
            print("跳过图表生成（需要 matplotlib + seaborn）")

        return report_filename


def main():
    """主函数"""
    dashboard = InteractiveDashboard()
    parser = argparse.ArgumentParser(description="AI Agent Harness Dashboard")
    parser.add_argument("--mode", choices=["live", "static", "demo"], default="demo",
                       help="Dashboard mode")
    parser.add_argument("--generate-report", action="store_true", help="Generate static report")
    args = parser.parse_args()

    try:
        if args.mode == "live":
            asyncio.run(dashboard.run_live_dashboard())
        elif args.mode == "static" or args.generate_report:
            dashboard.generate_static_report()
        elif args.mode == "demo":
            print("AI Agent Harness Dashboard Demo")
            print("=" * 40)
            print(f"rich: {'可用' if HAS_RICH else '不可用 (pip install rich)'}")
            print(f"matplotlib: {'可用' if HAS_MATPLOTLIB else '不可用 (pip install matplotlib seaborn)'}")
            print()
            print("功能:")
            print("• 实时系统监控")
            print("• 代理性能可视化")
            print("• 交互式性能报告")
            print("• 历史数据分析")
            print()
            print("用法:")
            print("  python dashboard.py --mode live     # 实时仪表板")
            print("  python dashboard.py --mode static   # 生成静态报告")
            print("  python dashboard.py --generate-report  # 快速报告")
            print()
            sample = {"total_agents": 3, "queued_tasks": 7, "completed_tasks": 23, "active_tasks": 3}
            print("示例系统状态:")
            print("-" * 40)
            for k, v in sample.items():
                print(f"  {k}: {v}")
    except KeyboardInterrupt:
        print("\nDashboard stopped by user.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
