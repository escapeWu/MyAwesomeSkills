import tempfile
import unittest
from pathlib import Path

from quick_validate import validate_skill


class QuickValidateFrontmatterTests(unittest.TestCase):
    def validate(self, frontmatter: str) -> tuple[bool, str]:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "explicit-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                f"---\n{frontmatter}\n---\n\n# Explicit Skill\n",
                encoding="utf-8",
            )
            return validate_skill(skill_dir)

    def test_accepts_boolean_disable_model_invocation(self) -> None:
        valid, message = self.validate(
            "name: explicit-skill\n"
            "description: Explicit user-invoked orchestration entry.\n"
            "disable-model-invocation: true"
        )
        self.assertTrue(valid, message)

    def test_rejects_string_disable_model_invocation(self) -> None:
        valid, message = self.validate(
            "name: explicit-skill\n"
            "description: Explicit user-invoked orchestration entry.\n"
            'disable-model-invocation: "true"'
        )
        self.assertFalse(valid)
        self.assertIn("must be a boolean", message)

    def test_accepts_compatibility_from_repository_spec(self) -> None:
        valid, message = self.validate(
            "name: explicit-skill\n"
            "description: Explicit user-invoked orchestration entry.\n"
            "compatibility: Requires a local repository."
        )
        self.assertTrue(valid, message)

    def test_rejects_non_string_compatibility(self) -> None:
        valid, message = self.validate(
            "name: explicit-skill\n"
            "description: Explicit user-invoked orchestration entry.\n"
            "compatibility: 123"
        )
        self.assertFalse(valid)
        self.assertIn("Compatibility must be a string", message)

    def test_rejects_compatibility_over_500_characters(self) -> None:
        valid, message = self.validate(
            "name: explicit-skill\n"
            "description: Explicit user-invoked orchestration entry.\n"
            f"compatibility: {'x' * 501}"
        )
        self.assertFalse(valid)
        self.assertIn("Maximum is 500 characters", message)

    def test_rejects_unknown_frontmatter_key(self) -> None:
        valid, message = self.validate(
            "name: explicit-skill\n"
            "description: Explicit user-invoked orchestration entry.\n"
            "unknown-field: value"
        )
        self.assertFalse(valid)
        self.assertIn("Unexpected key", message)


if __name__ == "__main__":
    unittest.main()
