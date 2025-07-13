# Tests

This directory contains all tests for the Hacker News Analytics Dashboard.

## 📁 Test Structure

```
tests/
├── unit/           # Unit tests (pytest)
│   └── test_backend_pytest.py
├── integration/    # Integration tests
│   └── test_backend.py
├── e2e/           # End-to-end tests
│   └── test_e2e.py
├── conftest.py    # Pytest configuration and fixtures
└── README.md      # This file
```

## 🧪 Test Types

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual functions and classes in isolation
- **Framework**: pytest
- **Scope**: Single functions, methods, or classes
- **Speed**: Fast
- **Dependencies**: Minimal (mocked external dependencies)

### Integration Tests (`tests/integration/`)
- **Purpose**: Test how components work together
- **Framework**: Custom test scripts
- **Scope**: Multiple components, API endpoints
- **Speed**: Medium
- **Dependencies**: Database, external services

### End-to-End Tests (`tests/e2e/`)
- **Purpose**: Test the entire application from user perspective
- **Framework**: Custom test scripts
- **Scope**: Full application stack
- **Speed**: Slow
- **Dependencies**: All services running (backend, frontend, database)

## 🚀 Running Tests

### Quick Start
```bash
# Run all tests
python3 run_tests.py all

# Run specific test types
python3 run_tests.py unit
python3 run_tests.py integration
python3 run_tests.py e2e

# Run with coverage
python3 run_tests.py coverage
```

### Using pytest directly
```bash
# Run all pytest tests
pytest tests/ -v

# Run specific test types
pytest tests/unit/ -v
pytest tests/integration/ -v

# Run with markers
pytest -m unit -v
pytest -m integration -v
pytest -m e2e -v
```

### Manual test execution
```bash
# Backend integration tests
python3 tests/integration/test_backend.py

# End-to-end tests
python3 tests/e2e/test_e2e.py
```

## 📋 Test Requirements

### For Unit Tests
- pytest
- httpx (for async testing)
- No external services required

### For Integration Tests
- Backend API running on localhost:8000
- Database connection
- Redis connection

### For E2E Tests
- Backend API running on localhost:8000
- Frontend running on localhost:3000
- Database with test data
- All services healthy

## 🔧 Test Configuration

### pytest.ini
- Test discovery patterns
- Markers for different test types
- Output formatting options

### conftest.py
- Common fixtures
- Test client setup
- Sample data fixtures

## 📊 Test Coverage

To generate coverage reports:
```bash
# Install coverage tools
pip install pytest-cov

# Run with coverage
python run_tests.py coverage

# Coverage report will be generated in htmlcov/
```

## 🐛 Debugging Tests

### Common Issues
1. **Import errors**: Ensure you're running from project root
2. **Database connection**: Check DATABASE_URL in .env
3. **Service not running**: Start required services before running tests
4. **Port conflicts**: Ensure ports 8000 and 3000 are available

### Debug Mode
```bash
# Run with debug output
pytest tests/ -v -s

# Run specific test with debug
pytest tests/unit/test_backend_pytest.py::test_hn_service -v -s
```

## 📝 Adding New Tests

### Unit Tests
1. Create test file in `tests/unit/`
2. Use pytest framework
3. Mock external dependencies
4. Test single function/class

### Integration Tests
1. Create test file in `tests/integration/`
2. Test component interactions
3. Use real database (test database)
4. Test API endpoints

### E2E Tests
1. Create test file in `tests/e2e/`
2. Test full user workflows
3. Require all services running
4. Test real user scenarios

## 🎯 Best Practices

1. **Test Naming**: Use descriptive test names
2. **Test Isolation**: Each test should be independent
3. **Cleanup**: Clean up test data after tests
4. **Mocking**: Mock external services in unit tests
5. **Fixtures**: Use pytest fixtures for common setup
6. **Assertions**: Use specific assertions with clear messages
7. **Documentation**: Document complex test scenarios

## 🔄 CI/CD Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Unit Tests
  run: python run_tests.py unit

- name: Run Integration Tests
  run: python run_tests.py integration

- name: Run E2E Tests
  run: python run_tests.py e2e
```

## 📈 Test Metrics

- **Unit Tests**: ~100ms per test
- **Integration Tests**: ~1-5s per test
- **E2E Tests**: ~10-30s per test
- **Coverage Target**: >80% for backend code 