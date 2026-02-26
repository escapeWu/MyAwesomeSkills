# Skill Directory Structure Reference

Standard directory layout and conventions for building Claude skills.

## Standard Structure

```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + Markdown instructions
├── scripts/              # Optional: Executable code (Python/Bash)
│   └── my_script.py
├── references/           # Optional: Docs loaded into context on demand via Read
│   └── api_docs.md
├── assets/               # Optional: Templates/images, referenced by path only
│   └── template.html
└── examples.md           # Optional: Input/output examples
```

## SKILL.md Frontmatter

Only `name` and `description` are required. Do not add other fields.

```yaml
---
name: my-skill
description: >
  What the skill does and when to trigger it.
  Include all trigger conditions here — the body is only loaded after triggering.
---
```

### Description Guidelines

- Describe both what the skill does AND when to use it
- All "when to use" info must be in the description, not the body
- Be specific about trigger contexts:

```yaml
# Good
description: >
  Write scored news records to the sentiment database in batch.
  Use after rating articles to persist them.

# Bad — too vague
description: Write data to database.
```

## Bundled Resources

### scripts/

Executable code called via Bash. Use `{baseDir}` for portable paths.

```markdown
## Usage
\`\`\`bash
.venv/bin/python {baseDir}/scripts/crawl_news.py --relation "BTC"
\`\`\`
```

- Include when the same code would be rewritten repeatedly
- Test scripts before packaging
- Scripts can be executed without loading into context (token efficient)

### references/

Documentation loaded into context on demand via Read tool.

```markdown
For API details, see `Read({baseDir}/references/api_docs.md)`.
```

- Keep SKILL.md lean — move detailed schemas, API docs, domain knowledge here
- For files >100 lines, include a table of contents at the top
- For files >10k words, include grep search patterns in SKILL.md
- Avoid duplication between SKILL.md and references

### assets/

Files used in output, never loaded into context.

```markdown
Copy the template from `{baseDir}/assets/template.html`.
```

- Templates, images, icons, fonts, boilerplate code
- Referenced by path only

## Path Convention: {baseDir}

Always use `{baseDir}` to reference files within the skill directory:

```markdown
# Good — portable
.venv/bin/python {baseDir}/scripts/process.py
Read({baseDir}/references/schema.md)

# Bad — hardcoded
.venv/bin/python /Users/me/project/.claude/skills/my-skill/scripts/process.py
```

## Progressive Disclosure

Three-level loading to manage context efficiently:

| Level | What | When loaded | Size target |
|-------|------|-------------|-------------|
| 1. Metadata | name + description | Always in context | ~100 words |
| 2. SKILL.md body | Instructions | When skill triggers | <5k words, <500 lines |
| 3. Resources | scripts/references/assets | As needed by Claude | Unlimited |

## What NOT to Include

Do not create these files — they add clutter:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- Any user-facing documentation

The skill is for an AI agent, not a human reader.

## Organizing Multi-Domain Skills

For skills with multiple variants, keep selection logic in SKILL.md and split details into references:

```
cloud-deploy/
├── SKILL.md                    # Workflow + provider selection guide
└── references/
    ├── aws.md                  # AWS-specific patterns
    ├── gcp.md                  # GCP-specific patterns
    └── azure.md                # Azure-specific patterns
```

Claude only loads the relevant reference file based on context.

## Checklist

Before packaging, verify:

- [ ] SKILL.md has `name` and `description` in frontmatter
- [ ] Description includes all trigger conditions
- [ ] Body uses imperative/infinitive form
- [ ] All file references use `{baseDir}`
- [ ] Scripts are tested and executable
- [ ] No duplicate info between SKILL.md and references
- [ ] No unnecessary docs (README, CHANGELOG, etc.)
- [ ] SKILL.md body < 500 lines
