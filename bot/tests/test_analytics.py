import unittest
from bot.database.models.analytics import HourlyActivityRecord, ChannelActivityRecord


class TestAnalyticsModels(unittest.TestCase):
    def test_hourly_record_creation(self):
        rec = HourlyActivityRecord(
            guild_id=112233,
            timestamp_hour=1710000000,
            message_count=150,
            active_users=45,
            voice_minutes=320,
            commands_run=28,
        )
        self.assertEqual(rec.guild_id, 112233)
        self.assertEqual(rec.message_count, 150)
        self.assertEqual(rec.voice_minutes, 320)

    def test_channel_record_creation(self):
        ch = ChannelActivityRecord(
            guild_id=112233,
            channel_id=998877,
            message_count=520,
            last_active=1710001000,
        )
        self.assertEqual(ch.channel_id, 998877)
        self.assertEqual(ch.message_count, 520)


if __name__ == "__main__":
    unittest.main()

