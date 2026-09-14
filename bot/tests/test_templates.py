from __future__ import annotations
import unittest
from services.templates import PUBLIC_TEMPLATES, TemplateEngine


class TestTemplates(unittest.TestCase):
    def test_public_templates_exist(self):
        self.assertIn("gaming_community", PUBLIC_TEMPLATES)
        self.assertIn("tech_developer", PUBLIC_TEMPLATES)
        self.assertIn("community_lounge", PUBLIC_TEMPLATES)
        self.assertIn("study_university", PUBLIC_TEMPLATES)
        self.assertIn("esports_clan", PUBLIC_TEMPLATES)

    def test_public_template_structure(self):
        for key, tmpl in PUBLIC_TEMPLATES.items():
            self.assertIn("name", tmpl)
            self.assertIn("description", tmpl)
            self.assertIn("category", tmpl)
            self.assertIn("roles", tmpl)
            self.assertIn("categories", tmpl)
            self.assertTrue(len(tmpl["roles"]) > 0)
            self.assertTrue(len(tmpl["categories"]) > 0)

            for cat in tmpl["categories"]:
                self.assertIn("name", cat)
                self.assertIn("channels", cat)
                for ch in cat["channels"]:
                    self.assertIn("name", ch)
                    self.assertIn("type", ch)
                    self.assertIn(ch["type"], ("text", "voice", "stage", "forum"))

    def test_roles_attributes(self):
        tmpl = PUBLIC_TEMPLATES["gaming_community"]
        for role in tmpl["roles"]:
            self.assertIn("name", role)
            self.assertIn("color", role)
            self.assertIn("permissions", role)
            self.assertIsInstance(role["hoist"], bool)
            self.assertIsInstance(role["mentionable"], bool)


if __name__ == "__main__":
    unittest.main()
