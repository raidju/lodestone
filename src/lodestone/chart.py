# Stub: fakes P5 (chart building: ghost-note filter, string/fret
# assignment, chord grouping).
# Real replacement: filter notes by amplitude (ghost notes are quieter),
# assign string/fret with a neck-position optimiser to keep the hand in
# one position, and group simultaneous notes into numbered chords.

from __future__ import annotations

from lodestone.store import SongStore

# Standard guitar tuning, string 0 (lowest) to string 5 (highest).
_TUNING = [40, 45, 50, 55, 59, 64]
_CAPO = 0

# Guitar's practical playable range.
_MIDI_MIN = 40   # open low E
_MIDI_MAX = 88   # fret 24 on high e
_FRET_MAX = 24


def build_chart(song_id: str, target: str, store: SongStore) -> None:
    """Build a chart from the raw note list and write chart/<target>.json.

    The stub assigns each note to the lowest string where it fits within
    frets 0-24. Output satisfies all 5 chart guarantees from ARCHITECTURE.md.
    """
    notes_data = store.read_notes(song_id, target)
    events = notes_data["events"]

    # Guarantee 1: sort by start time.
    events = sorted(events, key=lambda e: e["start_s"])

    chart_notes = []
    # Track the end time of the last note placed on each string, so we
    # can enforce guarantee 4 (no two notes overlap on the same string).
    last_end: dict[int, float] = {}

    for event in events:
        # Guarantee 2: skip events where end is not after start.
        if event["end_s"] <= event["start_s"]:
            continue

        midi = int(event["midi"])

        # Guarantee 5: drop notes outside the instrument's playable range.
        if midi < _MIDI_MIN or midi > _MIDI_MAX:
            continue

        # Find the first string (lowest to highest) where the fret is valid.
        assigned_string = None
        assigned_fret = None
        for string_idx, open_note in enumerate(_TUNING):
            fret = midi - open_note - _CAPO
            if 0 <= fret <= _FRET_MAX:
                assigned_string = string_idx
                assigned_fret = fret
                break

        # Guarantee 5: drop notes no string can play.
        if assigned_string is None:
            continue

        # Guarantee 4: drop notes that would overlap on the same string.
        prev_end = last_end.get(assigned_string, 0.0)
        if event["start_s"] < prev_end:
            continue

        last_end[assigned_string] = event["end_s"]

        chart_notes.append({
            "id": len(chart_notes),
            "start_s": float(event["start_s"]),
            "end_s": float(event["end_s"]),
            "midi": midi,
            "string": assigned_string,
            "fret": assigned_fret,
            "chord": None,  # stub: no chord grouping
        })

    chart_data = {
        "schema_version": 1,
        "instrument": target,
        "tuning": _TUNING,
        "capo": _CAPO,
        "notes": chart_notes,
    }
    store.write_chart(song_id, target, chart_data)
