# Compact Chess Engine

A small self-contained chess engine written in Python. It plays full legal
chess (including castling, en passant and pawn promotion) and communicates
with a standard UCI-like text protocol on stdin/stdout.

Search: iterative alpha-beta with a simple node budget and a king-capture
safety check, so lines that leave the king en prise are cut off immediately.

Evaluation: piece-square tables tuned for middlegame play, plus mate,
stalemate and draw scoring.

The repo ships in two forms: v7_engine.py is the readable reference engine,
and main.py / main_golf.py contain the same logic compressed (LZMA + base85
payload decompressed at import time). The compressed loader stays under 4
kilobytes of source, which is the whole point of this exercise.

Run it: `python3.13 main.py` (environment variables set the endpoint and
credentials if you point it at a host service).
