---
name: memory-leak-hunter
description: Analyzes Valgrind logs, AddressSanitizer output, and memory profiling reports to trace unreleased allocations and pointer leaks. Use when debugging C/C++ memory management.
---

# Memory Leak Hunter

Diagnose heap memory leaks, dangling pointers, and double-free errors using Valgrind and AddressSanitizer diagnostics.

## Trigger Conditions

Activate this skill when:
- A user provides a Valgrind summary, ASan log, or reports growing resident memory in C/C++/Rust code.
- A student asks: 'Fix this Valgrind error', 'Why is my program leaking memory?', or 'Analyze this AddressSanitizer output'.

## Execution Protocol

Follow this memory analysis workflow:

### 1. Leak Categorization
Classify Valgrind leak types from the summary:
- **Definitely Lost**: Pointer to allocated block lost completely (critical bug).
- **Indirectly Lost**: Structure pointing to other lost structures (cascade leak).
- **Possibly Lost**: Pointer shifted into middle of allocated block.
- **Still Reachable**: Memory allocated and reachable at exit but not freed (lazy cleanup).

### 2. Allocation vs Deallocation Site Mapping
- Locate the exact stack trace where `malloc`, `calloc`, or `new` allocated the leaked bytes.
- Trace the execution path to identify the branch or early return statement that bypassed `free()` or `delete`.

### 3. Lifecycle Ownership Audit
- Define the clear ownership lifecycle for the buffer:
  - Who allocates?
  - Who borrows?
  - Who is guaranteed to free?

### 4. Patch & RAII Modernization
- Provide the surgical fix ensuring all exit paths deallocate memory.
- Where applicable in C++, demonstrate the modern RAII alternative (`std::unique_ptr`, `std::vector`).

## Output Quality Rules

- Ensure every allocated byte has an associated deallocation path.
- Always check error-handling branches, which are the most common source of leaked allocations.
