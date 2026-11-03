---
name: stack-trace-analyzer
description: Parses complex, multi-threaded, or nested stack traces and compiler error dumps to pinpoint the exact root-cause frame. Use when confronted with dense error logs.
---

# Stack Trace Analyzer

Deconstruct noisy, nested stack traces and compiler diagnostic dumps into prioritized root-cause locations.

## Trigger Conditions

Activate this skill when:
- A user provides a lengthy terminal error dump, exception chain, or gdb backtrace.
- A student asks: 'Where did this crash start?', 'Help me read this Java stack trace', or 'Find the line causing this traceback'.

## Execution Protocol

Execute this log triage sequence:

### 1. Noise Elimination & Frame Filtering
- Strip irrelevant third-party framework frames (e.g., runtime standard libraries, test runner internals).
- Isolate the application-level boundary: the first and last lines of user-authored code in the call stack.

### 2. Root Cause vs Cascading Failure Identification
- Identify the originating exception in nested chains ('Caused by: ...').
- Extract the exact error code, signal (e.g., SIGSEGV, SIGABRT, SIGFPE), or exception class.

### 3. Terminal Line & Variable Context Extraction
- Identify the exact source file, function, and line number where execution aborted.
- Reconstruct the local variable state that led to the fault based on the exception message.

### 4. Direct Actionable Remediation
- Provide the immediate 1–2 line code correction required at the fault location.

## Output Quality Rules

- Immediately lead with the exact file and line number—do not bury the culprit frame in paragraphs of text.
- Explain the causal chain clearly when multiple exceptions are nested.
