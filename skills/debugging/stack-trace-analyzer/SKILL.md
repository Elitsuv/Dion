---
name: stack-trace-analyzer
description: Parses dense compiler dumps and multithreaded stack traces to isolate the originating root-cause failure frame. Use when debugging runtime crashes.
---

# Stack Trace Analyzer

## Protocol
1. Filter -> Isolate app frames from library noise.
2. Pinpoint -> Identify failing frame, exception, args.
3. Trace -> Reconstruct call path from entry to crash.

## Guardrails
- Never output filler or pleasantries.
- Never confuse wrapper handlers with root causes.
- Never guess lines; quote directly from trace.

## Output Schema
### Root Cause
- Frame: [File:Line] -> Exception: [Class & Msg]
- Call Path: [Entry] -> [Helper] -> [Crash Site]
### Solution
[Targeted code correction]
