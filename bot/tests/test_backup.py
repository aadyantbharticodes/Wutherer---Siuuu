import json
import unittest
from bot.database.models.backup import GuildBackupSnapshot


class TestBackupSnapshot(unittest.TestCase):
    def setUp(self):
        self.snapshot = GuildBackupSnapshot(
            backup_id="snp_test123",
            guild_id=987654321,
            guild_name="Wutherer Test Guild",
            created_by=11223344,
            roles_data=[
                {"id": 1, "name": "Admin", "color": 0xFF0000, "position": 10},
                {"id": 2, "name": "Member", "color": 0x00FF00, "position": 1},
            ],
            categories_data=[{"id": 10, "name": "Text Channels", "position": 0}],
            channels_data=[
                {"id": 101, "name": "general", "type": "text", "category_id": 10},
                {"id": 102, "name": "voice", "type": "voice", "category_id": 10},
            ],
            notes="Automated test snapshot",
        )

    def test_serialization_and_deserialization(self):
        json_str = self.snapshot.to_json()
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["backup_id"], "snp_test123")
        self.assertEqual(len(parsed["roles_data"]), 2)
        self.assertEqual(len(parsed["channels_data"]), 2)

        restored = GuildBackupSnapshot.from_json(json_str)
        self.assertEqual(restored.backup_id, self.snapshot.backup_id)
        self.assertEqual(restored.guild_name, self.snapshot.guild_name)
        self.assertEqual(len(restored.roles_data), 2)
        self.assertEqual(restored.notes, "Automated test snapshot")


if __name__ == "__main__":
    unittest.main()

