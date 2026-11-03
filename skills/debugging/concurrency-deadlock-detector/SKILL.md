---
name: concurrency-deadlock-detector
description: Identifies race conditions, deadlocks, and synchronization pitfalls across threads, mutexes, and async routines. Use when multi-threaded code hangs or yields nondeterministic results.
---

# Concurrency Deadlock Detector

Detect, analyze, and resolve race conditions, thread deadlocks, and synchronization bugs in concurrent code.

## Trigger Conditions

Activate this skill when:
- A user reports that a multi-threaded program freezes, hangs intermittently, or yields inconsistent results.
- A student asks: 'Why is my threaded code hanging?', 'Find the race condition in this code', or 'Fix this mutex deadlock'.

## Execution Protocol

Follow this concurrency triage sequence:

### 1. Coffman Condition Audit
Verify if the 4 necessary conditions for deadlock are satisfied:
1. **Mutual Exclusion**: Exclusive access to resources.
2. **Hold and Wait**: Threads holding resources while requesting new ones.
3. **No Preemption**: Resources cannot be forcibly revoked.
4. **Circular Wait**: Thread A waits for Lock B held by Thread B, which waits for Lock A.

### 2. Lock Acquisition Ordering Analysis
- Map out the exact lock acquisition order across all threads.
- Identify the circular dependency inversion where Lock X is acquired before Lock Y in Thread 1, but Lock Y before Lock X in Thread 2.

### 3. Data Race & Critical Section Triage
- Identify shared mutable variables accessed without synchronized mutual exclusion.
- Check for atomicity violations and false sharing.

### 4. Resolution Strategy
Apply the appropriate concurrency pattern:
- Enforce a strict global lock hierarchy (always acquire Lock A before Lock B).
- Use `std::lock` / `try_lock` or atomic operations where appropriate.
- Eliminate shared state using thread-local storage or message-passing queues.

## Output Quality Rules

- Detail the exact interleaving of thread execution that triggers the bug.
- Avoid vague advice like 'add more locks'—minimize critical section scope.
