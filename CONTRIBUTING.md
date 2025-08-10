# Contributing to Portfolio Optimization Project

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of financial concepts
- Familiarity with pandas, numpy, and scikit-learn

### Development Setup

1. **Fork and clone the repository**
   \`\`\`bash
   git clone https://github.com/yourusername/portfolio-optimization.git
   cd portfolio-optimization
   \`\`\`

2. **Create a virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install development dependencies**
   \`\`\`bash
   make install
   # or
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   \`\`\`

4. **Set up pre-commit hooks**
   \`\`\`bash
   pre-commit install
   \`\`\`

5. **Verify setup**
   \`\`\`bash
   make test
   \`\`\`

## Contributing Process

### 1. Choose an Issue

- Look for issues labeled `good first issue` for beginners
- Check existing issues before creating new ones
- Comment on issues you'd like to work on

### 2. Create a Branch

\`\`\`bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
\`\`\`

### 3. Make Changes

- Follow the coding standards (see below)
- Write tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Commit Changes

\`\`\`bash
git add .
git commit -m "feat: add new forecasting model"
\`\`\`

**Commit Message Format:**
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` adding tests
- `refactor:` code refactoring
- `style:` formatting changes

### 5. Push and Create Pull Request

\`\`\`bash
git push origin feature/your-feature-name
\`\`\`

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots if applicable

## Coding Standards

### Python Style

- Follow PEP 8
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

```python
def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily returns from price data.
    
    Args:
        prices: DataFrame with price data
        
    Returns:
        DataFrame with daily returns
    """
    return prices.pct_change().dropna()
