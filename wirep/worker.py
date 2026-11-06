"""Worker process: claims jobs atomically (O_EXCL lock files) and runs them
until none are left. Many workers (GPU and CPU) can run side by side."""
import argparse
import json
import os
import sys
import time
import traceback

import torch

from .experiments import all_jobs
from .jobs import job_id, out_paths, run_job


def claim(lock_dir, jid):
    try:
        fd = os.open(os.path.join(lock_dir, jid + ".lock"), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--root", default="results")
    ap.add_argument("--name", default="w")
    ap.add_argument("--only", default="", help="comma-separated experiment prefixes")
    ap.add_argument("--light-only", action="store_true", help="CPU workers: skip wavelet activations")
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    dev = torch.device(a.device)
    lock_dir = os.path.join(a.root, "_locks")
    os.makedirs(lock_dir, exist_ok=True)
    log = open(os.path.join(a.root, f"_worker_{a.name}.log"), "a", buffering=1)
    only = [x for x in a.only.split(",") if x]
    for j in all_jobs():
        if only and not any(j["exp"].startswith(o) for o in only):
            continue
        if a.light_only and ("Morlet" in j["act"] or "WIRE" in j["act"]):
            continue
        jid = job_id(j)
        if os.path.exists(out_paths(a.root, j)[0]) or not claim(lock_dir, jid):
            continue
        t0 = time.time()
        try:
            r = run_job(j, a.root, dev)
            msg = (f"{time.strftime('%H:%M:%S')} OK  {jid} {time.time() - t0:.0f}s "
                   f"lbfgs={r['lbfgs_evals']} mean_rel={r.get('mean_rel', float('nan')):.3e}")
        except Exception:
            msg = f"{time.strftime('%H:%M:%S')} ERR {jid}\n{traceback.format_exc()}"
            os.remove(os.path.join(lock_dir, jid + ".lock"))
        log.write(msg + "\n")
    log.write(f"{time.strftime('%H:%M:%S')} DONE\n")


if __name__ == "__main__":
    sys.exit(main())
