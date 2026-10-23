# Stub: fakes P3 (Demucs instrument separation).
# Real replacement: call demucs.api.Separator on mix.wav, write one WAV
# per stem (vocals, drums, bass, other/guitar), then mix all stems except
# <target> together to produce backing/<target>.wav.

from __future__ import annotations

import pathlib
import struct
import wave

from lodestone.store import SongStore


def separate(song_id: str, target: str, store: SongStore) -> None:
    """Write a silent stem and a silent backing track for the given target.

    The stub produces 1-second silent WAV files. Real code runs Demucs,
    which takes a few minutes and produces actual isolated instrument tracks.
    """
    _write_silent_wav(store.stem_path(song_id, target))
    _write_silent_wav(store.backing_path(song_id, target))


def _write_silent_wav(path: pathlib.Path, duration_s: float = 1.0) -> None:
    """Write a silent (all-zero) mono 16-bit PCM WAV to path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    sample_rate = 44100
    n_frames = int(sample_rate * duration_s)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)       # 16-bit PCM
        w.setframerate(sample_rate)
        w.writeframes(struct.pack(f"<{n_frames}h", *([0] * n_frames)))
