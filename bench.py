"""Quick timing benchmark: a short run on a given device, extrapolated to the full budget."""
import argparse
import tempfile
import time

import torch

from wirep import jobs

ap = argparse.ArgumentParser()
ap.add_argument("--device", default="cuda")
ap.add_argument("--threads", type=int, default=0)
ap.add_argument("--act", default="WIRE-P")
ap.add_argument("--kind", default="forward")
ap.add_argument("--disease", default="COVID-19")
a = ap.parse_args()
if a.threads:
    torch.set_num_threads(a.threads)
dev = torch.device(a.device)
budget = {"n_p1": 150, "n_p2": 150, "n_lbfgs": 100}
j = {"exp": "bench", "kind": a.kind, "disease": a.disease, "act": a.act, "seed": 42}
t0 = time.time()
r = jobs.run_job(j, tempfile.mkdtemp(), dev, budget=budget)
el = time.time() - t0
adam_steps, lb = 300, r["lbfgs_evals"]
print(f"{a.device} thr={a.threads} {a.act}: {el:.1f}s for 300 Adam + {lb} LBFGS evals "
      f"-> est. full run ~{el / (300 + lb) * (8000 + 3000 * 1.2) / 60:.1f} min | mean_rel={r.get('mean_rel', r.get('rmse_train'))}")
