# AI Agent Harness - Development Guidelines

## 🎯 Overview

This document provides comprehensive development guidelines for the AI Agent Harness project, including coding standards, architecture principles, testing requirements, and deployment procedures.

## 🏗️ Architecture Principles

### Core Philosophy
1. **Layered Constraints**: Each layer adds specific constraints that build upon previous layers
2. **Progressive Disclosure**: Start simple, add complexity as needed
3. **Token Efficiency First**: All optimizations prioritize token reduction
4. **Backward Compatibility**: Never break existing functionality

### Design Patterns
```python
# Layered Architecture Pattern
class BaseLayer:
    """Base class for all harness layers"""
    def __init__(self):
        self.config = {}
        self.metrics = MetricsCollector()

class SuperPowersLayer(BaseLayer):
    """Programming discipline enforcement"""
    def enforce_workflow(self):
        # Implementation must follow 7 stages
        pass

class GSDLayer(BaseLayer): 
    """Context isolation for long tasks"""
    def execute_with_isolation(self):
        # Must use fresh context per phase
        pass

class TokenOptimizationMixin:
    """Shared optimization capabilities"""
    def optimize_request(self, request):
        # Apply caching, compression, reuse
        pass
```

## 📝 Coding Standards

### Python Style Guide
```python
# File: core/super_powers.py
"""Super Powers - AI programming discipline engine."""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime


class SuperPowersEngine:
    """
    Enforces 7-stage programming workflow with hard gates.
    
    This class implements Gyro's Super Powers methodology to ensure
    AI agents follow proper software engineering practices.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Super Powers engine with configuration."""
        self.config = config or self._default_config()
        self.active_sessions: Dict[str, SessionState] = {}
        
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "max_stages": 7,
            "hard_gate_enforcement": True,
            "tdd_required": True,
            "git_isolation": True
        }
    
    async def create_session(self, task_description: str) -> SessionState:
        """
        Create new development session with enforced workflow.
        
        Args:
            task_description: Clear description of what needs to be built
            
        Returns:
            SessionState object representing the active session
            
        Raises:
            ValueError: If task description is insufficiently detailed
        """
        if len(task_description) < 50:
            raise ValueError("Task description must be at least 50 characters")
            
        session_id = f"session_{int(datetime.now().timestamp())}"
        session = SessionState(
            session_id=session_id,
            task=task_description,
            current_stage=Stage.BRAINSTORMING
        )
        
        self.active_sessions[session_id] = session
        return session
```

### Documentation Requirements
- **Docstrings**: Required for all public methods using Google style
- **Type Hints**: Required for all function parameters and return values
- **Comments**: Only when logic is non-obvious
- **Examples**: Include in docstrings when helpful

### Error Handling
```python
# Use custom exceptions for domain-specific errors
class HarnessError(Exception):
    """Base exception for harness-related errors."""
    pass

class HardGateViolation(HarnessError):
    """Raised when a hard gate is violated."""
    pass

class TokenBudgetExceeded(HarnessError):
    """Raised when token budget is exceeded."""
    pass

def enforce_hard_gate(condition: bool, message: str) -> None:
    """Enforce hard gates in workflows."""
    if not condition:
        raise HardGateViolation(f"Hard gate violation: {message}")
```

## 🧪 Testing Strategy

### Test Organization
```
tests/
├── unit/
│   ├── test_super_powers.py
│   ├── test_gsd_engine.py
│   ├── test_token_optimizer.py
│   └── test_knowledge_reuse.py
├── integration/
│   ├── test_layer_integration.py
│   └── test_end_to_end.py
├── performance/
│   ├── test_token_efficiency.py
│   └── test_response_time.py
└── fixtures/
    ├── sample_requests.py
    └── mock_responses.py
```

### Unit Testing Example
```python
# tests/unit/test_token_optimizer.py
import pytest
from unittest.mock import Mock
from core.token_optimizer import TokenOptimizer


class TestTokenOptimizer:
    """Test suite for TokenOptimizer class."""
    
    @pytest.fixture
    def optimizer(self):
        """Create test instance."""
        return TokenOptimizer(config={"max_cache_size": 10})
    
    def test_cache_hit_rate(self, optimizer):
        """Test cache hit rate calculation."""
        # Arrange
        request_data = {"prompt": "test", "context": []}
        
        # Act - First call (cache miss)
        result1 = await optimizer.optimize_request(request_data)
        
        # Second call (cache hit)
        result2 = await optimizer.optimize_request(request_data)
        
        # Assert
        assert result1 == result2
        assert optimizer.cache.get_cache_stats()["hit_rate"] > 0
    
    @pytest.mark.asyncio
    async def test_context_compression(self, optimizer):
        """Test context compression reduces size."""
        # Arrange
        large_context = [{"data": "x" * 1000} for _ in range(10)]
        request_data = {
            "prompt": "process this",
            "context": large_context
        }
        
        # Act
        original_size = len(json.dumps(request_data))
        optimized = await optimizer.optimize_request(request_data)
        compressed_size = len(json.dumps(optimized))
        
        # Assert
        assert compressed_size < original_size
        assert optimized["optimization_applied"] is True
```

### Integration Testing
```python
# tests/integration/test_layer_integration.py
import pytest
from core.super_powers import SuperPowersEngine
from core.gsd_engine import GSDWorkflow
from token_optimizer import global_optimizer


class TestLayerIntegration:
    """Test integration between harness layers."""
    
    @pytest.fixture
    def super_powers(self):
        return SuperPowersEngine()
    
    @pytest.fixture  
    def gsd_workflow(self):
        return GSDWorkflow()
    
    @pytest.mark.asyncio
    async def test_super_powers_to_gsd_flow(self, super_powers, gsd_workflow):
        """Test workflow from Super Powers to GSD integration."""
        # Create Super Powers session
        session = await super_powers.create_session("Refactor user system")
        
        # Validate TDD requirement
        await super_powers.enforce_tdd_phase(session.session_id)
        
        # Convert to GSD long task
        gsd_project = await gsd_workflow.new_project(
            name="User System Refactor",
            phases=6
        )
        
        # Verify token optimization applied
        assert gsd_project["token_optimized"] is True
```

## 🔧 Development Workflow

### Branch Naming Convention
```
feature/<layer>-<functionality>    # e.g., feature/super-powers-brainstorm
bugfix/<component>-<issue>         # e.g., bugfix/gsd-context-leak
hotfix/<critical-issue>             # e.g., hotfix/token-budget-overrun
release/<version>                   # e.g., release/v1.1.0
```

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type Options
- `feat`: New functionality
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Build/CI changes

#### Example
```
feat(token-optimizer): implement knowledge reuse engine

Adds semantic similarity detection and concept mapping
to reduce token consumption through knowledge reuse.

Resolves: #123
Related: #124, #125
```

### Pull Request Process
1. **Create PR** with descriptive title and detailed description
2. **Assign Reviewers** from appropriate layer experts
3. **Run Tests** - Ensure all CI checks pass
4. **Address Feedback** - Respond to review comments promptly
5. **Squash Commits** - Keep history clean before merge
6. **Update Documentation** - Reflect any API changes

## 📊 Code Quality

### Static Analysis
```bash
# Run all static checks
flake8 core/ token_optimizer/ skills/
mypy core/ token_optimizer/ --ignore-missing-imports

# Check imports are properly sorted
isort --check-only core/ token_optimizer/

# Format code according to standards
black core/ token_optimizer/
```

### Performance Profiling
```python
# Use cProfile for performance analysis
import cProfile
import pstats

def profile_token_optimization():
    """Profile token optimization performance."""
    profiler = cProfile.Profile()
    
    # Your optimization code here
    optimizer = TokenOptimizer()
    request = generate_test_request()
    
    profiler.runcall(optimizer.optimize_request, request)
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
```

### Memory Profiling
```python
# Use memory_profiler for memory analysis
@profile
def analyze_memory_usage():
    """Analyze memory usage patterns."""
    optimizer = TokenOptimizer()
    # Your code here
    pass
```

## 🚀 Deployment & CI/CD

### Continuous Integration
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/ --cov=core --cov=token_optimizer
    - name: Run linter
      run: |
        flake8 core/ token_optimizer/
        mypy core/ token_optimizer/
```

### Deployment Strategy
```
Development -> Staging -> Production
     ↓           ↓          ↓
  Manual    Automated   Zero-downtime
  Testing   Validation  Blue-green
```

### Environment Configuration
```yaml
# config/production.yaml
token_optimizer:
  max_cache_size: 5000
  cache_ttl_hours: 48
  enable_knowledge_reuse: true
  budget_limit_per_call: 15000

monitoring:
  enable_metrics_collection: true
  alert_thresholds:
    budget_utilization_max: 0.9
```

## 📈 Monitoring & Observability

### Key Metrics to Track
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Cache Hit Rate | >80% | <70% |
| Average Response Time | <500ms | >1000ms |
| Token Budget Utilization | <90% | >95% |
| Error Rate | <1% | >5% |

### Logging Standards
```python
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TokenOptimizer:
    """Token optimizer with structured logging."""
    
    def optimize_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize request with detailed logging."""
        start_time = time.time()
        logger.info("Starting token optimization", extra={
            "request_size": len(str(request)),
            "request_type": request.get("type", "unknown")
        })
        
        try:
            result = await self._perform_optimization(request)
            duration = time.time() - start_time
            
            logger.info("Optimization completed", extra={
                "duration_ms": duration * 1000,
                "tokens_saved": result.get("tokens_saved", 0),
                "success": True
            })
            
            return result
            
        except Exception as e:
            logger.error("Optimization failed", extra={
                "error": str(e),
                "request": str(request)[:200]  # Truncate for log safety
            })
            raise
```

## 🛡️ Security Guidelines

### Code Security
- **Input Validation**: Validate all external inputs
- **Output Sanitization**: Sanitize all outputs to prevent injection attacks
- **Dependency Management**: Regularly update dependencies
- **Secret Management**: Use environment variables, never hardcode secrets

### Data Security
```python
# Secure cache key generation
def generate_secure_cache_key(data: Dict[str, Any]) -> str:
    """Generate secure hash-based cache key."""
    content = json.dumps(data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()

# Sensitive data filtering
def filter_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove sensitive information from data."""
    filtered = data.copy()
    
    sensitive_fields = ["password", "token", "key", "secret"]
    for field in sensitive_fields:
        if field in filtered:
            filtered[field] = "***REDACTED***"
            
    return filtered
```

## 📚 Documentation Standards

### Module Documentation
```python
"""
Module: core/super_powers.py

Implements Super Powers methodology for AI agent programming discipline.
Based on Gyro's four-layer engineering constraints framework.

Key Features:
- 7-stage enforced workflow
- Hard gate enforcement
- TDD validation
- Git worktree isolation

Usage:
    engine = SuperPowersEngine()
    session = await engine.create_session("Implement user login")
"""

class SuperPowersEngine:
    """See module docstring for overview."""
    pass
```

### README Requirements
Every new component must have:
- Purpose and scope
- Usage examples
- Configuration options
- Performance characteristics
- Dependencies
- Troubleshooting guide

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create feature branch (`git checkout -b feature/my-feature`)
3. Commit changes (`git commit -am 'Add amazing feature'`)
4. Push to branch (`git push origin feature/my-feature`)
5. Create Pull Request

### Contribution Checklist
- [ ] Code follows project style guidelines
- [ ] Unit tests added for new functionality
- [ ] Integration tests pass
- [ ] Documentation updated
- [ ] Performance impact assessed
- [ ] Security review completed
- [ ] Changelog entry added

---

*These guidelines evolve with the project. Please contribute improvements via GitHub Issues or Pull Requests.*