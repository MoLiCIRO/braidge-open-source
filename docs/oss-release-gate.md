# OSS Release Gate

Use this checklist before copying, rewriting, publishing, or releasing anything
from private Braidge repositories into this public-facing repository.

## 1. Choose Only Public-Safe Scope

Allowed:

- Inch fraction parsing, formatting, and arithmetic.
- Generic 2D geometry helpers.
- Generic DXF convenience helpers.
- Generic cutout validation concepts.
- Synthetic examples and tests.

Not allowed:

- Proprietary production orchestration or commercial workflow automation.
- Private production rules, machine integrations, or deployment details.
- Customer cases, drawings, prompts, logs, or internal validation data.
- Tenant, billing, quota, auth, or customer operations logic.

## 2. Prefer Rewrite Over Copy

When a private module is close to the commercial production path, rewrite the
public version from the general concept instead of copying implementation
details. Public modules should stand alone and should not import private code.

## 3. Sanitize

Check for:

- API keys, tokens, webhook URLs, internal domains, and account IDs.
- Customer names, project names, drawing names, and production identifiers.
- Paths from local machines, deployment systems, or private services.
- References to private prompts, agents, workflows, or runbooks.

## 4. Test Independently

Run:

```bash
python -m pip install -e ".[dev]"
pytest
```

The repository must clone, install, test, and run examples without access to any
private Braidge repository.

## 5. Human Approval

Before making the repository public:

- Review the diff against the previous public release.
- Run a secret scan.
- Confirm that examples use synthetic data.
- Confirm that no private repository paths or imports are present.
- Confirm that the repository description matches the public positioning.
