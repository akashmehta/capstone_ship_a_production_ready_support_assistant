```markdown
---
description: Run the Capstone Evaluation suite, analyze test pass rates, and output a diagnostic summary.
argument-hint: "[optional-pytest-filter-or-test-name]"
allowed-tools:
- Bash
---

# Capstone Evaluation Suite Execution

Run the evaluation suite for the Claude Support Assistant and generate an executive test report.

## Step 1: Execute Test Suite
Execute pytest against the evaluation dataset:

```!
pytest tests/evals/ -v -k "$ARGUMENTS" --tb=short