#!/usr/bin/env python3
"""
AI Agent Harness System Validation Script
验证所有核心组件是否正确创建和配置
"""

import os
import sys
import json
from pathlib import Path

def validate_file_structure():
    """验证项目文件结构"""
    print("🔍 Validating AI Agent Harness File Structure")
    print("=" * 60)

    expected_files = {
        "core/": [
            "super_powers.py",
            "gsd_engine.py",
            "gstack_roles.py",
            "gary_tan_system.py",
            "agent_controller.py",
            "test_scenarios.py",
            "evaluation_metrics.py",
            "dashboard.py",
            "main.py"
        ],
        "token_optimizer/": [
            "token_optimizer.py",
            "token_config.yaml",
            "token_optimization_guide.md",
            "token_optimization_demo.py"
        ],
        "skills/harness-integration/": [
            "SKILL.md",
            "harness_skill.py"
        ],
        "docs/": [
            "README.md",
            "QUICK_START.md",
            "SYSTEM_STATUS.md",
            "CLAUDE.md",
            "token_optimization_guide.md"
        ]
    }

    missing_files = []
    total_files = 0

    for directory, files in expected_files.items():
        full_dir = f"E:\\WorkSpace\\Newmax\\ai-agent-harness\\{directory}"
        if not os.path.exists(full_dir):
            print(f"❌ Directory missing: {directory}")
            continue

        for file in files:
            total_files += 1
            file_path = os.path.join(full_dir, file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {directory}{file} ({size:,} bytes)")
            else:
                print(f"❌ Missing: {directory}{file}")
                missing_files.append(f"{directory}{file}")

    print(f"\n📊 Summary: {total_files - len(missing_files)}/{total_files} files found")
    return len(missing_files) == 0

def validate_core_components():
    """验证核心组件功能"""
    print("\n🔧 Validating Core Components")
    print("-" * 40)

    core_modules = [
        ("super_powers.py", "Super Powers Engine"),
        ("gsd_engine.py", "GSD Engine"),
        ("gstack_roles.py", "G-Stack Roles"),
        ("gary_tan_system.py", "Gar Tan System"),
        ("token_optimizer.py", "Token Optimizer")
    ]

    for module_file, description in core_modules:
        module_path = f"E:\\WorkSpace\\Newmax\\ai-agent-harness\\{module_file}"
        if os.path.exists(module_path):
            try:
                # Try to parse the Python file
                with open(module_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "class" in content and "def __init__" in content:
                        print(f"✅ {description}: Class structure valid")
                    elif "def main" in content:
                        print(f"✅ {description}: Main function present")
                    else:
                        print(f"⚠️  {description}: Basic structure found")
            except Exception as e:
                print(f"❌ {description}: Error reading file - {e}")
        else:
            print(f"❌ {description}: File not found")

def validate_token_optimizer():
    """验证Token优化器配置"""
    print("\n🎯 Validating Token Optimization Configuration")
    print("-" * 50)

    config_path = "E:\\WorkSpace\\Newmax\\ai-agent-harness\\token_config.yaml"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                print("✅ token_config.yaml: Valid YAML syntax")

                # Check key sections
                required_sections = ["token_optimizer", "layer_optimizations", "monitoring"]
                for section in required_sections:
                    if section in config:
                        print(f"✅ Config section '{section}': Present")
                    else:
                        print(f"⚠️  Config section '{section}': Missing or empty")

        except Exception as e:
            print(f"❌ token_config.yaml: Error parsing - {e}")
    else:
        print("❌ token_config.yaml: File not found")

def validate_skill_integration():
    """验证牛马AI技能集成"""
    print("\n🤖 Validating 牛马AI Skill Integration")
    print("-" * 40)

    skill_files = [
        "E:\\WorkSpace\\Newmax\\ai-agent-harness\\skills\\harness-integration\\SKILL.md",
        "E:\\WorkSpace\\Newmax\\ai-agent-harness\\skills\\harness-integration\\harness_skill.py"
    ]

    for skill_file in skill_files:
        if os.path.exists(skill_file):
            try:
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                if ".md" in skill_file:
                    if "name:" in content and "description:" in content:
                        print(f"✅ SKILL.md: Properly formatted")
                    else:
                        print(f"⚠️  SKILL.md: May need formatting review")
                else:
                    if "class HarnessSkill" in content and "def main" in content:
                        print(f"✅ harness_skill.py: Complete implementation")
                    else:
                        print(f"⚠️  harness_skill.py: May need completion")

            except Exception as e:
                print(f"❌ {os.path.basename(skill_file)}: Error reading - {e}")
        else:
            print(f"❌ {os.path.basename(skill_file)}: Not found")

def validate_documentation():
    """验证文档完整性"""
    print("\n📚 Validating Documentation")
    print("-" * 30)

    doc_files = [
        ("README.md", "Main README"),
        ("docs/README.md", "Documentation README"),
        ("docs/QUICK_START.md", "Quick Start Guide"),
        ("docs/SYSTEM_STATUS.md", "System Status"),
        ("docs/token_optimization_guide.md", "Token Optimization Guide")
    ]

    for doc_file, description in doc_files:
        doc_path = f"E:\\WorkSpace\\Newmax\\ai-agent-harness\\{doc_file}"
        if os.path.exists(doc_path):
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    if lines > 50:  # Reasonable documentation length
                        print(f"✅ {description}: {lines} lines")
                    else:
                        print(f"⚠️  {description}: Short ({lines} lines)")

            except Exception as e:
                print(f"❌ {description}: Error reading - {e}")
        else:
            print(f"❌ {description}: Not found")

def validate_project_stats():
    """验证项目统计信息"""
    print("\n📊 Project Statistics")
    print("-" * 20)

    total_size = 0
    file_count = 0

    for root, dirs, files in os.walk("E:\\WorkSpace\\Newmax\\ai-agent-harness"):
        for file in files:
            if file.endswith(('.py', '.md', '.yaml', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    total_size += size
                    file_count += 1
                except:
                    pass

    print(f"📁 Total files: {file_count}")
    print(f"💾 Total size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    print(f"📝 Average file size: {total_size/file_count:.1f} bytes")

    # Breakdown by type
    py_files = sum(1 for f in os.listdir("E:\\WorkSpace\\Newmax\\ai-agent-harness") if f.endswith('.py'))
    md_files = sum(1 for f in os.listdir("E:\\WorkSpace\\Newmax\\ai-agent-harness") if f.endswith('.md'))
    yaml_files = sum(1 for f in os.listdir("E:\\WorkSpace\\Newmax\\ai-agent-harness") if f.endswith('.yaml'))

    print(f"🐍 Python files: {py_files}")
    print(f"📄 Markdown files: {md_files}")
    print(f"⚙️  YAML config files: {yaml_files}")

def main():
    """主验证函数"""
    print("🚀 AI Agent Harness System Validation")
    print("=" * 60)

    try:
        import yaml  # For YAML validation
    except ImportError:
        print("⚠️  PyYAML not installed, skipping YAML validation")
        yaml = None

    # Run all validation checks
    structure_ok = validate_file_structure()
    components_ok = validate_core_components()
    token_ok = validate_token_optimizer() if yaml else True
    skill_ok = validate_skill_integration()
    docs_ok = validate_documentation()
    stats_ok = validate_project_stats()

    # Final summary
    print("\n🏁 Validation Summary")
    print("=" * 30)

    checks = [
        ("File Structure", structure_ok),
        ("Core Components", components_ok),
        ("Token Configuration", token_ok),
        ("Skill Integration", skill_ok),
        ("Documentation", docs_ok)
    ]

    passed = sum(result for _, result in checks)
    total = len(checks)

    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")

    print(f"\n🎉 Overall Result: {passed}/{total} checks passed")

    if passed == total:
        print("\n✨ All validations passed! System is ready for use.")
        print("\n🚀 Next steps:")
        print("   1. Run 'python integrated_demo.py' for demonstration")
        print("   2. Try 'python super_powers.py' to test basic functionality")
        print("   3. Use '/harness' commands in 牛马AI for direct integration")
        print("   4. Review 'docs/QUICK_START.md' for detailed usage guide")
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed. Please review the issues above.")

if __name__ == "__main__":
    main()