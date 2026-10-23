"""
test_chart_guarantees.py — verifies all 5 chart guarantees defined in
ARCHITECTURE.md against the fixture.

The chart module must produce output that passes every check here.
"""
import json
import pathlib
from collections import defaultdict


FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "chart" / "guitar.json"


def _load() -> dict:
    with open(FIXTURE) as f:
        return json.load(f)


def test_guarantee_1_sorted_by_start():
    """Notes are sorted by start_s (non-decreasing)."""
    chart = _load()
    starts = [n["start_s"] for n in chart["notes"]]
    assert starts == sorted(starts)


def test_guarantee_2_end_after_start():
    """Every note has end_s strictly after start_s."""
    chart = _load()
    for note in chart["notes"]:
        assert note["end_s"] > note["start_s"], (
            f"Note {note['id']}: end_s={note['end_s']} <= start_s={note['start_s']}"
        )


def test_guarantee_3_string_fret_midi():
    """tuning[string] + capo + fret == midi for every note."""
    chart = _load()
    tuning = chart["tuning"]
    capo = chart["capo"]
    for note in chart["notes"]:
        expected = tuning[note["string"]] + capo + note["fret"]
        assert expected == note["midi"], (
            f"Note {note['id']}: tuning[{note['string']}]={tuning[note['string']]} "
            f"+ capo={capo} + fret={note['fret']} = {expected} != midi={note['midi']}"
        )


def test_guarantee_4_no_string_overlap():
    """No two notes overlap in time on the same string."""
    chart = _load()
    by_string: dict[int, list] = defaultdict(list)
    for note in chart["notes"]:
        by_string[note["string"]].append(note)
    for string_id, notes in by_string.items():
        notes_sorted = sorted(notes, key=lambda n: n["start_s"])
        for i in range(len(notes_sorted) - 1):
            a, b = notes_sorted[i], notes_sorted[i + 1]
            assert a["end_s"] <= b["start_s"], (
                f"String {string_id}: note {a['id']} ({a['start_s']}-{a['end_s']}) "
                f"overlaps note {b['id']} ({b['start_s']}-{b['end_s']})"
            )


def test_guarantee_5_playable_fret():
    """Every note has fret in [0, 24] — within the instrument's playable range."""
    chart = _load()
    for note in chart["notes"]:
        assert note["fret"] >= 0, f"Note {note['id']} has negative fret {note['fret']}"
        assert note["fret"] <= 24, f"Note {note['id']} has fret {note['fret']} > 24"
