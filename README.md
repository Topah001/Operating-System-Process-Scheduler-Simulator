# Operating System Process Scheduler Simulator

A Python 3.13+ command-line simulator for First-Come, First-Served (FCFS), non-preemptive Shortest Job First (SJF), and Round Robin scheduling. It prints per-process waiting/turnaround times and averages. CPU time is integer ticks; processes arriving at the same tick are ordered by ID for deterministic ties.

## Run

```powershell
python scheduler.py
python -m unittest -v
```

The script runs an illustrative workload. Import `Process(pid, arrival, burst)`, then call `fcfs(processes)`, `sjf(processes)`, or `round_robin(processes, quantum)`. Invalid IDs, negative/noninteger arrivals, nonpositive/noninteger bursts, empty input, and invalid quantum raise `ValueError`. Waiting time = turnaround ? burst; turnaround = completion ? arrival. This is a teaching model and does not model I/O or context-switch overhead.
