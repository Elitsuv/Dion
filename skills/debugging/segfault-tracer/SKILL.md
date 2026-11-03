---
name: segfault-tracer
description: Diagnoses segmentation faults and bus errors in C/C++ by analyzing pointer arithmetic, null references, and buffer overflows. Use when a binary terminates with SIGSEGV.
---

# Segfault Tracer

Isolate the precise pointer dereference, buffer overflow, or stack corruption causing SIGSEGV crashes.

## Trigger Conditions

Activate this skill when:
- A user's program crashes with 'Segmentation fault (core dumped)' or SIGBUS.
- A user provides a gdb `bt` (backtrace) or asks: 'Why am I getting a segfault in my linked list/tree/array?'.

## Execution Protocol

Follow this pointer forensics protocol:

### 1. Dereference Category Classification
Determine the exact physical cause of the memory fault:
- **Null Pointer Dereference**: Accessing address `0x0` or small offset (e.g., `ptr->next` where `ptr == NULL`).
- **Use-After-Free**: Reading or writing to an address already returned to the heap.
- **Out-of-Bounds Buffer Access**: Indexing past allocated array boundary into unmapped virtual memory.
- **Stack Overflow**: Infinite recursion exceeding thread stack quota.
- **Wild / Uninitialized Pointer**: Dereferencing garbage pointer values.

### 2. GDB Command & Inspection Guide
- Provide the exact GDB commands to reproduce and inspect the crash:
  ```gdb
  run
  backtrace
  frame 0
  info locals
  print *ptr
  ```

### 3. Code Anatomy & Boundary Fix
- Highlight the exact failing line and explain the invalid pointer state.
- Provide the corrected code with appropriate boundary checks and initialization guards.

## Output Quality Rules

- Explain the physical virtual memory mechanism (unmapped page, permission violation).
- Check loop termination conditions and off-by-one indices thoroughly.
