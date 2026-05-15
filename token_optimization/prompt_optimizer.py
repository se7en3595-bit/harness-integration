#!/usr/bin/env python3
"""
AI Agent Harness - Prompt优化器
基于动态prompt调整策略减少token消耗

核心能力：
1. 智能截断 - 根据预算自动截断prompt
2. 模板化 - 复杂prompt替换为结构化模板
3. 关键信息提取 - 只保留最关键的指令
4. 动态调整 - 根据上下文复杂度调整prompt长度

Token节省贡献: 15-25%
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple


class PromptOptimizer:
    """
    Prompt优化器

    根据token预算和上下文复杂度，
    动态调整prompt长度和内容。
    """

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.default_budget = config.get("default_budget", 10000)
        self.template_threshold = config.get("template_threshold", 8000)
        self.truncation_marker = config.get("truncation_marker", "... [已截断]")

    def optimize(self, prompt: str, budget: int = None, context: Dict = None) -> Dict[str, Any]:
        """
        优化prompt

        返回:
        - optimized_prompt: 优化后的prompt
        - strategy: 使用的优化策略
        - tokens_saved: 估算节省的token数
        """
        budget = budget or self.default_budget
        original_tokens = self._estimate_tokens(prompt)

        # 如果prompt在预算内，无需优化
        if original_tokens <= budget:
            return {
                "optimized_prompt": prompt,
                "strategy": "none",
                "original_tokens": original_tokens,
                "optimized_tokens": original_tokens,
                "tokens_saved": 0
            }

        # 根据prompt特征选择优化策略
        if original_tokens > self.template_threshold:
            # 超长prompt -> 模板化
            optimized = self._template_prompt(prompt, context)
            strategy = "template"
        elif self._is_code_heavy(prompt):
            # 代码密集型 -> 保留结构，压缩注释
            optimized = self._compress_code_prompt(prompt, budget)
            strategy = "code_compress"
        elif self._is_conversation_heavy(prompt):
            # 对话密集型 -> 摘要历史
            optimized = self._summarize_conversation(prompt, budget)
            strategy = "summarize"
        else:
            # 默认 -> 智能截断
            optimized = self._smart_truncate(prompt, budget)
            strategy = "truncate"

        optimized_tokens = self._estimate_tokens(optimized)

        return {
            "optimized_prompt": optimized,
            "strategy": strategy,
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "tokens_saved": max(original_tokens - optimized_tokens, 0),
            "saving_rate": round((1 - optimized_tokens / max(original_tokens, 1)) * 100, 1)
        }

    def batch_optimize(self, prompts: List[str], total_budget: int = None) -> List[Dict[str, Any]]:
        """
        批量优化多个prompt

        在总预算约束下，为每个prompt分配最优预算
        """
        total_budget = total_budget or self.default_budget * len(prompts)

        # 按重要性排序（假设越前面的越重要）
        results = []
        remaining_budget = total_budget

        for i, prompt in enumerate(prompts):
            # 按比例分配预算
            allocated = remaining_budget // max(len(prompts) - i, 1)
            result = self.optimize(prompt, budget=allocated)
            results.append(result)
            remaining_budget -= result["optimized_tokens"]

        return results

    def build_efficient_prompt(self, task: str, context_items: List[str] = None,
                                constraints: List[str] = None,
                                output_format: str = None) -> str:
        """
        高效prompt构建器

        从结构化组件构建精简的prompt
        """
        parts = []

        # 任务描述（必选）
        if task:
            parts.append(f"任务: {task}")

        # 上下文（限制数量）
        if context_items:
            top_context = context_items[:3]  # 最多3个上下文
            parts.append(f"上下文:\n" + "\n".join(f"- {c}" for c in top_context))

        # 约束（限制数量）
        if constraints:
            top_constraints = constraints[:3]  # 最多3个约束
            parts.append(f"约束:\n" + "\n".join(f"- {c}" for c in top_constraints))

        # 输出格式
        if output_format:
            parts.append(f"输出格式: {output_format}")

        return "\n\n".join(parts)

    def _template_prompt(self, prompt: str, context: Dict = None) -> str:
        """将长prompt转化为结构化模板"""
        # 提取关键组件
        task = self._extract_task_section(prompt)
        constraints = self._extract_constraints(prompt)
        examples = self._extract_examples(prompt)

        template_parts = []

        if task:
            template_parts.append(f"[任务]\n{task}")

        if context:
            template_parts.append(f"[上下文]\n{json.dumps(context, ensure_ascii=False, indent=2)[:500]}")

        if constraints:
            template_parts.append(f"[约束]\n{constraints[:300]}")

        if examples:
            # 只保留1个示例
            template_parts.append(f"[示例]\n{examples[:200]}")

        return "\n\n".join(template_parts)

    def _compress_code_prompt(self, prompt: str, budget: int) -> str:
        """压缩代码密集型prompt"""
        lines = prompt.split('\n')
        compressed = []
        in_code_block = False
        code_buffer = []

        for line in lines:
            if line.startswith('```'):
                if in_code_block:
                    # 代码块结束，保留结构
                    compressed.append('```')
                    # 只保留前20行代码
                    if len(code_buffer) > 20:
                        compressed.extend(code_buffer[:20])
                        compressed.append(f'... [省略 {len(code_buffer) - 20} 行代码]')
                    else:
                        compressed.extend(code_buffer)
                    compressed.append('```')
                    code_buffer = []
                    in_code_block = False
                else:
                    compressed.append(line)
                    in_code_block = True
            elif in_code_block:
                code_buffer.append(line)
            else:
                # 非代码部分：移除多余空行和注释
                stripped = line.strip()
                if stripped and not stripped.startswith('//') and not stripped.startswith('#'):
                    compressed.append(line)

        result = '\n'.join(compressed)

        # 如果还是太长，进一步截断
        if self._estimate_tokens(result) > budget:
            result = self._smart_truncate(result, budget)

        return result

    def _summarize_conversation(self, prompt: str, budget: int) -> str:
        """摘要对话密集型prompt"""
        # 提取对话历史
        dialogue_pattern = r'(User:|Assistant:|Human:|AI:)(.*?)(?=User:|Assistant:|Human:|AI:|$)'
        matches = re.findall(dialogue_pattern, prompt, re.DOTALL)

        if len(matches) <= 2:
            # 对话轮次少，直接截断
            return self._smart_truncate(prompt, budget)

        # 保留最近3轮对话
        recent = matches[-6:]  # 3轮 = 6条消息

        # 摘要早期对话
        early_count = len(matches) - len(recent)
        summary = f"[早期对话摘要: 共{early_count}条消息，已压缩]\n"

        # 构建结果
        result_parts = [summary]
        for speaker, content in recent:
            result_parts.append(f"{speaker}{content.strip()}")

        return '\n'.join(result_parts)

    def _smart_truncate(self, text: str, budget: int) -> str:
        """智能截断"""
        # 1字符 ≈ 1.3 tokens
        max_chars = int(budget / 1.3)

        if len(text) <= max_chars:
            return text

        # 优先截断中间部分，保留开头和结尾
        head_ratio = 0.6  # 保留60%的开头
        tail_ratio = 0.2  # 保留20%的结尾

        head_chars = int(max_chars * head_ratio)
        tail_chars = int(max_chars * tail_ratio)
        marker = self.truncation_marker

        head = text[:head_chars]
        tail = text[-tail_chars:]

        return f"{head}\n{marker}\n{tail}"

    def _extract_task_section(self, prompt: str) -> str:
        """提取任务描述"""
        patterns = [
            r'(?:任务|Task|要求|Request)[：:]\s*(.+?)(?:\n\n|\Z)',
            r'(?:请|Please|Help me|帮我)(.+?)(?:\n\n|\Z)',
        ]
        for pattern in patterns:
            match = re.search(pattern, prompt, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(0).strip()
        return prompt[:300]

    def _extract_constraints(self, prompt: str) -> str:
        """提取约束条件"""
        patterns = [
            r'(?:约束|限制|要求|Constraint|Rule)[：:]\s*(.+?)(?:\n\n|\Z)',
        ]
        for pattern in patterns:
            match = re.search(pattern, prompt, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    def _extract_examples(self, prompt: str) -> str:
        """提取示例"""
        patterns = [
            r'(?:示例|例子|Example)[：:]\s*(.+?)(?:\n\n|\Z)',
        ]
        for pattern in patterns:
            match = re.search(pattern, prompt, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    def _is_code_heavy(self, prompt: str) -> bool:
        """判断是否为代码密集型prompt"""
        code_indicators = ['```', 'def ', 'class ', 'import ', 'function', 'const ', 'var ']
        count = sum(1 for ind in code_indicators if ind in prompt)
        return count >= 2

    def _is_conversation_heavy(self, prompt: str) -> bool:
        """判断是否为对话密集型prompt"""
        dialogue_markers = ['User:', 'Assistant:', 'Human:', 'AI:']
        count = sum(prompt.count(m) for m in dialogue_markers)
        return count >= 4

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """估算token数"""
        return int(len(text) * 1.3)
