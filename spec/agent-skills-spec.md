# Agent Skills Specification

This document defines the Agent Skills format.

## Directory structure

A skill is a directory containing at minimum a SKILL.md file:
skill-name/
└── SKILL.md # Required

## SKILL.md format

The SKILL.md file must contain YAML frontmatter followed by Markdown content.

### Frontmatter (required)

---
name: skill-name
description: A description of what this skill does and when to use it.
---

With optional fields:
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
 author: example-org
 version: "1.0"
---

| Field | Required | Constraints |
|-------|----------|-------------|
| name | Yes | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. |
| description | Yes | Max 1024 characters. Non-empty. Describes what the skill does and when to use it. |
| license | No | License name or reference to a bundled license file. |
| compatibility | No | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| metadata | No | Arbitrary key-value mapping for additional metadata. |
| allowed-tools | No | Space-delimited list of pre-approved tools the skill may use. (Experimental) |

#### name field

The required name field:
- Must be 1-64 characters
- May only contain unicode lowercase alphanumeric characters and hyphens (a-z and -)
- Must not start or end with -
- Must not contain consecutive hyphens (--)
- Must match the parent directory name

#### description field

The required description field:
- Must be 1-1024 characters
- Should describe both what the skill does and when to use it
- Should include specific keywords that help agents identify relevant tasks

#### license field (optional)
- Specifies the license applied to the skill.

#### compatibility field (optional)
- Can indicate intended product, required system packages, network access needs, etc.

#### metadata field (optional)
- A map from string keys to string values for additional properties.

#### allowed-tools field (optional)
- A space-delimited list of tools that are pre-approved to run.

### Body content

The Markdown body after the frontmatter contains the skill instructions. There are no format restrictions. Recommended sections:
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases

## Optional directories

### scripts/
Contains executable code that agents can run (Python, Bash, JavaScript, etc.).

### references/
Contains additional documentation (REFERENCE.md, FORMS.md, etc.) that agents load on demand.

### assets/
Contains static resources (templates, images, data files).

## Progressive disclosure

Skills should be structured for efficient use of context:
- Metadata (~100 tokens): Loaded at startup for all skills.
- Instructions: Keep your main SKILL.md under 500 lines. Move detailed material to separate files.

## File references

Use relative paths from the skill root (e.g., `scripts/extract.py`). Keep references one level deep.

## Validation

Use the skills-ref reference library to validate your skills:
`skills-ref validate ./my-skill`
