# Stub: fakes P4 (Basic Pitch note transcription).
# Real replacement: call basic_pitch.inference.predict on
# stems/<target>.wav and convert numpy output to plain Python floats
# before writing (Basic Pitch returns numpy types, not JSON-serialisable).

from lodestone.store import SongStore


# Three notes that cover low, mid, and high guitar range.
# All have start_s < end_s, midi in [40, 88], amplitude in [0.0, 1.0],
# and are sorted by start_s so the chart stub receives valid input.
_STUB_EVENTS = [
    {"start_s": 0.5, "end_s": 1.0, "midi": 40, "amplitude": 0.8},
    {"start_s": 1.5, "end_s": 2.0, "midi": 52, "amplitude": 0.7},
    {"start_s": 2.5, "end_s": 3.0, "midi": 64, "amplitude": 0.9},
]


def transcribe(song_id: str, target: str, store: SongStore) -> None:
    """Write a hardcoded raw note list for the given target.

    The stub emits three notes covering the guitar's playable range.
    Real code runs Basic Pitch on stems/<target>.wav and converts its
    numpy arrays to plain Python numbers before saving.
    """
    notes_data = {
        "schema_version": 1,
        "target": target,
        "events": _STUB_EVENTS,
    }
    store.write_notes(song_id, target, notes_data)
