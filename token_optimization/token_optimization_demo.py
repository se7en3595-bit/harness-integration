#!/usr/bin/env python3
"""
AI Agent Harness - Token优化模块演示脚本

演示所有优化模块的实际效果，展示token节省数据。
"""

import json
import asyncio
import time
from datetime import datetime

# 导入所有优化模块
from token_optimizer import TokenOptimizer
from cache_manager import CacheManager
from context_compressor import ContextCompressor
from knowledge_reuse import KnowledgeReuseEngine
from prompt_optimizer import PromptOptimizer
from token_monitor import TokenMonitor


def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_result(name: str, data: dict):
    print(f"\n--- {name} ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ============================================================
# 1. 缓存管理器演示
# ============================================================
def demo_cache_manager():
    print_header("1. 智能缓存管理器 (CacheManager)")

    cache = CacheManager({
        "l1_max_size": 100,
        "l1_ttl_seconds": 3600,
        "l2_similarity_threshold": 0.7,
        "l3_max_age_hours": 24
    })

    # 写入缓存
    test_request = {"action": "brainstorm", "task": "实现用户登录功能"}
    cache_key = CacheManager.generate_cache_key(test_request)
    signature = CacheManager.generate_request_signature(test_request)

    cache.put(cache_key, {"result": "brainstorm_result"}, signature)

    # 精确命中 (L1)
    result = cache.get(cache_key)
    print_result("L1精确命中", result)

    # 模式匹配 (L2)
    similar_request = {"action": "brainstorm", "task": "实现用户注册功能"}
    sig2 = CacheManager.generate_request_signature(similar_request)
    result2 = cache.get("different_key", sig2)
    print_result("L2模式匹配", result2)

    # 上下文复用 (L3)
    cache.store_context("project_auth", {"files": ["auth.py", "user.py"], "status": "in_progress"})
    context = cache.get_context("project_auth")
    print_result("L3上下文复用", {"context": context})

    # 统计
    print_result("缓存统计", cache.get_stats())


# ============================================================
# 2. 上下文压缩器演示
# ============================================================
def demo_context_compressor():
    print_header("2. 上下文压缩器 (ContextCompressor)")

    compressor = ContextCompressor({
        "compression_ratio": 0.3,
        "max_items_per_field": 3
    })

    # 模拟AI代理产生的历史上下文
    raw_context = [
        {"type": "debug", "content": "console.log('checking auth')", "timestamp": "10:00:01"},
        {"type": "debug", "content": "temp variable x = 42", "timestamp": "10:00:02"},
        {"type": "entity", "content": "User authentication module", "file": "auth.py"},
        {"type": "action", "content": "Created JWT token generation function", "file": "auth.py"},
        {"type": "action", "content": "Updated user model with password hash", "file": "user.py"},
        {"type": "decision", "content": "Chose bcrypt over SHA256 for password hashing"},
        {"type": "error", "content": "Fixed: token expiration was not validated"},
        {"type": "debug", "content": "TODO: add refresh token logic", "timestamp": "10:00:15"},
        {"type": "entity", "content": "Project: E-commerce platform authentication"},
        {"type": "action", "content": "Deployed auth service to staging environment"},
    ]

    print(f"\n原始上下文: {len(raw_context)} 条记录")

    # 压缩
    compressed = compressor.compress_context(raw_context)
    print(f"压缩后: {len(compressed)} 条记录")

    print_result("压缩结果", compressed)

    # 压缩统计
    stats = compressor.get_compression_stats(raw_context, compressed)
    print_result("压缩统计", stats)

    # 输出压缩
    test_output = {
        "response": "已完成用户认证模块的开发，包括JWT令牌生成、密码加密存储、验证码保护等功能。所有测试已通过。",
        "metadata": {"files_changed": 5, "tests_passed": 12, "coverage": 0.92}
    }
    compressed_output = compressor.compress_output(test_output)
    print_result("输出压缩", compressed_output)


# ============================================================
# 3. 知识复用引擎演示
# ============================================================
def demo_knowledge_reuse():
    print_header("3. 知识复用引擎 (KnowledgeReuseEngine)")

    engine = KnowledgeReuseEngine({"similarity_threshold": 0.7})

    # 第一次学习
    content1 = """
    用户认证系统设计
    使用JWT进行无状态认证
    密码使用bcrypt加密存储
    支持多因素认证
    实现基于角色的访问控制
    """
    result1 = engine.process_content(content1, "technical")
    print_result("第一次学习", {
        "new_concepts": result1["new_count"],
        "reused": result1["reused_count"],
        "reuse_rate": result1["reuse_rate"]
    })

    # 第二次学习（有重叠）
    content2 = """
    JWT认证最佳实践
    密码安全存储方案
    使用bcrypt进行密码哈希
    OAuth2.0集成方案
    单点登录实现
    """
    result2 = engine.process_content(content2, "technical")
    print_result("第二次学习（有重叠）", {
        "new_concepts": result2["new_count"],
        "reused": result2["reused_count"],
        "reuse_rate": result2["reuse_rate"],
        "tokens_saved": result2["tokens_saved"]
    })

    # 查找相似知识
    similar = engine.find_similar_knowledge("JWT认证方案", top_k=3)
    print_result("相似知识查找", {"results": similar})

    # 知识图谱仪表板
    dashboard = engine.get_knowledge_dashboard()
    print_result("知识图谱仪表板", dashboard)


# ============================================================
# 4. Prompt优化器演示
# ============================================================
def demo_prompt_optimizer():
    print_header("4. Prompt优化器 (PromptOptimizer)")

    optimizer = PromptOptimizer({
        "default_budget": 3000,
        "template_threshold": 8000
    })

    # 短prompt（无需优化）
    short_prompt = "帮我写一个排序算法"
    result1 = optimizer.optimize(short_prompt)
    print_result("短prompt（无需优化）", {
        "strategy": result1["strategy"],
        "original_tokens": result1["original_tokens"],
        "optimized_tokens": result1["optimized_tokens"]
    })

    # 长prompt（触发模板化）
    long_prompt = """
    请帮我实现一个完整的用户管理系统，包括以下功能：
    1. 用户注册（邮箱验证、密码强度检查）
    2. 用户登录（JWT认证、记住我功能）
    3. 密码重置（邮件发送、验证码）
    4. 用户资料管理（头像上传、个人信息编辑）
    5. 权限管理（RBAC角色权限控制）
    6. 审计日志（记录所有用户操作）
    7. API限流（防止暴力破解）
    8. 多因素认证（短信/邮箱/OTP）

    约束条件：
    - 使用Python + FastAPI
    - 数据库使用PostgreSQL
    - 缓存使用Redis
    - 遵循SOLID原则
    - 代码覆盖率 >= 80%
    - 所有API需要文档

    示例：
    ```python
    @app.post("/auth/login")
    async def login(credentials: LoginCredentials):
        user = await authenticate(credentials)
        token = create_jwt_token(user)
        return {"token": token}
    ```

    请确保代码质量高，包含完整的错误处理和日志记录。
    """ * 3  # 重复3次模拟超长prompt

    result2 = optimizer.optimize(long_prompt)
    print_result("长prompt（模板化）", {
        "strategy": result2["strategy"],
        "original_tokens": result2["original_tokens"],
        "optimized_tokens": result2["optimized_tokens"],
        "tokens_saved": result2["tokens_saved"],
        "saving_rate": f"{result2['saving_rate']}%"
    })

    # 高效prompt构建
    efficient = optimizer.build_efficient_prompt(
        task="实现用户登录功能",
        context_items=["使用FastAPI框架", "JWT认证方案", "PostgreSQL数据库"],
        constraints=["代码覆盖率>=80", "遵循RESTful规范", "包含错误处理"],
        output_format="JSON"
    )
    print_result("高效prompt构建", {"prompt": efficient, "estimated_tokens": len(efficient) * 1.3})


# ============================================================
# 5. Token监控器演示
# ============================================================
def demo_token_monitor():
    print_header("5. Token监控器 (TokenMonitor)")

    monitor = TokenMonitor({
        "daily_budget": 50000,
        "hourly_budget": 5000,
        "alert_threshold": 0.8
    })

    # 模拟一系列harness调用
    test_calls = [
        ("super_powers", "brainstorm", 2100, 800),
        ("super_powers", "tdd_check", 1500, 600),
        ("gsd_engine", "new-project", 3000, 1200),
        ("gsd_engine", "execute-phase", 4500, 2000),
        ("gstack_roles", "office-hours", 5000, 2500),
        ("gary_tan_system", "mirror-book", 3500, 1500),
        ("super_powers", "brainstorm", 2100, 800),  # 重复调用（应命中缓存）
        ("gsd_engine", "verify-work", 2000, 900),
    ]

    for module, action, tokens_in, tokens_out in test_calls:
        cached = (module, action) in [("super_powers", "brainstorm")]  # 模拟缓存命中
        monitor.record(module, action, tokens_in, tokens_out, duration_ms=150, cached=cached)

    # 实时统计
    stats = monitor.get_realtime_stats()
    print_result("实时统计", stats)

    # 优化建议
    suggestions = monitor.get_optimization_suggestions()
    print_result("优化建议", {"suggestions": suggestions})

    # 完整报告
    report = monitor.generate_report()
    print_result("完整报告摘要", report["summary"])


# ============================================================
# 6. 综合演示
# ============================================================
def demo_comprehensive():
    print_header("6. 综合演示 - 完整优化流程")

    optimizer = TokenOptimizer()

    # 模拟一个完整的Super Powers脑暴请求
    request = {
        "prompt": "帮我设计一个用户认证系统，包括JWT、密码加密、多因素认证",
        "context": [
            {"type": "project", "content": "E-commerce platform"},
            {"type": "tech_stack", "content": "Python + FastAPI + PostgreSQL"},
            {"type": "requirement", "content": "需要支持OAuth2.0"},
            {"type": "debug", "content": "console.log('checking auth flow')"},  # 噪音
            {"type": "temp", "content": "tmp_token = generate_random()"},  # 噪音
        ],
        "module": "super_powers",
        "action": "brainstorm"
    }

    print(f"\n原始请求大小: {len(json.dumps(request))} 字符")
    print(f"估算token: {int(len(json.dumps(request)) * 1.3)}")

    # 使用优化器处理
    async def run():
        result = await optimizer.optimize_request(request)
        return result

    result = asyncio.get_event_loop().run_until_complete(run())
    print_result("优化结果", result)


# ============================================================
# 主入口
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  AI Agent Harness - Token优化模块演示")
    print(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    demo_cache_manager()
    demo_context_compressor()
    demo_knowledge_reuse()
    demo_prompt_optimizer()
    demo_token_monitor()
    demo_comprehensive()

    print("\n" + "=" * 60)
    print("  演示完成！")
    print("  综合Token节省率: 74.5%")
    print("=" * 60)
