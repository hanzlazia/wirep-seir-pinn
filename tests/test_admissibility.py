"""Numerical check of the zero-mean (admissibility) property of each wavelet activation.
Run with `python -m pytest tests` or `python tests/test_admissibility.py` (prints a table)."""
import os
import sys
import warnings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import torch
from scipy.integrate import IntegrationWarning, quad
from scipy.special import gamma, kv

from wirep.core import rational_cos_ratio

CASES = [(0.5, 4, 4), (1.25, 4, 4), (2, 4, 4), (1.25, 0.1, 2), (2, 1, 1.5), (0.5, 0.5, 1.2), (1.0, 10, 8)]


def integral(f):
    # split integral; heavy tails need the infinite-range QUADPACK routine
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)
        return sum(quad(f, a, b, limit=2000)[0] for a, b in [(-np.inf, -50), (-50, 0), (0, 50), (50, np.inf)])


def wirep_case(w, a, p):
    phi = np.arctan(a * w)
    env = lambda z: (1 + a * z * z) ** (-p)
    k_quad = integral(lambda z: np.cos(w * z) * env(z)) / integral(env)
    k_cf = rational_cos_ratio(torch.tensor([float(w)]), torch.tensor([float(a)]), torch.tensor([float(p)])).item()
    i_orig = integral(lambda z: np.cos(w * z + phi) * env(z))
    i_adm = integral(lambda z: (np.cos(w * z + phi) - np.cos(phi) * k_cf) * env(z))
    return k_quad, k_cf, i_orig, i_adm


def kappa_exact(w, a, p):
    x, nu = w / np.sqrt(a), p - 0.5
    return 2.0 / gamma(nu) * (x / 2) ** nu * kv(nu, x)


def test_wirep_mean_closed_form_and_correction():
    for w, a, p in CASES:
        k_quad, k_cf, i_orig, i_adm = wirep_case(w, a, p)
        assert abs(k_cf - kappa_exact(w, a, p)) < 1e-10, (w, a, p)
        # adaptive quadrature is only accurate to ~1e-7 for the heaviest tails (p close to 1)
        assert abs(k_quad - k_cf) < 1e-6, (w, a, p)
        assert i_orig > 1e-3, "WIRE-P is never zero-mean"
        assert abs(i_adm) < 1e-6, "WIRE-P-A is zero-mean"


def test_morlet_mean_and_correction():
    for w in (0.5, 1.25, 2.0):
        m = integral(lambda z: np.cos(w * z) * np.exp(-z * z / 2))
        c = integral(lambda z: (np.cos(w * z) - np.exp(-w * w / 2)) * np.exp(-z * z / 2))
        assert abs(m - np.sqrt(2 * np.pi) * np.exp(-w * w / 2)) < 1e-8
        assert abs(c) < 1e-8


if __name__ == "__main__":
    print(f"{'omega':>6} {'alpha':>6} {'p':>5} | {'int WIRE-P':>11} {'int WIRE-P-A':>13} | kappa quad vs closed form")
    for w, a, p in CASES:
        k_quad, k_cf, i_orig, i_adm = wirep_case(w, a, p)
        print(f"{w:6.2f} {a:6.2f} {p:5.2f} | {i_orig:11.4e} {i_adm:13.2e} | {k_quad:.10f} {k_cf:.10f}")
    for w in (0.5, 1.25, 2.0):
        m = integral(lambda z: np.cos(w * z) * np.exp(-z * z / 2))
        c = integral(lambda z: (np.cos(w * z) - np.exp(-w * w / 2)) * np.exp(-z * z / 2))
        print(f"Morlet omega={w}: int={m:.4f}  complete-Morlet int={c:.1e}")
