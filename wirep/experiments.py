"""Full experiment matrix of the revised study, in execution-priority order."""

SEEDS_ORIG = [42, 7, 123, 2024, 314]
SEEDS = SEEDS_ORIG + [1, 2, 3, 4, 5]          # 10 matched seeds
DISEASES = ["Hantavirus", "SARS-2003", "COVID-19"]
WAVELETS = ["WIRE-P", "WIRE-P-A", "WIRE-P(phi=0)", "MV-Morlet", "MV-Morlet-A", "MV-Morlet+"]
STANDARD = ["Tanh", "ReLU", "Sigmoid", "SIREN", "Fourier"]
ALL_ACTS = WAVELETS + STANDARD
CORE = ["WIRE-P", "WIRE-P-A", "MV-Morlet", "Tanh"]


def all_jobs():
    J = []
    # E0: reproduction of the submitted numbers with the ORIGINAL (detached) L-BFGS gradient
    for d in DISEASES:
        for a in ["WIRE-P", "MV-Morlet", "Tanh"]:
            for s in SEEDS_ORIG:
                J.append(dict(exp="E0_legacy", kind="forward", disease=d, act=a, seed=s, legacy=True))
    # E1: main forward benchmark, corrected residual gradient, 11 activations x 10 seeds
    for s in SEEDS:
        for d in DISEASES:
            for a in ALL_ACTS:
                J.append(dict(exp="E1_main", kind="forward", disease=d, act=a, seed=s))
    # E5: real data (1978 boarding-school influenza), all activations
    for s in SEEDS:
        for a in ALL_ACTS:
            J.append(dict(exp="E5_real", kind="real", disease="BoardingSchool-1978", act=a, seed=s))
    # E4: inverse problem, only noisy I(t) observed, beta & gamma unknown
    for s in SEEDS:
        for nz in (0.0, 0.05, 0.10):
            for d in DISEASES:
                for a in CORE + ["Sigmoid"]:
                    J.append(dict(exp="E4_inverse", kind="inverse", disease=d, act=a, seed=s, noise=nz))
    # E2: noisy anchors (forward problem), 2% and 5%
    for s in SEEDS:
        for nz in (0.02, 0.05):
            for d in DISEASES:
                for a in CORE:
                    J.append(dict(exp="E2_noise", kind="forward", disease=d, act=a, seed=s, noise=nz))
    # E3: smaller architecture 3x32
    for s in SEEDS:
        for d in DISEASES:
            for a in CORE:
                J.append(dict(exp="E3_arch", kind="forward", disease=d, act=a, seed=s,
                              layers=[1, 32, 32, 32, 4]))
    return J
