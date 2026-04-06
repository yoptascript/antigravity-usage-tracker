from __future__ import annotations

from contextlib import redirect_stdout
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import types
import unittest


AG_PATH = Path(__file__).resolve().parents[1] / "ag"


def load_ag_module() -> types.ModuleType:
    loader = SourceFileLoader("ag_script_repo", str(AG_PATH))
    spec = spec_from_loader(loader.name, loader)
    assert spec is not None
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class AgTests(unittest.TestCase):
    def test_parse_burn_event_uses_logged_reset_duration(self) -> None:
        ag = load_ag_module()
        line = (
            "2026-04-06 13:02:39.210 [info] agent executor error: RESOURCE_EXHAUSTED "
            "(code 429): You have exhausted your capacity on this model. "
            "Your quota will reset after 101h27m16s."
        )

        event = ag.parse_burn_event(line, Path("/tmp/Antigravity.log"))

        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.occurred_at.isoformat(), "2026-04-06T13:02:39.210000+03:00")
        self.assertEqual(event.reset_at.isoformat(), "2026-04-10T18:29:55.210000+03:00")

    def test_detect_last_burn_scans_nested_logs(self) -> None:
        ag = load_ag_module()

        with TemporaryDirectory() as tmp_dir:
            nested_log = Path(tmp_dir) / "20260405T181216" / "window1" / "exthost" / "google.antigravity"
            nested_log.mkdir(parents=True)
            log_path = nested_log / "Antigravity.log"
            log_path.write_text(
                "\n".join(
                    [
                        "2026-04-06 12:40:51.203 [info] Trace: 0xab3c0aceeb26bfc3",
                        (
                            "2026-04-06 13:02:39.210 [info] agent executor error: "
                            "RESOURCE_EXHAUSTED (code 429): You have exhausted your capacity "
                            "on this model. Your quota will reset after 101h27m16s."
                        ),
                    ]
                )
            )

            ag.LOG_DIR = Path(tmp_dir)
            event = ag.detect_last_burn()

        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.source.name, "Antigravity.log")
        self.assertEqual(event.occurred_at.isoformat(), "2026-04-06T13:02:39.210000+03:00")

    def test_help_command_lists_all_commands(self) -> None:
        ag = load_ag_module()
        output = StringIO()
        old_argv = sys.argv

        try:
            sys.argv = [str(AG_PATH), "help"]
            with redirect_stdout(output):
                exit_code = ag.main()
        finally:
            sys.argv = old_argv

        self.assertEqual(exit_code, 0)
        self.assertIn("Usage: ag [command]", output.getvalue())
        self.assertIn("next", output.getvalue())
        self.assertIn("watch", output.getvalue())
        self.assertIn("help", output.getvalue())


if __name__ == "__main__":
    unittest.main()
