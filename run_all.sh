#!/usr/bin/env bash
# Runs the complete study: 8 GPU workers + 4 CPU workers share one job queue.
# Safe to re-run: finished jobs are skipped. Stale locks of killed workers
# must be cleared (results/_locks) before restarting.
cd "$(dirname "$0")"
mkdir -p results
for i in 1 2 3 4 5 6 7 8; do
  python -m wirep.worker --device cuda --threads 1 --name gpu$i &
done
for i in 1 2 3 4; do
  python -m wirep.worker --device cpu --threads 4 --light-only --name cpu$i &
done
wait
echo "ALL WORKERS FINISHED"
