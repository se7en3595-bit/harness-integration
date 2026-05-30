#!/usr/bin/env python3
"""
AI Agent Harness v0.8 - 牛马AI Skill主调用接口

整合四层工程约束 + 三层复利系统 + Token优化模块

使用方法:
    python harness_skill.py <module> <action> [params_json]

模块列表:
    super-powers  - Super Powers纪律引擎（7阶段状态机）
    gsd           - GSD上下文隔离引擎（6阶段项目管理）
    g-stack       - G-Stack多角色决策（基于关键词匹配评分）
    gar-tan       - Gar Tan三层复利系统（知识图谱积累）
    token         - Token优化模块
    monitor       - Token监控
    status        - 系统状态总览
"""

import sys
import json
import os
from datetime import datetime

# ============================================================
# 路径配置
# ============================================================
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(SKILL_DIR, "core")
TOKEN_OPT_DIR = os.path.join(SKILL_DIR, "token_optimization")


def _load_core_module(module_name: str):
    """动态加载 core/ 目录下的模块"""
    sys.path.insert(0, CORE_DIR)
    try:
        if module_name == "super_powers":
            from super_powers import SuperPowersEngine
            return SuperPowersEngine()
        elif module_name == "gsd_engine":
            from gsd_engine import GSDEngine
            return GSDEngine()
        elif module_name == "gstack_roles":
            from gstack_roles import GStackEngine
            return GStackEngine()
        elif module_name == "gary_tan_system":
            from gary_tan_system import GarTanSystem
            return GarTanSystem()
    except ImportError as e:
        return {"error": f"Failed to load core/{module_name}: {str(e)}"}
    finally:
        if CORE_DIR in sys.path:
            sys.path.remove(CORE_DIR)


def _load_token_module(module_name: str):
    """动态加载 token_optimization/ 目录下的模块"""
    sys.path.insert(0, TOKEN_OPT_DIR)
    try:
        if module_name == "token_optimizer":
            from token_optimizer import TokenOptimizer
            return TokenOptimizer()
        elif module_name == "cache_manager":
            from cache_manager import CacheManager
            return CacheManager()
        elif module_name == "context_compressor":
            from context_compressor import ContextCompressor
            return ContextCompressor()
        elif module_name == "knowledge_reuse":
            from knowledge_reuse import KnowledgeReuseEngine
            return KnowledgeReuseEngine()
        elif module_name == "prompt_optimizer":
            from prompt_optimizer import PromptOptimizer
            return PromptOptimizer()
        elif module_name == "token_monitor":
            from token_monitor import TokenMonitor
            return TokenMonitor()
    except ImportError as e:
        return {"error": f"Failed to load token_optimization/{module_name}: {str(e)}"}
    finally:
        if TOKEN_OPT_DIR in sys.path:
            sys.path.remove(TOKEN_OPT_DIR)


# ============================================================
# Super Powers - 第一层纪律引擎
# ============================================================
def call_super_powers(action: str, params: dict) -> dict:
    """调用 core/super_powers.py 的 SuperPowersEngine"""
    engine = _load_core_module("super_powers")
    if isinstance(engine, dict) and "error" in engine:
        return engine

    if action == "create-session":
        project_name = params.get("project", params.get("task", "Untitled"))
        description = params.get("description", "")
        session = engine.create_session(project_name, description)
        return {
            "module": "super-powers",
            "action": "create-session",
            "session_id": session.session_id,
            "project": project_name,
            "current_stage": session.get_current_stage_info(),
            "progress": session.get_progress()
        }

    elif action == "advance":
        session_id = params.get("session_id", "")
        session = engine.get_session(session_id)
        if not session:
            # 没有 session_id 时自动创建一个临时 session
            task = params.get("task", "Unnamed Task")
            session = engine.create_session(task)
        checklist_completed = params.get("checklist_completed", [])
        result = session.advance({"checklist_completed": checklist_completed})
        return {"module": "super-powers", "action": "advance", **result}

    elif action == "status":
        session_id = params.get("session_id", "")
        session = engine.get_session(session_id)
        if not session:
            return {
                "module": "super-powers",
                "action": "status",
                "sessions": engine.list_sessions(),
                "all_stages": engine.get_all_stages()
            }
        return {
            "module": "super-powers",
            "action": "status",
            "session_id": session_id,
            "progress": session.get_progress(),
            "current_stage": session.get_current_stage_info()
        }

    elif action == "list-stages":
        return {
            "module": "super-powers",
            "action": "list-stages",
            "stages": engine.get_all_stages()
        }

    elif action == "list-sessions":
        return {
            "module": "super-powers",
            "action": "list-sessions",
            "sessions": engine.list_sessions()
        }

    else:
        return {
            "error": f"Unknown action: {action}",
            "available": ["create-session", "advance", "status", "list-stages", "list-sessions"]
        }


# ============================================================
# GSD - 第二层上下文隔离
# ============================================================
def call_gsd(action: str, params: dict) -> dict:
    """调用 core/gsd_engine.py 的 GSDEngine"""
    engine = _load_core_module("gsd_engine")
    if isinstance(engine, dict) and "error" in engine:
        return engine

    if action == "new-project":
        name = params.get("name", "Untitled")
        description = params.get("description", "")
        project = engine.create_project(name, description)
        return {
            "module": "gsd",
            "action": "new-project",
            "project_id": project.project_id,
            "name": name,
            "progress": project.get_progress()
        }

    elif action == "execute-phase":
        project_id = params.get("project_id", "")
        task = params.get("task", "")
        command = params.get("command", "/gsd-execute-phase")

        project = engine.get_project(project_id)
        if not project:
            # 没有 project_id 时自动创建
            project = engine.create_project(task or "Auto Project")

        result = project.execute_command(command, {"task": task, **params})
        return {"module": "gsd", "action": "execute-phase", **result}

    elif action == "run-command":
        command = params.get("command", "")
        project_id = params.get("project_id", "")
        project = engine.get_project(project_id)
        if not project:
            return {"error": "project_id not found. Use new-project first."}
        result = project.execute_command(command, params)
        return {"module": "gsd", "action": "run-command", **result}

    elif action == "status":
        project_id = params.get("project_id", "")
        project = engine.get_project(project_id)
        if not project:
            return {
                "module": "gsd",
                "action": "status",
                "projects": engine.list_projects()
            }
        return {
            "module": "gsd",
            "action": "status",
            "project_id": project_id,
            "progress": project.get_progress()
        }

    elif action == "list-projects":
        return {
            "module": "gsd",
            "action": "list-projects",
            "projects": engine.list_projects()
        }

    else:
        return {
            "error": f"Unknown action: {action}",
            "available": ["new-project", "execute-phase", "run-command", "status", "list-projects"]
        }


# ============================================================
# G-Stack - 第三层多角色决策
# ============================================================
def call_g_stack(action: str, params: dict) -> dict:
    """调用 core/gstack_roles.py 的 GStackEngine"""
    engine = _load_core_module("gstack_roles")
    if isinstance(engine, dict) and "error" in engine:
        return engine

    if action == "office-hours":
        topic = params.get("topic", "")
        roles_param = params.get("roles", "")
        content = params.get("content", "")

        if roles_param:
            participants = [r.strip() for r in roles_param.split(",")]
        else:
            # 根据 topic 自动推荐角色
            participants = engine.recommend_roles(topic)

        result = engine.conduct_office_hours(topic, participants, content)
        return {"module": "g-stack", "action": "office-hours", **result}

    elif action == "recommend-roles":
        topic = params.get("topic", "")
        recommended = engine.recommend_roles(topic)
        return {
            "module": "g-stack",
            "action": "recommend-roles",
            "topic": topic,
            "recommended_roles": recommended
        }

    elif action == "list-roles":
        all_roles = engine.get_all_roles()
        by_category = {}
        for role_id, role_def in all_roles.items():
            cat = role_def.get("category", "other")
            by_category.setdefault(cat, []).append(role_id)
        return {
            "module": "g-stack",
            "action": "list-roles",
            "total": len(all_roles),
            "by_category": by_category
        }

    elif action == "history":
        return {
            "module": "g-stack",
            "action": "history",
            "history": engine.get_history()
        }

    else:
        return {
            "error": f"Unknown action: {action}",
            "available": ["office-hours", "recommend-roles", "list-roles", "history"]
        }


# ============================================================
# Gar Tan - 三层复利系统
# ============================================================
def call_gar_tan(action: str, params: dict) -> dict:
    """调用 core/gary_tan_system.py 的 GarTanSystem"""
    system = _load_core_module("gary_tan_system")
    if isinstance(system, dict) and "error" in system:
        return system

    if action == "mirror-book":
        title = params.get("title", "")
        content = params.get("content", "")
        if not title:
            return {"error": "title is required"}
        result = system.mirror_book(title, content)
        return {"module": "gar-tan", "action": "mirror-book", **result}

    elif action == "analyze-meeting":
        transcript = params.get("transcript", "")
        participants_raw = params.get("participants", "")
        if isinstance(participants_raw, str):
            participants = [p.strip() for p in participants_raw.split(",") if p.strip()]
        else:
            participants = participants_raw
        result = system.analyze_meeting(transcript, participants)
        return {"module": "gar-tan", "action": "analyze-meeting", **result}

    elif action == "query":
        query = params.get("query", "")
        if not query:
            return {"error": "query is required"}
        result = system.query_knowledge(query)
        return {"module": "gar-tan", "action": "query", **result}

    elif action == "dashboard":
        result = system.get_system_dashboard()
        return {"module": "gar-tan", "action": "dashboard", **result}

    else:
        return {
            "error": f"Unknown action: {action}",
            "available": ["mirror-book", "analyze-meeting", "query", "dashboard"]
        }


# ============================================================
# Token优化模块
# ============================================================
def call_token(action: str, params: dict) -> dict:
    """Token优化模块接口"""
    if action == "optimize-prompt":
        optimizer = _load_token_module("prompt_optimizer")
        if isinstance(optimizer, dict) and "error" in optimizer:
            return optimizer
        prompt = params.get("prompt", "")
        budget = params.get("budget", 5000)
        result = optimizer.optimize(prompt, budget=budget)
        return {"module": "token", "action": "optimize-prompt", "result": result}

    elif action == "compress-context":
        compressor = _load_token_module("context_compressor")
        if isinstance(compressor, dict) and "error" in compressor:
            return compressor
        context = params.get("context", [])
        compressed = compressor.compress_context(context)
        stats = compressor.get_compression_stats(context, compressed)
        return {"module": "token", "action": "compress-context", "compressed": compressed, "stats": stats}

    elif action == "cache-stats":
        cache = _load_token_module("cache_manager")
        if isinstance(cache, dict) and "error" in cache:
            return cache
        return {"module": "token", "action": "cache-stats", "stats": cache.get_stats()}

    elif action == "status":
        return {
            "module": "token",
            "action": "status",
            "components": {
                "cache_manager": "三级智能缓存 (L1 LRU + L2模式 + L3上下文)",
                "context_compressor": "上下文压缩器 (去噪+提取+编码)",
                "knowledge_reuse": "知识复用引擎 (Jaccard相似度匹配)",
                "prompt_optimizer": "Prompt优化器 (智能截断+模板化)",
                "token_monitor": "Token监控器 (实时统计+告警)"
            }
        }

    else:
        return {
            "error": f"Unknown action: {action}",
            "available": ["optimize-prompt", "compress-context", "cache-stats", "status"]
        }


# ============================================================
# Token监控
# ============================================================
def call_monitor(action: str, params: dict) -> dict:
    """Token监控接口"""
    monitor = _load_token_module("token_monitor")
    if isinstance(monitor, dict) and "error" in monitor:
        return monitor

    if action == "stats":
        return {"module": "monitor", "action": "stats", "stats": monitor.get_realtime_stats()}

    elif action == "record":
        module = params.get("module", "unknown")
        act = params.get("action", "unknown")
        tokens_in = params.get("tokens_in", 0)
        tokens_out = params.get("tokens_out", 0)
        monitor.record(module, act, tokens_in, tokens_out)
        return {
            "module": "monitor",
            "action": "record",
            "result": f"已记录: {module}/{act} ({tokens_in + tokens_out} tokens)"
        }

    elif action == "suggestions":
        return {"module": "monitor", "action": "suggestions", "suggestions": monitor.get_optimization_suggestions()}

    elif action == "report":
        return {"module": "monitor", "action": "report", "report": monitor.generate_report()}

    else:
        return {"error": f"Unknown action: {action}", "available": ["stats", "record", "suggestions", "report"]}


# ============================================================
# 系统状态总览
# ============================================================
def get_system_status() -> dict:
    """获取完整系统状态"""
    return {
        "system": "AI Agent Harness",
        "version": "0.8.0",
        "timestamp": datetime.now().isoformat(),
        "layers": {
            "layer1_super_powers": {
                "name": "Super Powers - 编程纪律",
                "status": "active",
                "implementation": "真实7阶段状态机，硬门禁强制执行",
                "stages": 7
            },
            "layer2_gsd": {
                "name": "GSD - 上下文隔离",
                "status": "active",
                "implementation": "真实6阶段项目管理，上下文隔离记录",
                "phases": 6
            },
            "layer3_gstack": {
                "name": "G-Stack - 多角色决策",
                "status": "active",
                "implementation": "基于关键词匹配的角色评分，非AI调用",
                "roles": 24
            },
            "layer4_gar_tan": {
                "name": "Gar Tan - 三层复利",
                "status": "active",
                "implementation": "真实内存知识图谱，Jaccard相似度搜索",
                "components": ["ThinShellScheduler", "SkillifyEngine", "BrainDataManager"]
            }
        },
        "token_optimization": {
            "status": "active",
            "components": {
                "cache_manager": "LRU + 模式匹配 + 上下文复用三级缓存",
                "context_compressor": "去噪+关键状态提取",
                "knowledge_reuse": "Jaccard相似度知识复用",
                "prompt_optimizer": "智能截断+模板化",
                "token_monitor": "实时统计+告警"
            }
        }
    }


# ============================================================
# 主路由
# ============================================================
def call_harness(module: str, action: str, params: dict = None) -> dict:
    """统一调用入口"""
    params = params or {}

    router = {
        "super-powers": call_super_powers,
        "gsd": call_gsd,
        "g-stack": call_g_stack,
        "gar-tan": call_gar_tan,
        "token": call_token,
        "monitor": call_monitor,
    }

    if module == "status":
        return get_system_status()

    handler = router.get(module)
    if handler:
        return handler(action, params)
    else:
        return {
            "error": f"Unknown module: {module}",
            "available_modules": list(router.keys()) + ["status"]
        }


# ============================================================
# CLI入口
# ============================================================
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python harness_skill.py <module> <action> [params_json]",
            "modules": ["super-powers", "gsd", "g-stack", "gar-tan", "token", "monitor", "status"],
            "examples": [
                'python harness_skill.py super-powers create-session \'{"project": "实现登录"}\'',
                'python harness_skill.py gsd new-project \'{"name": "用户系统重构"}\'',
                'python harness_skill.py g-stack office-hours \'{"topic": "API设计"}\'',
                'python harness_skill.py gar-tan mirror-book \'{"title": "书名", "content": "内容"}\'',
                'python harness_skill.py status'
            ]
        }, indent=2, ensure_ascii=False))
        return

    module = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "status"
    params = {}

    if len(sys.argv) > 3:
        try:
            params = json.loads(sys.argv[3])
        except json.JSONDecodeError:
            params = {"raw_input": sys.argv[3]}

    result = call_harness(module, action, params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
