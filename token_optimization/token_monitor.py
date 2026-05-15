#!/usr/bin/env python3
"""
AI Agent Harness - Token监控器
实时监控token消耗，提供分析和优化建议

核心能力：
1. 实时token计数 - 每次调用精确统计
2. 消耗趋势分析 - 追踪token使用趋势
3. 预算告警 - 超预算时自动告警
4. 优化建议 - 基于使用模式给出优化建议
5. 报告生成 - 生成token使用报告
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict


class TokenUsageRecord:
    """单次token使用记录"""

    def __init__(self, module: str, action: str, tokens_in: int, tokens_out: int,
                 duration_ms: float = 0, cached: bool = False):
        self.module = module
        self.action = action
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out
        self.total_tokens = tokens_in + tokens_out
        self.duration_ms = duration_ms
        self.cached = cached
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "action": self.action,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "total_tokens": self.total_tokens,
            "duration_ms": self.duration_ms,
            "cached": self.cached,
            "timestamp": self.timestamp.isoformat()
        }


class TokenMonitor:
    """
    Token监控器

    监控所有harness模块的token消耗，
    提供实时统计、趋势分析和优化建议。
    """

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.daily_budget = config.get("daily_budget", 100000)
        self.hourly_budget = config.get("hourly_budget", 10000)
        self.alert_threshold = config.get("alert_threshold", 0.8)  # 80%触发告警
        self.records: List[TokenUsageRecord] = []
        self.module_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"tokens_in": 0, "tokens_out": 0, "calls": 0, "cached_calls": 0}
        )
        self.alerts: List[Dict[str, Any]] = []

    def record(self, module: str, action: str, tokens_in: int, tokens_out: int,
               duration_ms: float = 0, cached: bool = False):
        """记录一次token使用"""
        record = TokenUsageRecord(module, action, tokens_in, tokens_out, duration_ms, cached)
        self.records.append(record)

        # 更新模块统计
        stats = self.module_stats[module]
        stats["tokens_in"] += tokens_in
        stats["tokens_out"] += tokens_out
        stats["calls"] += 1
        if cached:
            stats["cached_calls"] += 1

        # 检查告警
        self._check_alerts()

    def get_realtime_stats(self) -> Dict[str, Any]:
        """获取实时统计"""
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)

        recent_hour = [r for r in self.records if r.timestamp > one_hour_ago]
        recent_day = [r for r in self.records if r.timestamp > one_day_ago]

        hour_tokens = sum(r.total_tokens for r in recent_hour)
        day_tokens = sum(r.total_tokens for r in recent_day)

        return {
            "total_records": len(self.records),
            "total_tokens": sum(r.total_tokens for r in self.records),
            "last_hour": {
                "tokens": hour_tokens,
                "calls": len(recent_hour),
                "budget_usage": round(hour_tokens / max(self.hourly_budget, 1), 2),
                "remaining": max(self.hourly_budget - hour_tokens, 0)
            },
            "last_24h": {
                "tokens": day_tokens,
                "calls": len(recent_day),
                "budget_usage": round(day_tokens / max(self.daily_budget, 1), 2),
                "remaining": max(self.daily_budget - day_tokens, 0)
            },
            "cache_hit_rate": self._calc_cache_hit_rate(),
            "avg_tokens_per_call": self._calc_avg_tokens(),
            "module_breakdown": {
                module: {
                    "total_tokens": s["tokens_in"] + s["tokens_out"],
                    "calls": s["calls"],
                    "cache_hit_rate": round(s["cached_calls"] / max(s["calls"], 1), 2),
                    "avg_per_call": round((s["tokens_in"] + s["tokens_out"]) / max(s["calls"], 1))
                }
                for module, s in self.module_stats.items()
            }
        }

    def get_trend(self, periods: int = 10) -> List[Dict[str, Any]]:
        """
        获取token消耗趋势

        将历史记录分成若干时间段，展示趋势变化
        """
        if not self.records:
            return []

        # 按时间分桶
        min_time = self.records[0].timestamp
        max_time = self.records[-1].timestamp
        time_range = (max_time - min_time).total_seconds()

        if time_range <= 0:
            return [{
                "period": 0,
                "tokens": sum(r.total_tokens for r in self.records),
                "calls": len(self.records),
                "timestamp": max_time.isoformat()
            }]

        bucket_size = time_range / periods
        buckets: List[List[TokenUsageRecord]] = [[] for _ in range(periods)]

        for record in self.records:
            idx = min(int((record.timestamp - min_time).total_seconds() / bucket_size), periods - 1)
            buckets[idx].append(record)

        trend = []
        for i, bucket in enumerate(buckets):
            if bucket:
                trend.append({
                    "period": i,
                    "tokens": sum(r.total_tokens for r in bucket),
                    "calls": len(bucket),
                    "cached_calls": sum(1 for r in bucket if r.cached),
                    "avg_tokens": round(sum(r.total_tokens for r in bucket) / len(bucket)),
                    "timestamp": bucket[-1].timestamp.isoformat()
                })

        return trend

    def get_optimization_suggestions(self) -> List[Dict[str, str]]:
        """基于使用模式生成优化建议"""
        suggestions = []

        # 1. 检查缓存命中率
        cache_rate = self._calc_cache_hit_rate()
        if cache_rate < 0.3:
            suggestions.append({
                "category": "缓存优化",
                "priority": "高",
                "suggestion": "缓存命中率低于30%，建议增加缓存容量或调整缓存策略",
                "potential_saving": "20-30%"
            })

        # 2. 检查高频高消耗模块
        for module, stats in self.module_stats.items():
            avg = (stats["tokens_in"] + stats["tokens_out"]) / max(stats["calls"], 1)
            if avg > 5000:
                suggestions.append({
                    "category": "模块优化",
                    "priority": "高",
                    "suggestion": f"模块 '{module}' 平均每次调用 {avg:.0f} tokens，建议检查prompt长度",
                    "potential_saving": "15-25%"
                })

        # 3. 检查重复调用
        action_counts = defaultdict(int)
        for r in self.records:
            action_counts[(r.module, r.action)] += 1

        for (module, action), count in action_counts.items():
            if count > 10:
                suggestions.append({
                    "category": "重复调用",
                    "priority": "中",
                    "suggestion": f"'{module}/{action}' 被调用了 {count} 次，建议缓存结果",
                    "potential_saving": "10-20%"
                })

        # 4. 检查预算使用情况
        stats = self.get_realtime_stats()
        if stats["last_hour"]["budget_usage"] > 0.8:
            suggestions.append({
                "category": "预算告警",
                "priority": "紧急",
                "suggestion": f"过去1小时已使用 {stats['last_hour']['budget_usage']*100:.0f}% 的预算",
                "potential_saving": "立即优化"
            })

        if not suggestions:
            suggestions.append({
                "category": "状态良好",
                "priority": "低",
                "suggestion": "当前token使用效率良好，继续保持",
                "potential_saving": "N/A"
            })

        return suggestions

    def generate_report(self) -> Dict[str, Any]:
        """生成完整token使用报告"""
        return {
            "report_generated_at": datetime.now().isoformat(),
            "realtime_stats": self.get_realtime_stats(),
            "trend": self.get_trend(),
            "suggestions": self.get_optimization_suggestions(),
            "alerts": self.alerts[-10:],  # 最近10条告警
            "summary": {
                "total_tokens_consumed": sum(r.total_tokens for r in self.records),
                "total_api_calls": len(self.records),
                "total_cached_calls": sum(1 for r in self.records if r.cached),
                "overall_cache_hit_rate": self._calc_cache_hit_rate(),
                "estimated_cost_saved": self._estimate_cost_saved()
            }
        }

    def _check_alerts(self):
        """检查是否需要触发告警"""
        stats = self.get_realtime_stats()

        # 小时预算告警
        if stats["last_hour"]["budget_usage"] >= self.alert_threshold:
            self.alerts.append({
                "type": "hourly_budget",
                "level": "warning" if stats["last_hour"]["budget_usage"] < 0.95 else "critical",
                "message": f"小时token使用率达 {stats['last_hour']['budget_usage']*100:.0f}%",
                "timestamp": datetime.now().isoformat()
            })

        # 日预算告警
        if stats["last_24h"]["budget_usage"] >= self.alert_threshold:
            self.alerts.append({
                "type": "daily_budget",
                "level": "warning" if stats["last_24h"]["budget_usage"] < 0.95 else "critical",
                "message": f"日token使用率达 {stats['last_24h']['budget_usage']*100:.0f}%",
                "timestamp": datetime.now().isoformat()
            })

    def _calc_cache_hit_rate(self) -> float:
        total = len(self.records)
        if total == 0:
            return 0.0
        cached = sum(1 for r in self.records if r.cached)
        return round(cached / total, 2)

    def _calc_avg_tokens(self) -> float:
        if not self.records:
            return 0.0
        return round(sum(r.total_tokens for r in self.records) / len(self.records))

    def _estimate_cost_saved(self) -> Dict[str, Any]:
        """估算节省的成本"""
        cached_calls = sum(1 for r in self.records if r.cached)
        avg_tokens = self._calc_avg_tokens()
        # 假设 $0.002 per 1K tokens (参考Claude定价)
        cost_per_token = 0.002 / 1000

        saved_tokens = cached_calls * avg_tokens
        saved_cost = saved_tokens * cost_per_token

        return {
            "cached_calls": cached_calls,
            "estimated_tokens_saved": int(saved_tokens),
            "estimated_cost_saved_usd": round(saved_cost, 4)
        }

    def reset(self):
        """重置所有统计数据"""
        self.records.clear()
        self.module_stats.clear()
        self.alerts.clear()
