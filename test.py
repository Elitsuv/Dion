import unittest
import os
from utils.db import SQLiteDatabase

class TestDionDatabase(unittest.TestCase):
    def setUp(self):
        self.db_path = "data/test_dion.db"
        self.db = SQLiteDatabase(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_warnings(self):
        warnings = self.db.get_warnings("12345")
        self.assertEqual(len(warnings), 0)

        self.db.add_warning("12345", "9999", "Testing warn rules", "2026-06-29 20:00:00")
        warnings = self.db.get_warnings("12345")
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]["reason"], "Testing warn rules")
        self.assertEqual(warnings[0]["moderator_id"], "9999")

    def test_temp_voice_config(self):
        config = self.db.get_temp_voice_config("111")
        self.assertIsNone(config)

        self.db.set_temp_voice_config("111", 222, 333)
        config = self.db.get_temp_voice_config("111")
        self.assertIsNotNone(config)
        self.assertEqual(config["setup_channel_id"], 222)
        self.assertEqual(config["category_id"], 333)

    def test_active_temp_channels(self):
        channel = self.db.get_active_temp_channel("444")
        self.assertIsNone(channel)

        self.db.set_active_temp_channel("444", "555")
        channel = self.db.get_active_temp_channel("444")
        self.assertIsNotNone(channel)
        self.assertEqual(channel["owner_id"], "555")

        self.db.remove_active_temp_channel("444")
        channel = self.db.get_active_temp_channel("444")
        self.assertIsNone(channel)

    def test_stats(self):
        self.db.record_command_usage("123", "20:00:00")
        self.db.record_command_usage("123", "20:01:00")
        self.db.record_command_usage("456", "20:02:00")

        stats = self.db.get_command_usage_stats()
        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0]["user_id"], "123")
        self.assertEqual(stats[0]["command_count"], 2)
        self.assertEqual(stats[1]["user_id"], "456")
        self.assertEqual(stats[1]["command_count"], 1)

    def test_events(self):
        self.db.add_event(1001, 2002, 3003, "Game Night", "LFG Rocket League", 1782316910, 4004, 5005)
        
        event = self.db.get_event(1001)
        self.assertIsNotNone(event)
        self.assertEqual(event["title"], "Game Night")
        self.assertEqual(event["channel_id"], 5005)

        events = self.db.get_guild_events(2002)
        self.assertEqual(len(events), 1)

        self.db.set_rsvp(1001, 3003, "attending")
        rsvps = self.db.get_rsvps(1001)
        self.assertEqual(len(rsvps), 1)
        self.assertEqual(rsvps[0]["status"], "attending")

        self.db.remove_event(1001)
        event = self.db.get_event(1001)
        self.assertIsNone(event)
        rsvps = self.db.get_rsvps(1001)
        self.assertEqual(len(rsvps), 0)

    def test_alerts(self):
        success = self.db.add_alert_topic(777, "gaming", 888)
        self.assertTrue(success)

        success2 = self.db.add_alert_topic(777, "gaming", 889)
        self.assertFalse(success2)

        topic = self.db.get_alert_topic(777, "gaming")
        self.assertIsNotNone(topic)
        self.assertEqual(topic["role_id"], 888)

        topics = self.db.get_alert_topics(777)
        self.assertEqual(len(topics), 1)

        role_id = self.db.remove_alert_topic(777, "gaming")
        self.assertEqual(role_id, 888)
        
        topic = self.db.get_alert_topic(777, "gaming")
        self.assertIsNone(topic)

    def test_reaction_roles(self):
        self.db.add_reaction_role("111", "222", "👍", "333")
        
        mapping = self.db.get_reaction_role("111", "222", "👍")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping["role_id"], "333")

        binds = self.db.get_all_reaction_roles("111")
        self.assertEqual(len(binds), 1)
        self.assertEqual(binds[0]["message_id"], "222")

        self.db.remove_reaction_role("111", "222", "👍")
        mapping = self.db.get_reaction_role("111", "222", "👍")
        self.assertIsNone(mapping)

if __name__ == '__main__':
    unittest.main()

