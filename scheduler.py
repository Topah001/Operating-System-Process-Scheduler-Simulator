"""Small, deterministic CPU scheduling simulator."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Process:
    pid: str
    arrival: int
    burst: int

@dataclass(frozen=True)
class Result:
    pid: str
    start: int
    completion: int
    waiting: int
    turnaround: int

def validate(processes):
    processes = list(processes)
    if not processes:
        raise ValueError("at least one process is required")
    ids = set()
    for p in processes:
        if not isinstance(p.pid, str) or not p.pid.strip() or p.pid in ids:
            raise ValueError("process IDs must be unique, non-empty strings")
        ids.add(p.pid)
        if isinstance(p.arrival, bool) or not isinstance(p.arrival, int) or p.arrival < 0:
            raise ValueError("arrival times must be non-negative integers")
        if isinstance(p.burst, bool) or not isinstance(p.burst, int) or p.burst <= 0:
            raise ValueError("burst times must be positive integers")
    return processes

def _results(processes, timeline):
    finished = []
    for p, start, end in timeline:
        turnaround = end - p.arrival
        finished.append(Result(p.pid, start, end, turnaround - p.burst, turnaround))
    return finished

def fcfs(processes):
    pending = sorted(validate(processes), key=lambda p: (p.arrival, p.pid))
    timeline, now = [], 0
    for p in pending:
        start = max(now, p.arrival)
        now = start + p.burst
        timeline.append((p, start, now))
    return _results(pending, timeline)

def sjf(processes):
    pending = validate(processes)
    timeline, now = [], 0
    while pending:
        ready = [p for p in pending if p.arrival <= now]
        if not ready:
            now = min(p.arrival for p in pending)
            ready = [p for p in pending if p.arrival <= now]
        p = min(ready, key=lambda p: (p.burst, p.arrival, p.pid))
        pending.remove(p)
        start, now = now, now + p.burst
        timeline.append((p, start, now))
    return _results(processes, timeline)

def round_robin(processes, quantum):
    pending = sorted(validate(processes), key=lambda p: (p.arrival, p.pid))
    if isinstance(quantum, bool) or not isinstance(quantum, int) or quantum <= 0:
        raise ValueError("quantum must be a positive integer")
    remaining = {p.pid: p.burst for p in pending}
    first_start, completion = {}, {}
    queue, i, now = [], 0, 0
    while i < len(pending) or queue:
        if not queue and i < len(pending) and now < pending[i].arrival:
            now = pending[i].arrival
        while i < len(pending) and pending[i].arrival <= now:
            queue.append(pending[i]); i += 1
        p = queue.pop(0)
        first_start.setdefault(p.pid, now)
        run = min(quantum, remaining[p.pid])
        now += run
        remaining[p.pid] -= run
        while i < len(pending) and pending[i].arrival <= now:
            queue.append(pending[i]); i += 1
        if remaining[p.pid]:
            queue.append(p)
        else:
            completion[p.pid] = now
    return [Result(p.pid, first_start[p.pid], completion[p.pid], completion[p.pid]-p.arrival-p.burst, completion[p.pid]-p.arrival) for p in pending]

def averages(results):
    return {"average_waiting": sum(r.waiting for r in results)/len(results), "average_turnaround": sum(r.turnaround for r in results)/len(results)}


def demo():
    jobs = [Process("P1", 0, 5), Process("P2", 1, 3), Process("P3", 2, 1), Process("P4", 4, 2)]
    for name, run in (("FCFS", fcfs), ("Non-preemptive SJF", sjf)):
        results = run(jobs)
        print(f"\n{name}")
        for r in results: print(f"{r.pid}: start={r.start}, finish={r.completion}, wait={r.waiting}, turnaround={r.turnaround}")
        print(averages(results))
    results = round_robin(jobs, 2)
    print("\nRound Robin (quantum=2)")
    for r in results: print(f"{r.pid}: first_start={r.start}, finish={r.completion}, wait={r.waiting}, turnaround={r.turnaround}")
    print(averages(results))

if __name__ == "__main__": demo()
