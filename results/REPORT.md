# Progress: E0_legacy 45/45, E1_main 330/330, E2_noise 240/240, E3_arch 120/120, E4_inverse 450/450, E5_real 110/110
# mean train time (s) by activation: Fourier=1761, MV-Morlet=3325, MV-Morlet+=3638, MV-Morlet-A=3468, ReLU=729, SIREN=1712, Sigmoid=1369, Tanh=1342, WIRE-P=4447, WIRE-P(phi=0)=4258, WIRE-P-A=5417

## E0 — reproduction (original detached L-BFGS gradient) vs corrected gradient, 5 original seeds
Hantavirus  MV-Morlet  legacy: relL2=1.348e-03 peak=0.1031% phys=3.252e-08 lbfgs=1080 (n=5) | corrected: relL2=7.102e-04 peak=0.0350% phys=5.709e-09 lbfgs=3614 (n=5)
Hantavirus  WIRE-P     legacy: relL2=5.156e-04 peak=0.0242% phys=2.684e-09 lbfgs=1655 (n=5) | corrected: relL2=4.695e-04 peak=0.0099% phys=1.427e-09 lbfgs=3751 (n=5)
Hantavirus  Tanh       legacy: relL2=1.061e-03 peak=0.0529% phys=1.328e-08 lbfgs=2502 (n=5) | corrected: relL2=8.161e-04 peak=0.0351% phys=5.914e-09 lbfgs=3674 (n=5)
SARS-2003   MV-Morlet  legacy: relL2=7.334e-03 peak=0.4053% phys=7.905e-07 lbfgs=238 (n=5) | corrected: relL2=1.510e-03 peak=0.0290% phys=2.336e-08 lbfgs=3642 (n=5)
SARS-2003   WIRE-P     legacy: relL2=2.631e-03 peak=0.0325% phys=5.361e-08 lbfgs=703 (n=5) | corrected: relL2=1.865e-03 peak=0.0172% phys=2.289e-08 lbfgs=3750 (n=5)
SARS-2003   Tanh       legacy: relL2=3.900e-02 peak=1.7060% phys=1.566e-05 lbfgs=119 (n=5) | corrected: relL2=1.546e-03 peak=0.0323% phys=3.265e-08 lbfgs=3456 (n=5)
COVID-19    MV-Morlet  legacy: relL2=1.698e-02 peak=0.5650% phys=3.680e-06 lbfgs=66 (n=5) | corrected: relL2=2.590e-03 peak=0.0135% phys=4.410e-08 lbfgs=3623 (n=5)
COVID-19    WIRE-P     legacy: relL2=5.007e-03 peak=0.0270% phys=1.418e-07 lbfgs=239 (n=5) | corrected: relL2=1.525e-03 peak=0.0072% phys=1.434e-08 lbfgs=3751 (n=5)
COVID-19    Tanh       legacy: relL2=2.299e-02 peak=0.5251% phys=1.637e-05 lbfgs=57 (n=5) | corrected: relL2=4.050e-03 peak=0.0159% phys=4.731e-08 lbfgs=3742 (n=5)

## E1_main: mean ± sd (n seeds)
  Hantavirus  mean_rel  WIRE-P=4.987e-04±8.0e-05(n=10) | WIRE-P-A=5.688e-04±9.2e-05(n=10) | WIRE-P(phi=0)=7.774e-04±1.1e-04(n=10) | MV-Morlet=7.631e-04±3.0e-04(n=10) | MV-Morlet-A=6.765e-04±1.3e-04(n=10) | MV-Morlet+=8.340e-04±2.4e-04(n=10) | Tanh=8.323e-04±1.9e-04(n=10) | ReLU=3.304e-03±1.2e-03(n=10) | Sigmoid=9.914e-04±4.2e-04(n=10) | SIREN=2.034e-03±2.2e-04(n=10) | Fourier=1.335e-03±3.0e-04(n=10)
  Hantavirus  peak_err  WIRE-P=1.133e-02±9.5e-03(n=10) | WIRE-P-A=1.330e-02±1.0e-02(n=10) | WIRE-P(phi=0)=1.188e-02±9.5e-03(n=10) | MV-Morlet=4.271e-02±4.3e-02(n=10) | MV-Morlet-A=2.826e-02±3.0e-02(n=10) | MV-Morlet+=5.213e-02±3.3e-02(n=10) | Tanh=3.675e-02±2.1e-02(n=10) | ReLU=5.927e-01±2.8e-01(n=10) | Sigmoid=6.542e-02±3.6e-02(n=10) | SIREN=1.971e-02±1.4e-02(n=10) | Fourier=1.518e-02±1.0e-02(n=10)
  Hantavirus  phys_res  WIRE-P=1.930e-09±8.7e-10(n=10) | WIRE-P-A=2.908e-09±1.2e-09(n=10) | WIRE-P(phi=0)=5.613e-09±2.5e-09(n=10) | MV-Morlet=6.309e-09±4.8e-09(n=10) | MV-Morlet-A=5.564e-09±3.5e-09(n=10) | MV-Morlet+=7.442e-09±4.8e-09(n=10) | Tanh=5.497e-09±2.2e-09(n=10) | ReLU=6.174e-07±2.9e-07(n=10) | Sigmoid=1.070e-08±9.2e-09(n=10) | SIREN=1.550e-07±2.7e-08(n=10) | Fourier=7.879e-08±2.6e-08(n=10)
  SARS-2003   mean_rel  WIRE-P=1.748e-03±4.6e-04(n=10) | WIRE-P-A=1.837e-03±5.2e-04(n=10) | WIRE-P(phi=0)=2.921e-03±7.8e-04(n=10) | MV-Morlet=1.694e-03±4.7e-04(n=10) | MV-Morlet-A=1.688e-03±5.5e-04(n=10) | MV-Morlet+=1.703e-03±5.5e-04(n=10) | Tanh=1.497e-03±2.8e-04(n=10) | ReLU=4.880e-03±9.7e-04(n=10) | Sigmoid=1.202e-03±4.2e-04(n=10) | SIREN=4.459e-03±1.1e-03(n=10) | Fourier=3.475e-03±1.0e-03(n=10)
  SARS-2003   peak_err  WIRE-P=1.797e-02±1.0e-02(n=10) | WIRE-P-A=8.817e-03±8.0e-03(n=10) | WIRE-P(phi=0)=1.650e-02±1.2e-02(n=10) | MV-Morlet=3.893e-02±2.7e-02(n=10) | MV-Morlet-A=3.816e-02±2.5e-02(n=10) | MV-Morlet+=4.845e-02±1.7e-02(n=10) | Tanh=3.720e-02±2.3e-02(n=10) | ReLU=9.723e-02±1.0e-01(n=10) | Sigmoid=3.381e-02±1.5e-02(n=10) | SIREN=6.509e-03±4.8e-03(n=10) | Fourier=7.116e-03±5.3e-03(n=10)
  SARS-2003   phys_res  WIRE-P=2.152e-08±1.0e-08(n=10) | WIRE-P-A=2.441e-08±1.1e-08(n=10) | WIRE-P(phi=0)=7.777e-08±4.4e-08(n=10) | MV-Morlet=3.060e-08±1.7e-08(n=10) | MV-Morlet-A=3.378e-08±2.3e-08(n=10) | MV-Morlet+=2.397e-08±1.1e-08(n=10) | Tanh=3.789e-08±1.8e-08(n=10) | ReLU=1.337e-06±3.7e-07(n=10) | Sigmoid=2.082e-08±1.3e-08(n=10) | SIREN=2.900e-07±6.8e-08(n=10) | Fourier=2.044e-07±9.8e-08(n=10)
  COVID-19    mean_rel  WIRE-P=1.766e-03±4.8e-04(n=10) | WIRE-P-A=2.052e-03±2.6e-04(n=10) | WIRE-P(phi=0)=3.877e-03±4.7e-04(n=10) | MV-Morlet=2.405e-03±6.0e-04(n=10) | MV-Morlet-A=3.029e-03±6.4e-04(n=10) | MV-Morlet+=2.540e-03±7.7e-04(n=10) | Tanh=3.371e-03±2.1e-03(n=10) | ReLU=1.054e-02±1.0e-03(n=10) | Sigmoid=2.711e-03±2.0e-03(n=10) | SIREN=5.454e-03±7.9e-04(n=10) | Fourier=5.915e-03±1.7e-03(n=10)
  COVID-19    peak_err  WIRE-P=9.157e-03±7.6e-03(n=10) | WIRE-P-A=1.017e-02±4.9e-03(n=10) | WIRE-P(phi=0)=1.583e-02±1.6e-02(n=10) | MV-Morlet=1.991e-02±1.8e-02(n=10) | MV-Morlet-A=3.299e-02±2.3e-02(n=10) | MV-Morlet+=2.741e-02±2.5e-02(n=10) | Tanh=2.483e-02±2.5e-02(n=10) | ReLU=1.023e-01±8.5e-02(n=10) | Sigmoid=3.280e-02±3.8e-02(n=10) | SIREN=1.070e-02±4.7e-03(n=10) | Fourier=5.123e-03±4.2e-03(n=10)
  COVID-19    phys_res  WIRE-P=1.883e-08±1.3e-08(n=10) | WIRE-P-A=2.486e-08±7.2e-09(n=10) | WIRE-P(phi=0)=7.810e-08±2.4e-08(n=10) | MV-Morlet=3.998e-08±1.9e-08(n=10) | MV-Morlet-A=6.945e-08±2.2e-08(n=10) | MV-Morlet+=4.642e-08±2.7e-08(n=10) | Tanh=4.244e-08±2.5e-08(n=10) | ReLU=1.788e-06±6.5e-07(n=10) | Sigmoid=5.862e-08±4.8e-08(n=10) | SIREN=2.409e-07±8.5e-08(n=10) | Fourier=2.335e-07±1.3e-07(n=10)

## E1_main: mean ± sd (n seeds)
  Hantavirus  time      WIRE-P=4.445e+03±2.0e+02(n=10) | WIRE-P-A=5.527e+03±3.7e+02(n=10) | WIRE-P(phi=0)=4.253e+03±2.0e+02(n=10) | MV-Morlet=3.393e+03±2.1e+02(n=10) | MV-Morlet-A=3.489e+03±1.6e+02(n=10) | MV-Morlet+=3.641e+03±1.8e+02(n=10) | Tanh=1.343e+03±4.5e+01(n=10) | ReLU=7.371e+02±1.8e+01(n=10) | Sigmoid=1.370e+03±1.1e+02(n=10) | SIREN=1.703e+03±5.7e+01(n=10) | Fourier=1.772e+03±9.7e+01(n=10)
  Hantavirus  lbfgs     WIRE-P=3.626e+03±2.0e+02(n=10) | WIRE-P-A=3.561e+03±1.5e+02(n=10) | WIRE-P(phi=0)=3.682e+03±1.5e+02(n=10) | MV-Morlet=3.599e+03±2.2e+02(n=10) | MV-Morlet-A=3.534e+03±2.2e+02(n=10) | MV-Morlet+=3.590e+03±2.6e+02(n=10) | Tanh=3.558e+03±2.0e+02(n=10) | ReLU=1.369e+02±5.7e+01(n=10) | Sigmoid=3.484e+03±5.8e+02(n=10) | SIREN=3.500e+03±2.9e+02(n=10) | Fourier=3.543e+03±1.8e+02(n=10)
  SARS-2003   time      WIRE-P=4.495e+03±1.5e+02(n=10) | WIRE-P-A=5.376e+03±1.9e+02(n=10) | WIRE-P(phi=0)=4.254e+03±1.8e+02(n=10) | MV-Morlet=3.270e+03±1.7e+02(n=10) | MV-Morlet-A=3.501e+03±1.5e+02(n=10) | MV-Morlet+=3.690e+03±1.9e+02(n=10) | Tanh=1.350e+03±6.9e+01(n=10) | ReLU=7.246e+02±2.6e+01(n=10) | Sigmoid=1.375e+03±4.4e+01(n=10) | SIREN=1.719e+03±4.3e+01(n=10) | Fourier=1.770e+03±3.3e+01(n=10)
  SARS-2003   lbfgs     WIRE-P=3.745e+03±1.8e+01(n=10) | WIRE-P-A=3.748e+03±6.2e+00(n=10) | WIRE-P(phi=0)=3.751e+03±4.8e-01(n=10) | MV-Morlet=3.661e+03±1.9e+02(n=10) | MV-Morlet-A=3.709e+03±1.3e+02(n=10) | MV-Morlet+=3.749e+03±3.7e+00(n=10) | Tanh=3.483e+03±1.3e+02(n=10) | ReLU=8.630e+01±3.7e+01(n=10) | Sigmoid=3.672e+03±1.6e+02(n=10) | SIREN=3.640e+03±1.4e+02(n=10) | Fourier=3.517e+03±2.2e+02(n=10)
  COVID-19    time      WIRE-P=4.400e+03±1.3e+02(n=10) | WIRE-P-A=5.346e+03±2.0e+02(n=10) | WIRE-P(phi=0)=4.268e+03±1.9e+02(n=10) | MV-Morlet=3.313e+03±1.3e+02(n=10) | MV-Morlet-A=3.413e+03±2.6e+02(n=10) | MV-Morlet+=3.584e+03±2.6e+02(n=10) | Tanh=1.331e+03±3.8e+01(n=10) | ReLU=7.239e+02±1.4e+01(n=10) | Sigmoid=1.361e+03±5.9e+01(n=10) | SIREN=1.713e+03±5.3e+01(n=10) | Fourier=1.743e+03±8.2e+01(n=10)
  COVID-19    lbfgs     WIRE-P=3.750e+03±5.3e-01(n=10) | WIRE-P-A=3.750e+03±5.2e-01(n=10) | WIRE-P(phi=0)=3.750e+03±5.2e-01(n=10) | MV-Morlet=3.681e+03±1.3e+02(n=10) | MV-Morlet-A=3.693e+03±1.8e+02(n=10) | MV-Morlet+=3.659e+03±1.9e+02(n=10) | Tanh=3.669e+03±1.8e+02(n=10) | ReLU=7.370e+01±2.6e+01(n=10) | Sigmoid=3.725e+03±8.1e+01(n=10) | SIREN=3.750e+03±4.8e-01(n=10) | Fourier=3.537e+03±2.0e+02(n=10)

## E1_main: ranking by mean (geometric mean over seeds in brackets)
  Hantavirus  mean_rel : WIRE-P=4.99e-04[4.93e-04]  WIRE-P-A=5.69e-04[5.63e-04]  MV-Morlet-A=6.76e-04[6.66e-04]  MV-Morlet=7.63e-04[7.21e-04]  WIRE-P(phi=0)=7.77e-04[7.71e-04]  Tanh=8.32e-04[8.13e-04]  MV-Morlet+=8.34e-04[8.04e-04]  Sigmoid=9.91e-04[8.98e-04]  Fourier=1.34e-03[1.31e-03]  SIREN=2.03e-03[2.02e-03]  ReLU=3.30e-03[3.13e-03]
  Hantavirus  peak_err : WIRE-P=1.13e-02[6.98e-03]  WIRE-P(phi=0)=1.19e-02[6.43e-03]  WIRE-P-A=1.33e-02[8.34e-03]  Fourier=1.52e-02[1.23e-02]  SIREN=1.97e-02[1.54e-02]  MV-Morlet-A=2.83e-02[1.92e-02]  Tanh=3.68e-02[2.72e-02]  MV-Morlet=4.27e-02[2.42e-02]  MV-Morlet+=5.21e-02[4.22e-02]  Sigmoid=6.54e-02[5.44e-02]  ReLU=5.93e-01[5.32e-01]
  Hantavirus  phys_res : WIRE-P=1.93e-09[1.77e-09]  WIRE-P-A=2.91e-09[2.64e-09]  Tanh=5.50e-09[5.09e-09]  MV-Morlet-A=5.56e-09[4.63e-09]  WIRE-P(phi=0)=5.61e-09[5.06e-09]  MV-Morlet=6.31e-09[4.81e-09]  MV-Morlet+=7.44e-09[6.12e-09]  Sigmoid=1.07e-08[6.41e-09]  Fourier=7.88e-08[7.46e-08]  SIREN=1.55e-07[1.53e-07]  ReLU=6.17e-07[5.66e-07]
  SARS-2003   mean_rel : Sigmoid=1.20e-03[1.15e-03]  Tanh=1.50e-03[1.47e-03]  MV-Morlet-A=1.69e-03[1.59e-03]  MV-Morlet=1.69e-03[1.64e-03]  MV-Morlet+=1.70e-03[1.62e-03]  WIRE-P=1.75e-03[1.69e-03]  WIRE-P-A=1.84e-03[1.78e-03]  WIRE-P(phi=0)=2.92e-03[2.84e-03]  Fourier=3.47e-03[3.34e-03]  SIREN=4.46e-03[4.32e-03]  ReLU=4.88e-03[4.79e-03]
  SARS-2003   peak_err : SIREN=6.51e-03[4.82e-03]  Fourier=7.12e-03[5.29e-03]  WIRE-P-A=8.82e-03[5.99e-03]  WIRE-P(phi=0)=1.65e-02[1.17e-02]  WIRE-P=1.80e-02[1.46e-02]  Sigmoid=3.38e-02[2.98e-02]  Tanh=3.72e-02[2.83e-02]  MV-Morlet-A=3.82e-02[2.96e-02]  MV-Morlet=3.89e-02[3.14e-02]  MV-Morlet+=4.85e-02[4.53e-02]  ReLU=9.72e-02[6.17e-02]
  SARS-2003   phys_res : Sigmoid=2.08e-08[1.70e-08]  WIRE-P=2.15e-08[1.93e-08]  MV-Morlet+=2.40e-08[2.17e-08]  WIRE-P-A=2.44e-08[2.23e-08]  MV-Morlet=3.06e-08[2.67e-08]  MV-Morlet-A=3.38e-08[2.85e-08]  Tanh=3.79e-08[3.28e-08]  WIRE-P(phi=0)=7.78e-08[6.79e-08]  Fourier=2.04e-07[1.87e-07]  SIREN=2.90e-07[2.83e-07]  ReLU=1.34e-06[1.29e-06]
  COVID-19    mean_rel : WIRE-P=1.77e-03[1.71e-03]  WIRE-P-A=2.05e-03[2.04e-03]  MV-Morlet=2.41e-03[2.34e-03]  MV-Morlet+=2.54e-03[2.45e-03]  Sigmoid=2.71e-03[2.35e-03]  MV-Morlet-A=3.03e-03[2.97e-03]  Tanh=3.37e-03[2.86e-03]  WIRE-P(phi=0)=3.88e-03[3.85e-03]  SIREN=5.45e-03[5.41e-03]  Fourier=5.91e-03[5.71e-03]  ReLU=1.05e-02[1.05e-02]
  COVID-19    peak_err : Fourier=5.12e-03[3.07e-03]  WIRE-P=9.16e-03[6.17e-03]  WIRE-P-A=1.02e-02[8.82e-03]  SIREN=1.07e-02[9.70e-03]  WIRE-P(phi=0)=1.58e-02[5.55e-03]  MV-Morlet=1.99e-02[1.08e-02]  Tanh=2.48e-02[1.21e-02]  MV-Morlet+=2.74e-02[1.44e-02]  Sigmoid=3.28e-02[2.04e-02]  MV-Morlet-A=3.30e-02[1.65e-02]  ReLU=1.02e-01[7.47e-02]
  COVID-19    phys_res : WIRE-P=1.88e-08[1.61e-08]  WIRE-P-A=2.49e-08[2.39e-08]  MV-Morlet=4.00e-08[3.67e-08]  Tanh=4.24e-08[3.67e-08]  MV-Morlet+=4.64e-08[3.98e-08]  Sigmoid=5.86e-08[4.85e-08]  MV-Morlet-A=6.95e-08[6.66e-08]  WIRE-P(phi=0)=7.81e-08[7.48e-08]  Fourier=2.34e-07[2.10e-07]  SIREN=2.41e-07[2.30e-07]  ReLU=1.79e-06[1.69e-06]

## E1_main: WIRE-P vs others  (paired over seeds; Holm over 3x3x10 tests)
  COVID-19    mean_rel  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.841 wins=8/10 p_W=0.1602 p_W,Holm=0.2109 p_t,Holm=0.1423 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  0.445 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    mean_rel  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.731 wins=7/10 p_W=0.0488 p_W,Holm=0.1484 p_t,Holm=0.1423 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.577 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0005 p_W,all=0.1758
  COVID-19    mean_rel  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.698 wins=9/10 p_W=0.0059 p_W,Holm=0.0293 p_t,Holm=0.0129 p_W,all=0.3105
  COVID-19    mean_rel  WIRE-P vs Tanh          n=10 ratio(GM)=  0.600 wins=8/10 p_W=0.0371 p_W,Holm=0.1484 p_t,Holm=0.1423 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P vs ReLU          n=10 ratio(GM)=  0.163 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    mean_rel  WIRE-P vs Sigmoid       n=10 ratio(GM)=  0.729 wins=7/10 p_W=0.1055 p_W,Holm=0.2109 p_t,Holm=0.1423 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P vs SIREN         n=10 ratio(GM)=  0.317 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    mean_rel  WIRE-P vs Fourier       n=10 ratio(GM)=  0.300 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    peak_err  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.699 wins=7/10 p_W=0.8457 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  1.113 wins=6/10 p_W=0.2754 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.571 wins=7/10 p_W=0.1934 p_W,Holm=0.9668 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.375 wins=8/10 p_W=0.0098 p_W,Holm=0.0879 p_t,Holm=1.0000 p_W,all=0.4785
  COVID-19    peak_err  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.429 wins=7/10 p_W=0.0273 p_W,Holm=0.2188 p_t,Holm=0.5461 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P vs Tanh          n=10 ratio(GM)=  0.511 wins=7/10 p_W=0.0488 p_W,Holm=0.2930 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P vs ReLU          n=10 ratio(GM)=  0.083 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0006 p_W,all=0.1758
  COVID-19    peak_err  WIRE-P vs Sigmoid       n=10 ratio(GM)=  0.303 wins=8/10 p_W=0.0371 p_W,Holm=0.2598 p_t,Holm=0.3369 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P vs SIREN         n=10 ratio(GM)=  0.636 wins=6/10 p_W=0.4316 p_W,Holm=1.0000 p_t,Holm=0.7029 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P vs Fourier       n=10 ratio(GM)=  2.009 wins=3/10 p_W=0.3750 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.674 wins=8/10 p_W=0.1055 p_W,Holm=0.1055 p_t,Holm=0.0455 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  0.216 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.439 wins=9/10 p_W=0.0273 p_W,Holm=0.0547 p_t,Holm=0.0158 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.242 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0009 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.405 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0024 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P vs Tanh          n=10 ratio(GM)=  0.439 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0091 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P vs ReLU          n=10 ratio(GM)=  0.010 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P vs Sigmoid       n=10 ratio(GM)=  0.332 wins=9/10 p_W=0.0137 p_W,Holm=0.0410 p_t,Holm=0.0086 p_W,all=0.6152
  COVID-19    phys_res  WIRE-P vs SIREN         n=10 ratio(GM)=  0.070 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P vs Fourier       n=10 ratio(GM)=  0.077 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.876 wins=7/10 p_W=0.3223 p_W,Holm=0.3223 p_t,Holm=0.1946 p_W,all=1.0000
  Hantavirus  mean_rel  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  0.640 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0002 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.684 wins=9/10 p_W=0.0039 p_W,Holm=0.0195 p_t,Holm=0.0176 p_W,all=0.2266
  Hantavirus  mean_rel  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.740 wins=9/10 p_W=0.0098 p_W,Holm=0.0195 p_t,Holm=0.0160 p_W,all=0.4785
  Hantavirus  mean_rel  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.614 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0032 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P vs Tanh          n=10 ratio(GM)=  0.607 wins=9/10 p_W=0.0039 p_W,Holm=0.0195 p_t,Holm=0.0046 p_W,all=0.2266
  Hantavirus  mean_rel  WIRE-P vs ReLU          n=10 ratio(GM)=  0.157 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P vs Sigmoid       n=10 ratio(GM)=  0.549 wins=9/10 p_W=0.0059 p_W,Holm=0.0195 p_t,Holm=0.0160 p_W,all=0.3105
  Hantavirus  mean_rel  WIRE-P vs SIREN         n=10 ratio(GM)=  0.244 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P vs Fourier       n=10 ratio(GM)=  0.378 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  peak_err  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.837 wins=5/10 p_W=0.9219 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  1.086 wins=5/10 p_W=0.8457 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.288 wins=6/10 p_W=0.1309 p_W,Holm=0.5273 p_t,Holm=0.3413 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.364 wins=8/10 p_W=0.0840 p_W,Holm=0.5039 p_t,Holm=0.2191 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.165 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0054 p_W,all=0.1758
  Hantavirus  peak_err  WIRE-P vs Tanh          n=10 ratio(GM)=  0.257 wins=9/10 p_W=0.0273 p_W,Holm=0.1914 p_t,Holm=0.2320 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P vs ReLU          n=10 ratio(GM)=  0.013 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0001 p_W,all=0.1758
  Hantavirus  peak_err  WIRE-P vs Sigmoid       n=10 ratio(GM)=  0.128 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0017 p_W,all=0.1758
  Hantavirus  peak_err  WIRE-P vs SIREN         n=10 ratio(GM)=  0.455 wins=7/10 p_W=0.1055 p_W,Holm=0.5273 p_t,Holm=0.4346 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P vs Fourier       n=10 ratio(GM)=  0.569 wins=5/10 p_W=0.6250 p_W,Holm=1.0000 p_t,Holm=0.7958 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.668 wins=7/10 p_W=0.1055 p_W,Holm=0.1055 p_t,Holm=0.1481 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  0.349 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0033 p_W,all=0.1758
  Hantavirus  phys_res  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.367 wins=8/10 p_W=0.0195 p_W,Holm=0.0410 p_t,Holm=0.0241 p_W,all=0.8203
  Hantavirus  phys_res  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.381 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0008 p_W,all=0.1758
  Hantavirus  phys_res  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.289 wins=9/10 p_W=0.0039 p_W,Holm=0.0195 p_t,Holm=0.0045 p_W,all=0.2266
  Hantavirus  phys_res  WIRE-P vs Tanh          n=10 ratio(GM)=  0.347 wins=9/10 p_W=0.0059 p_W,Holm=0.0234 p_t,Holm=0.0081 p_W,all=0.3105
  Hantavirus  phys_res  WIRE-P vs ReLU          n=10 ratio(GM)=  0.003 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  phys_res  WIRE-P vs Sigmoid       n=10 ratio(GM)=  0.276 wins=8/10 p_W=0.0137 p_W,Holm=0.0410 p_t,Holm=0.0241 p_W,all=0.6152
  Hantavirus  phys_res  WIRE-P vs SIREN         n=10 ratio(GM)=  0.012 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  phys_res  WIRE-P vs Fourier       n=10 ratio(GM)=  0.024 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.950 wins=5/10 p_W=0.8457 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  0.596 wins=9/10 p_W=0.0098 p_W,Holm=0.0684 p_t,Holm=0.0240 p_W,all=0.4785
  SARS-2003   mean_rel  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  1.029 wins=4/10 p_W=0.7695 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  1.063 wins=5/10 p_W=0.6250 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  1.044 wins=5/10 p_W=0.8457 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P vs Tanh          n=10 ratio(GM)=  1.150 wins=3/10 p_W=0.1602 p_W,Holm=0.8008 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P vs ReLU          n=10 ratio(GM)=  0.353 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0003 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P vs Sigmoid       n=10 ratio(GM)=  1.472 wins=2/10 p_W=0.0371 p_W,Holm=0.2227 p_t,Holm=0.1220 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P vs SIREN         n=10 ratio(GM)=  0.391 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0003 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P vs Fourier       n=10 ratio(GM)=  0.506 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0021 p_W,all=0.1758
  SARS-2003   peak_err  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  2.432 wins=2/10 p_W=0.0840 p_W,Holm=0.1934 p_t,Holm=0.3528 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  1.246 wins=5/10 p_W=0.7695 p_W,Holm=0.7695 p_t,Holm=0.5502 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.464 wins=8/10 p_W=0.0645 p_W,Holm=0.1934 p_t,Holm=0.3528 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.493 wins=8/10 p_W=0.0273 p_W,Holm=0.1367 p_t,Holm=0.3528 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.321 wins=9/10 p_W=0.0039 p_W,Holm=0.0391 p_t,Holm=0.0167 p_W,all=0.2266
  SARS-2003   peak_err  WIRE-P vs Tanh          n=10 ratio(GM)=  0.514 wins=9/10 p_W=0.0195 p_W,Holm=0.1172 p_t,Holm=0.3528 p_W,all=0.8203
  SARS-2003   peak_err  WIRE-P vs ReLU          n=10 ratio(GM)=  0.236 wins=9/10 p_W=0.0039 p_W,Holm=0.0391 p_t,Holm=0.0991 p_W,all=0.2266
  SARS-2003   peak_err  WIRE-P vs Sigmoid       n=10 ratio(GM)=  0.488 wins=8/10 p_W=0.0273 p_W,Holm=0.1367 p_t,Holm=0.3528 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P vs SIREN         n=10 ratio(GM)=  3.019 wins=2/10 p_W=0.0137 p_W,Holm=0.0957 p_t,Holm=0.0355 p_W,all=0.6152
  SARS-2003   peak_err  WIRE-P vs Fourier       n=10 ratio(GM)=  2.752 wins=2/10 p_W=0.0098 p_W,Holm=0.0781 p_t,Holm=0.0991 p_W,all=0.4785
  SARS-2003   phys_res  WIRE-P vs WIRE-P-A      n=10 ratio(GM)=  0.864 wins=6/10 p_W=0.6250 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P vs WIRE-P(phi=0) n=10 ratio(GM)=  0.284 wins=9/10 p_W=0.0059 p_W,Holm=0.0410 p_t,Holm=0.0122 p_W,all=0.3105
  SARS-2003   phys_res  WIRE-P vs MV-Morlet     n=10 ratio(GM)=  0.724 wins=6/10 p_W=0.3223 p_W,Holm=1.0000 p_t,Holm=0.8664 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P vs MV-Morlet-A   n=10 ratio(GM)=  0.678 wins=7/10 p_W=0.0840 p_W,Holm=0.4199 p_t,Holm=0.2505 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P vs MV-Morlet+    n=10 ratio(GM)=  0.889 wins=6/10 p_W=0.7695 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P vs Tanh          n=10 ratio(GM)=  0.587 wins=9/10 p_W=0.0371 p_W,Holm=0.2227 p_t,Holm=0.4497 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P vs ReLU          n=10 ratio(GM)=  0.015 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  SARS-2003   phys_res  WIRE-P vs Sigmoid       n=10 ratio(GM)=  1.132 wins=4/10 p_W=0.8457 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P vs SIREN         n=10 ratio(GM)=  0.068 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  SARS-2003   phys_res  WIRE-P vs Fourier       n=10 ratio(GM)=  0.103 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758

## E1_main: WIRE-P-A vs others  (paired over seeds; Holm over 3x3x10 tests)
  COVID-19    mean_rel  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.190 wins=2/10 p_W=0.1602 p_W,Holm=0.6406 p_t,Holm=0.2398 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  0.529 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    mean_rel  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.869 wins=6/10 p_W=0.1934 p_W,Holm=0.6406 p_t,Holm=0.3927 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.687 wins=9/10 p_W=0.0039 p_W,Holm=0.0234 p_t,Holm=0.0167 p_W,all=0.2344
  COVID-19    mean_rel  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  0.831 wins=8/10 p_W=0.0645 p_W,Holm=0.3223 p_t,Holm=0.1912 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.714 wins=6/10 p_W=0.2324 p_W,Holm=0.6406 p_t,Holm=0.3927 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.194 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    mean_rel  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  0.868 wins=7/10 p_W=0.4922 p_W,Holm=0.6406 p_t,Holm=0.4418 p_W,all=1.0000
  COVID-19    mean_rel  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.377 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    mean_rel  WIRE-P-A vs Fourier       n=10 ratio(GM)=  0.357 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    peak_err  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.430 wins=3/10 p_W=0.8457 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  1.591 wins=6/10 p_W=0.5566 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.816 wins=6/10 p_W=0.2754 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.536 wins=9/10 p_W=0.0195 p_W,Holm=0.1758 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  0.613 wins=7/10 p_W=0.0645 p_W,Holm=0.4512 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.731 wins=6/10 p_W=0.1055 p_W,Holm=0.5273 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.118 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0016 p_W,all=0.1758
  COVID-19    peak_err  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  0.433 wins=9/10 p_W=0.0273 p_W,Holm=0.2188 p_t,Holm=0.5750 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.910 wins=4/10 p_W=1.0000 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  COVID-19    peak_err  WIRE-P-A vs Fourier       n=10 ratio(GM)=  2.873 wins=2/10 p_W=0.0840 p_W,Holm=0.5039 p_t,Holm=0.5750 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.483 wins=2/10 p_W=0.1055 p_W,Holm=0.1934 p_t,Holm=0.1099 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  0.320 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0001 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.652 wins=7/10 p_W=0.0645 p_W,Holm=0.1934 p_t,Holm=0.1099 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.359 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0013 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  0.601 wins=6/10 p_W=0.0840 p_W,Holm=0.1934 p_t,Holm=0.0976 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.651 wins=8/10 p_W=0.0371 p_W,Holm=0.1484 p_t,Holm=0.1099 p_W,all=1.0000
  COVID-19    phys_res  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.014 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  0.493 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0316 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.104 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  COVID-19    phys_res  WIRE-P-A vs Fourier       n=10 ratio(GM)=  0.114 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.141 wins=3/10 p_W=0.3223 p_W,Holm=0.3223 p_t,Holm=0.1998 p_W,all=1.0000
  Hantavirus  mean_rel  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  0.730 wins=9/10 p_W=0.0098 p_W,Holm=0.0684 p_t,Holm=0.0192 p_W,all=0.5566
  Hantavirus  mean_rel  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.781 wins=7/10 p_W=0.1309 p_W,Holm=0.2617 p_t,Holm=0.1998 p_W,all=1.0000
  Hantavirus  mean_rel  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.844 wins=8/10 p_W=0.0488 p_W,Holm=0.1465 p_t,Holm=0.1414 p_W,all=1.0000
  Hantavirus  mean_rel  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  0.700 wins=8/10 p_W=0.0195 p_W,Holm=0.0977 p_t,Holm=0.0856 p_W,all=1.0000
  Hantavirus  mean_rel  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.692 wins=8/10 p_W=0.0098 p_W,Holm=0.0684 p_t,Holm=0.0125 p_W,all=0.5566
  Hantavirus  mean_rel  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.179 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  0.627 wins=8/10 p_W=0.0273 p_W,Holm=0.1094 p_t,Holm=0.1414 p_W,all=1.0000
  Hantavirus  mean_rel  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.278 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  mean_rel  WIRE-P-A vs Fourier       n=10 ratio(GM)=  0.431 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0001 p_W,all=0.1758
  Hantavirus  peak_err  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.195 wins=5/10 p_W=0.9219 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  1.298 wins=3/10 p_W=0.7695 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.344 wins=7/10 p_W=0.0840 p_W,Holm=0.5039 p_t,Holm=0.6391 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.435 wins=7/10 p_W=0.3750 p_W,Holm=1.0000 p_t,Holm=0.4870 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  0.197 wins=8/10 p_W=0.0195 p_W,Holm=0.1367 p_t,Holm=0.1510 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.306 wins=9/10 p_W=0.0137 p_W,Holm=0.1094 p_t,Holm=0.4252 p_W,all=0.7246
  Hantavirus  peak_err  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.016 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  peak_err  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  0.153 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0444 p_W,all=0.1758
  Hantavirus  peak_err  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.543 wins=6/10 p_W=0.3223 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  Hantavirus  peak_err  WIRE-P-A vs Fourier       n=10 ratio(GM)=  0.680 wins=6/10 p_W=0.4922 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.498 wins=3/10 p_W=0.1055 p_W,Holm=0.2578 p_t,Holm=0.2641 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  0.522 wins=8/10 p_W=0.0645 p_W,Holm=0.2578 p_t,Holm=0.1927 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.549 wins=8/10 p_W=0.0840 p_W,Holm=0.2578 p_t,Holm=0.2641 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.571 wins=8/10 p_W=0.0645 p_W,Holm=0.2578 p_t,Holm=0.2641 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  0.432 wins=7/10 p_W=0.0273 p_W,Holm=0.1641 p_t,Holm=0.1504 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.519 wins=9/10 p_W=0.0098 p_W,Holm=0.0684 p_t,Holm=0.0489 p_W,all=0.5566
  Hantavirus  phys_res  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.005 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  phys_res  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  0.413 wins=8/10 p_W=0.0371 p_W,Holm=0.1855 p_t,Holm=0.2641 p_W,all=1.0000
  Hantavirus  phys_res  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.017 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  Hantavirus  phys_res  WIRE-P-A vs Fourier       n=10 ratio(GM)=  0.035 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.052 wins=5/10 p_W=0.8457 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  0.627 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0269 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  1.083 wins=2/10 p_W=0.2754 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  1.118 wins=4/10 p_W=0.6250 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  1.098 wins=6/10 p_W=1.0000 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P-A vs Tanh          n=10 ratio(GM)=  1.210 wins=4/10 p_W=0.1934 p_W,Holm=0.9668 p_t,Holm=0.6728 p_W,all=1.0000
  SARS-2003   mean_rel  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.371 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0001 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  1.549 wins=0/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0143 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.411 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0003 p_W,all=0.1758
  SARS-2003   mean_rel  WIRE-P-A vs Fourier       n=10 ratio(GM)=  0.533 wins=9/10 p_W=0.0098 p_W,Holm=0.0586 p_t,Holm=0.0206 p_W,all=0.5566
  SARS-2003   peak_err  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  0.411 wins=8/10 p_W=0.0840 p_W,Holm=0.2578 p_t,Holm=0.2599 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  0.512 wins=8/10 p_W=0.0645 p_W,Holm=0.2578 p_t,Holm=0.1645 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.191 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0012 p_W,all=0.1758
  SARS-2003   peak_err  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.203 wins=9/10 p_W=0.0059 p_W,Holm=0.0352 p_t,Holm=0.0374 p_W,all=0.3398
  SARS-2003   peak_err  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  0.132 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0014 p_W,all=0.1758
  SARS-2003   peak_err  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.211 wins=8/10 p_W=0.0195 p_W,Holm=0.0977 p_t,Holm=0.0725 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.097 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0100 p_W,all=0.1758
  SARS-2003   peak_err  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  0.201 wins=9/10 p_W=0.0039 p_W,Holm=0.0273 p_t,Holm=0.0117 p_W,all=0.2344
  SARS-2003   peak_err  WIRE-P-A vs SIREN         n=10 ratio(GM)=  1.241 wins=4/10 p_W=0.6953 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   peak_err  WIRE-P-A vs Fourier       n=10 ratio(GM)=  1.132 wins=5/10 p_W=1.0000 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P-A vs WIRE-P        n=10 ratio(GM)=  1.157 wins=4/10 p_W=0.6250 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P-A vs WIRE-P(phi=0) n=10 ratio(GM)=  0.328 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0148 p_W,all=0.1758
  SARS-2003   phys_res  WIRE-P-A vs MV-Morlet     n=10 ratio(GM)=  0.837 wins=7/10 p_W=0.2324 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P-A vs MV-Morlet-A   n=10 ratio(GM)=  0.784 wins=6/10 p_W=0.4316 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P-A vs MV-Morlet+    n=10 ratio(GM)=  1.028 wins=6/10 p_W=0.9219 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P-A vs Tanh          n=10 ratio(GM)=  0.679 wins=8/10 p_W=0.1055 p_W,Holm=0.6328 p_t,Holm=0.8290 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P-A vs ReLU          n=10 ratio(GM)=  0.017 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  SARS-2003   phys_res  WIRE-P-A vs Sigmoid       n=10 ratio(GM)=  1.309 wins=5/10 p_W=0.6250 p_W,Holm=1.0000 p_t,Holm=1.0000 p_W,all=1.0000
  SARS-2003   phys_res  WIRE-P-A vs SIREN         n=10 ratio(GM)=  0.079 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758
  SARS-2003   phys_res  WIRE-P-A vs Fourier       n=10 ratio(GM)=  0.119 wins=10/10 p_W=0.0020 p_W,Holm=0.0195 p_t,Holm=0.0000 p_W,all=0.1758

## E1_main: MV-Morlet vs others  (paired over seeds; Holm over 3x3x1 tests)
  COVID-19    mean_rel  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  0.790 wins=7/10 p_W=0.0840 p_W,Holm=0.0840 p_t,Holm=0.0587 p_W,all=0.6719
  COVID-19    peak_err  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  0.656 wins=7/10 p_W=0.2324 p_W,Holm=0.2324 p_t,Holm=0.6526 p_W,all=1.0000
  COVID-19    phys_res  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  0.551 wins=8/10 p_W=0.0371 p_W,Holm=0.0371 p_t,Holm=0.0059 p_W,all=0.3340
  Hantavirus  mean_rel  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  1.081 wins=4/10 p_W=0.6250 p_W,Holm=0.6250 p_t,Holm=0.5828 p_W,all=1.0000
  Hantavirus  peak_err  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  1.265 wins=4/10 p_W=0.3750 p_W,Holm=0.3750 p_t,Holm=0.5838 p_W,all=1.0000
  Hantavirus  phys_res  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  1.040 wins=4/10 p_W=0.6953 p_W,Holm=0.6953 p_t,Holm=0.9104 p_W,all=1.0000
  SARS-2003   mean_rel  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  1.033 wins=6/10 p_W=0.9219 p_W,Holm=0.9219 p_t,Holm=0.8438 p_W,all=1.0000
  SARS-2003   peak_err  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  1.062 wins=6/10 p_W=1.0000 p_W,Holm=1.0000 p_t,Holm=0.8727 p_W,all=1.0000
  SARS-2003   phys_res  MV-Morlet vs MV-Morlet-A   n=10 ratio(GM)=  0.937 wins=6/10 p_W=1.0000 p_W,Holm=1.0000 p_t,Holm=0.8229 p_W,all=1.0000

## E5 real data (1978 boarding-school influenza; days 1-10 train, 11-14 forecast)
  classical least-squares SEIR fit: beta=5.856 sigma=0.630 gamma=0.437 R0=13.38 RMSE train=11.85 test=28.60
  WIRE-P        n=10 RMSE train=11.56±0.85 forecast=28.56±1.52 beta=5.769 sigma=26.097 gamma=0.437 R0=13.19±3.27 pinn-vs-ODE=4.28e-02
  WIRE-P-A      n=10 RMSE train=11.28±0.01 forecast=29.07±0.02 beta=6.233 sigma=0.616 gamma=0.437 R0=14.25±0.01 pinn-vs-ODE=4.42e-02
  WIRE-P(phi=0) n=10 RMSE train=18.20±1.42 forecast=14.13±1.77 beta=2.969 sigma=1.798 gamma=0.462 R0=6.43±1.40 pinn-vs-ODE=9.20e-02
  MV-Morlet     n=10 RMSE train=14.05±0.05 forecast=24.18±0.21 beta=1.686 sigma=165.267 gamma=0.433 R0=3.90±0.01 pinn-vs-ODE=3.04e-02
  MV-Morlet-A   n=10 RMSE train=13.97±0.02 forecast=24.47±0.12 beta=1.676 sigma=996.108 gamma=0.432 R0=3.88±0.00 pinn-vs-ODE=3.49e-02
  MV-Morlet+    n=10 RMSE train=14.08±0.06 forecast=24.11±0.20 beta=1.689 sigma=126.898 gamma=0.433 R0=3.90±0.01 pinn-vs-ODE=2.84e-02
  Tanh          n=10 RMSE train=13.96±0.01 forecast=24.54±0.17 beta=1.674 sigma=3174.238 gamma=0.432 R0=3.88±0.01 pinn-vs-ODE=3.34e-02
  ReLU          n=10 RMSE train=53.11±30.28 forecast=61.55±50.89 beta=2.148 sigma=2.487 gamma=0.414 R0=5.15±0.68 pinn-vs-ODE=2.11e-01
  Sigmoid       n=10 RMSE train=113.67±0.14 forecast=445.83±0.31 beta=0.404 sigma=8294471443556158264049664.000 gamma=0.000 R0=1424934161311.17±4504881807737.92 pinn-vs-ODE=8.74e+02
  SIREN         n=10 RMSE train=14.70±2.39 forecast=18.40±3.84 beta=4.463 sigma=0.965 gamma=0.456 R0=9.82±2.06 pinn-vs-ODE=3.09e-02
  Fourier       n=10 RMSE train=11.31±0.03 forecast=29.05±0.08 beta=6.216 sigma=0.617 gamma=0.438 R0=14.21±0.06 pinn-vs-ODE=4.23e-02
  WIRE-P vs WIRE-P-A      rmse_train: ratio=1.023 wins=2/10 p_W=0.0371 p_W,Holm=0.0742
  WIRE-P vs WIRE-P(phi=0) rmse_train: ratio=0.636 wins=10/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs MV-Morlet     rmse_train: ratio=0.821 wins=10/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs MV-Morlet-A   rmse_train: ratio=0.826 wins=9/10 p_W=0.0039 p_W,Holm=0.0195
  WIRE-P vs MV-Morlet+    rmse_train: ratio=0.820 wins=10/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs Tanh          rmse_train: ratio=0.826 wins=9/10 p_W=0.0039 p_W,Holm=0.0195
  WIRE-P vs ReLU          rmse_train: ratio=0.259 wins=10/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs Sigmoid       rmse_train: ratio=0.102 wins=10/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs SIREN         rmse_train: ratio=0.794 wins=10/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs Fourier       rmse_train: ratio=1.021 wins=5/10 p_W=0.7695 p_W,Holm=0.7695
  WIRE-P vs WIRE-P-A      rmse_test: ratio=0.981 wins=9/10 p_W=0.0098 p_W,Holm=0.0293
  WIRE-P vs WIRE-P(phi=0) rmse_test: ratio=2.031 wins=0/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs MV-Morlet     rmse_test: ratio=1.179 wins=0/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs MV-Morlet-A   rmse_test: ratio=1.166 wins=1/10 p_W=0.0039 p_W,Holm=0.0195
  WIRE-P vs MV-Morlet+    rmse_test: ratio=1.183 wins=0/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs Tanh          rmse_test: ratio=1.162 wins=1/10 p_W=0.0039 p_W,Holm=0.0195
  WIRE-P vs ReLU          rmse_test: ratio=0.644 wins=7/10 p_W=0.2324 p_W,Holm=0.4648
  WIRE-P vs Sigmoid       rmse_test: ratio=0.064 wins=10/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs SIREN         rmse_test: ratio=1.582 wins=0/10 p_W=0.0020 p_W,Holm=0.0195
  WIRE-P vs Fourier       rmse_test: ratio=0.982 wins=7/10 p_W=0.2324 p_W,Holm=0.4648

## E4 inverse problem: I(t) observed every 2 days with noise; beta, gamma learned (init 0.2, 0.1)
  failure = beta error > 50% (rates collapse towards the trivial solution beta, gamma -> 0)
  Hantavirus  noise=0.00 WIRE-P     median R0_err=    10.46% beta_err=   3.63% relL2=6.268e-02 failed=0/10
  Hantavirus  noise=0.00 WIRE-P-A   median R0_err=    11.11% beta_err=   3.18% relL2=6.727e-02 failed=0/10
  Hantavirus  noise=0.00 MV-Morlet  median R0_err=     6.88% beta_err=   2.82% relL2=4.398e-02 failed=3/10
  Hantavirus  noise=0.00 Tanh       median R0_err=    36.08% beta_err=  51.26% relL2=3.363e-01 failed=5/10
  Hantavirus  noise=0.00 Sigmoid    median R0_err=     6.26% beta_err=   3.06% relL2=3.289e-02 failed=4/10
  Hantavirus  noise=0.05 WIRE-P     median R0_err=    16.67% beta_err=   3.74% relL2=1.036e-01 failed=0/10
  Hantavirus  noise=0.05 WIRE-P-A   median R0_err=    14.02% beta_err=   3.57% relL2=8.941e-02 failed=0/10
  Hantavirus  noise=0.05 MV-Morlet  median R0_err=     7.93% beta_err=   4.89% relL2=4.853e-02 failed=3/10
  Hantavirus  noise=0.05 Tanh       median R0_err=    40.86% beta_err=  52.05% relL2=3.230e-01 failed=5/10
  Hantavirus  noise=0.05 Sigmoid    median R0_err=     4.83% beta_err=   3.68% relL2=3.232e-02 failed=4/10
  Hantavirus  noise=0.10 WIRE-P     median R0_err=   191.06% beta_err=  31.42% relL2=4.867e-01 failed=3/10
  Hantavirus  noise=0.10 WIRE-P-A   median R0_err=   239.34% beta_err=  43.11% relL2=5.443e-01 failed=5/10
  Hantavirus  noise=0.10 MV-Morlet  median R0_err=    67.53% beta_err=  39.99% relL2=5.287e-01 failed=4/10
  Hantavirus  noise=0.10 Tanh       median R0_err=   100.00% beta_err=  99.95% relL2=6.259e-01 failed=6/10
  Hantavirus  noise=0.10 Sigmoid    median R0_err=    99.25% beta_err=  87.10% relL2=6.174e-01 failed=6/10
  SARS-2003   noise=0.00 WIRE-P     median R0_err=     4.83% beta_err=   1.84% relL2=1.954e-02 failed=0/10
  SARS-2003   noise=0.00 WIRE-P-A   median R0_err=     4.44% beta_err=   1.73% relL2=1.893e-02 failed=0/10
  SARS-2003   noise=0.00 MV-Morlet  median R0_err=    62.22% beta_err=  94.96% relL2=7.207e-01 failed=8/10
  SARS-2003   noise=0.00 Tanh       median R0_err=    38.56% beta_err= 100.00% relL2=7.406e-01 failed=7/10
  SARS-2003   noise=0.00 Sigmoid    median R0_err=  5435.52% beta_err=  99.91% relL2=7.099e-01 failed=10/10
  SARS-2003   noise=0.05 WIRE-P     median R0_err=     6.78% beta_err=   1.80% relL2=3.672e-02 failed=0/10
  SARS-2003   noise=0.05 WIRE-P-A   median R0_err=    10.10% beta_err=   3.18% relL2=4.922e-02 failed=0/10
  SARS-2003   noise=0.05 MV-Morlet  median R0_err=    65.91% beta_err=  96.41% relL2=7.263e-01 failed=9/10
  SARS-2003   noise=0.05 Tanh       median R0_err=    91.47% beta_err=  99.93% relL2=7.060e-01 failed=6/10
  SARS-2003   noise=0.05 Sigmoid    median R0_err=    99.66% beta_err= 100.00% relL2=7.161e-01 failed=10/10
  SARS-2003   noise=0.10 WIRE-P     median R0_err=    30.86% beta_err=  10.59% relL2=1.223e-01 failed=0/10
  SARS-2003   noise=0.10 WIRE-P-A   median R0_err=    31.83% beta_err=  12.85% relL2=1.199e-01 failed=1/10
  SARS-2003   noise=0.10 MV-Morlet  median R0_err=    64.60% beta_err=  95.13% relL2=7.240e-01 failed=9/10
  SARS-2003   noise=0.10 Tanh       median R0_err=   109.09% beta_err=  99.95% relL2=6.950e-01 failed=7/10
  SARS-2003   noise=0.10 Sigmoid    median R0_err=5161367.13% beta_err= 100.00% relL2=7.341e-01 failed=9/10
  COVID-19    noise=0.00 WIRE-P     median R0_err=     5.06% beta_err=   2.31% relL2=1.494e-02 failed=0/10
  COVID-19    noise=0.00 WIRE-P-A   median R0_err=     6.61% beta_err=   2.92% relL2=1.850e-02 failed=0/10
  COVID-19    noise=0.00 MV-Morlet  median R0_err=     5.23% beta_err=   2.20% relL2=1.590e-02 failed=4/10
  COVID-19    noise=0.00 Tanh       median R0_err=    49.23% beta_err= 100.00% relL2=8.079e-01 failed=6/10
  COVID-19    noise=0.00 Sigmoid    median R0_err=    52.01% beta_err=  52.29% relL2=2.764e-01 failed=5/10
  COVID-19    noise=0.05 WIRE-P     median R0_err=     5.29% beta_err=   2.08% relL2=2.555e-02 failed=0/10
  COVID-19    noise=0.05 WIRE-P-A   median R0_err=     6.40% beta_err=   2.10% relL2=3.048e-02 failed=0/10
  COVID-19    noise=0.05 MV-Morlet  median R0_err=    40.49% beta_err=  47.91% relL2=3.381e-01 failed=5/10
  COVID-19    noise=0.05 Tanh       median R0_err=    54.25% beta_err= 100.00% relL2=8.371e-01 failed=6/10
  COVID-19    noise=0.05 Sigmoid    median R0_err=    99.99% beta_err= 100.00% relL2=6.788e-01 failed=6/10
  COVID-19    noise=0.10 WIRE-P     median R0_err=     9.72% beta_err=   4.56% relL2=4.935e-02 failed=0/10
  COVID-19    noise=0.10 WIRE-P-A   median R0_err=    15.71% beta_err=   6.70% relL2=5.824e-02 failed=0/10
  COVID-19    noise=0.10 MV-Morlet  median R0_err=    78.72% beta_err=  96.55% relL2=8.587e-01 failed=6/10
  COVID-19    noise=0.10 Tanh       median R0_err=    87.77% beta_err=  99.18% relL2=5.550e-01 failed=6/10
  COVID-19    noise=0.10 Sigmoid    median R0_err=   100.00% beta_err= 100.00% relL2=5.764e-01 failed=6/10
  Hantavirus  noise=0.00 mean_rel WIRE-P vs WIRE-P-A   ratio=1.026 wins=5/10 p_W=0.9219 p_W,Holm=1.0000
  Hantavirus  noise=0.00 mean_rel WIRE-P vs MV-Morlet  ratio=0.713 wins=4/10 p_W=0.5566 p_W,Holm=1.0000
  Hantavirus  noise=0.00 mean_rel WIRE-P vs Tanh       ratio=0.583 wins=6/10 p_W=0.1934 p_W,Holm=0.7734
  Hantavirus  noise=0.00 mean_rel WIRE-P vs Sigmoid    ratio=1.109 wins=5/10 p_W=0.4922 p_W,Holm=1.0000
  Hantavirus  noise=0.00 R0_err   WIRE-P vs WIRE-P-A   ratio=1.068 wins=5/10 p_W=0.6953 p_W,Holm=1.0000
  Hantavirus  noise=0.00 R0_err   WIRE-P vs MV-Morlet  ratio=0.827 wins=4/10 p_W=0.5566 p_W,Holm=1.0000
  Hantavirus  noise=0.00 R0_err   WIRE-P vs Tanh       ratio=0.912 wins=6/10 p_W=0.1934 p_W,Holm=0.7734
  Hantavirus  noise=0.00 R0_err   WIRE-P vs Sigmoid    ratio=0.167 wins=5/10 p_W=0.4922 p_W,Holm=1.0000
  Hantavirus  noise=0.05 mean_rel WIRE-P vs WIRE-P-A   ratio=1.246 wins=2/10 p_W=0.0840 p_W,Holm=0.3359
  Hantavirus  noise=0.05 mean_rel WIRE-P vs MV-Morlet  ratio=1.311 wins=4/10 p_W=0.5566 p_W,Holm=1.0000
  Hantavirus  noise=0.05 mean_rel WIRE-P vs Tanh       ratio=0.907 wins=5/10 p_W=0.2324 p_W,Holm=0.6973
  Hantavirus  noise=0.05 mean_rel WIRE-P vs Sigmoid    ratio=1.552 wins=4/10 p_W=0.5566 p_W,Holm=1.0000
  Hantavirus  noise=0.05 R0_err   WIRE-P vs WIRE-P-A   ratio=1.467 wins=3/10 p_W=0.2754 p_W,Holm=0.9297
  Hantavirus  noise=0.05 R0_err   WIRE-P vs MV-Morlet  ratio=1.506 wins=4/10 p_W=0.7695 p_W,Holm=1.0000
  Hantavirus  noise=0.05 R0_err   WIRE-P vs Tanh       ratio=1.376 wins=5/10 p_W=0.2324 p_W,Holm=0.9297
  Hantavirus  noise=0.05 R0_err   WIRE-P vs Sigmoid    ratio=1.111 wins=4/10 p_W=0.5566 p_W,Holm=1.0000
  Hantavirus  noise=0.10 mean_rel WIRE-P vs WIRE-P-A   ratio=0.980 wins=6/10 p_W=0.6250 p_W,Holm=1.0000
  Hantavirus  noise=0.10 mean_rel WIRE-P vs MV-Morlet  ratio=1.593 wins=5/10 p_W=0.6250 p_W,Holm=1.0000
  Hantavirus  noise=0.10 mean_rel WIRE-P vs Tanh       ratio=0.993 wins=8/10 p_W=0.1602 p_W,Holm=0.6406
  Hantavirus  noise=0.10 mean_rel WIRE-P vs Sigmoid    ratio=1.781 wins=6/10 p_W=1.0000 p_W,Holm=1.0000
  Hantavirus  noise=0.10 R0_err   WIRE-P vs WIRE-P-A   ratio=0.986 wins=6/10 p_W=0.7695 p_W,Holm=1.0000
  Hantavirus  noise=0.10 R0_err   WIRE-P vs MV-Morlet  ratio=2.158 wins=3/10 p_W=0.4316 p_W,Holm=1.0000
  Hantavirus  noise=0.10 R0_err   WIRE-P vs Tanh       ratio=0.728 wins=5/10 p_W=0.4922 p_W,Holm=1.0000
  Hantavirus  noise=0.10 R0_err   WIRE-P vs Sigmoid    ratio=0.504 wins=4/10 p_W=0.9219 p_W,Holm=1.0000
  SARS-2003   noise=0.00 mean_rel WIRE-P vs WIRE-P-A   ratio=0.990 wins=5/10 p_W=0.8457 p_W,Holm=0.8457
  SARS-2003   noise=0.00 mean_rel WIRE-P vs MV-Morlet  ratio=0.061 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  SARS-2003   noise=0.00 mean_rel WIRE-P vs Tanh       ratio=0.082 wins=8/10 p_W=0.0098 p_W,Holm=0.0195
  SARS-2003   noise=0.00 mean_rel WIRE-P vs Sigmoid    ratio=0.029 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  SARS-2003   noise=0.00 R0_err   WIRE-P vs WIRE-P-A   ratio=1.030 wins=5/10 p_W=0.9219 p_W,Holm=0.9219
  SARS-2003   noise=0.00 R0_err   WIRE-P vs MV-Morlet  ratio=0.061 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  SARS-2003   noise=0.00 R0_err   WIRE-P vs Tanh       ratio=0.167 wins=7/10 p_W=0.0273 p_W,Holm=0.0547
  SARS-2003   noise=0.00 R0_err   WIRE-P vs Sigmoid    ratio=0.000 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  SARS-2003   noise=0.05 mean_rel WIRE-P vs WIRE-P-A   ratio=0.837 wins=7/10 p_W=0.2324 p_W,Holm=0.2324
  SARS-2003   noise=0.05 mean_rel WIRE-P vs MV-Morlet  ratio=0.076 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  SARS-2003   noise=0.05 mean_rel WIRE-P vs Tanh       ratio=0.138 wins=9/10 p_W=0.0059 p_W,Holm=0.0117
  SARS-2003   noise=0.05 mean_rel WIRE-P vs Sigmoid    ratio=0.058 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  SARS-2003   noise=0.05 R0_err   WIRE-P vs WIRE-P-A   ratio=0.680 wins=7/10 p_W=0.1602 p_W,Holm=0.1602
  SARS-2003   noise=0.05 R0_err   WIRE-P vs MV-Morlet  ratio=0.032 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  SARS-2003   noise=0.05 R0_err   WIRE-P vs Tanh       ratio=0.057 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  SARS-2003   noise=0.05 R0_err   WIRE-P vs Sigmoid    ratio=0.000 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  SARS-2003   noise=0.10 mean_rel WIRE-P vs WIRE-P-A   ratio=0.852 wins=6/10 p_W=0.3750 p_W,Holm=0.3750
  SARS-2003   noise=0.10 mean_rel WIRE-P vs MV-Morlet  ratio=0.208 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  SARS-2003   noise=0.10 mean_rel WIRE-P vs Tanh       ratio=0.305 wins=8/10 p_W=0.0098 p_W,Holm=0.0195
  SARS-2003   noise=0.10 mean_rel WIRE-P vs Sigmoid    ratio=0.200 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  SARS-2003   noise=0.10 R0_err   WIRE-P vs WIRE-P-A   ratio=1.280 wins=5/10 p_W=0.9219 p_W,Holm=0.9219
  SARS-2003   noise=0.10 R0_err   WIRE-P vs MV-Morlet  ratio=0.149 wins=9/10 p_W=0.0039 p_W,Holm=0.0156
  SARS-2003   noise=0.10 R0_err   WIRE-P vs Tanh       ratio=0.218 wins=6/10 p_W=0.0840 p_W,Holm=0.1680
  SARS-2003   noise=0.10 R0_err   WIRE-P vs Sigmoid    ratio=0.000 wins=7/10 p_W=0.0273 p_W,Holm=0.0820
  COVID-19    noise=0.00 mean_rel WIRE-P vs WIRE-P-A   ratio=0.892 wins=7/10 p_W=0.4316 p_W,Holm=0.7500
  COVID-19    noise=0.00 mean_rel WIRE-P vs MV-Morlet  ratio=0.255 wins=6/10 p_W=0.3750 p_W,Holm=0.7500
  COVID-19    noise=0.00 mean_rel WIRE-P vs Tanh       ratio=0.092 wins=8/10 p_W=0.0371 p_W,Holm=0.1484
  COVID-19    noise=0.00 mean_rel WIRE-P vs Sigmoid    ratio=0.174 wins=6/10 p_W=0.1602 p_W,Holm=0.4805
  COVID-19    noise=0.00 R0_err   WIRE-P vs WIRE-P-A   ratio=0.862 wins=8/10 p_W=0.3223 p_W,Holm=0.6445
  COVID-19    noise=0.00 R0_err   WIRE-P vs MV-Morlet  ratio=0.592 wins=6/10 p_W=0.3750 p_W,Holm=0.6445
  COVID-19    noise=0.00 R0_err   WIRE-P vs Tanh       ratio=0.041 wins=7/10 p_W=0.0488 p_W,Holm=0.1953
  COVID-19    noise=0.00 R0_err   WIRE-P vs Sigmoid    ratio=0.332 wins=7/10 p_W=0.1309 p_W,Holm=0.3926
  COVID-19    noise=0.05 mean_rel WIRE-P vs WIRE-P-A   ratio=0.895 wins=6/10 p_W=0.2324 p_W,Holm=0.2324
  COVID-19    noise=0.05 mean_rel WIRE-P vs MV-Morlet  ratio=0.195 wins=8/10 p_W=0.0371 p_W,Holm=0.0742
  COVID-19    noise=0.05 mean_rel WIRE-P vs Tanh       ratio=0.105 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  COVID-19    noise=0.05 mean_rel WIRE-P vs Sigmoid    ratio=0.131 wins=8/10 p_W=0.0137 p_W,Holm=0.0410
  COVID-19    noise=0.05 R0_err   WIRE-P vs WIRE-P-A   ratio=0.568 wins=7/10 p_W=0.1602 p_W,Holm=0.1602
  COVID-19    noise=0.05 R0_err   WIRE-P vs MV-Morlet  ratio=0.234 wins=7/10 p_W=0.0488 p_W,Holm=0.0977
  COVID-19    noise=0.05 R0_err   WIRE-P vs Tanh       ratio=0.026 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  COVID-19    noise=0.05 R0_err   WIRE-P vs Sigmoid    ratio=0.001 wins=9/10 p_W=0.0098 p_W,Holm=0.0293
  COVID-19    noise=0.10 mean_rel WIRE-P vs WIRE-P-A   ratio=0.896 wins=7/10 p_W=0.0645 p_W,Holm=0.0645
  COVID-19    noise=0.10 mean_rel WIRE-P vs MV-Morlet  ratio=0.143 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  COVID-19    noise=0.10 mean_rel WIRE-P vs Tanh       ratio=0.147 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  COVID-19    noise=0.10 mean_rel WIRE-P vs Sigmoid    ratio=0.153 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  COVID-19    noise=0.10 R0_err   WIRE-P vs WIRE-P-A   ratio=0.622 wins=8/10 p_W=0.0840 p_W,Holm=0.0840
  COVID-19    noise=0.10 R0_err   WIRE-P vs MV-Morlet  ratio=0.166 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  COVID-19    noise=0.10 R0_err   WIRE-P vs Tanh       ratio=0.007 wins=10/10 p_W=0.0020 p_W,Holm=0.0078
  COVID-19    noise=0.10 R0_err   WIRE-P vs Sigmoid    ratio=0.000 wins=9/10 p_W=0.0039 p_W,Holm=0.0078

## E2 noisy anchors (forward problem)
  Hantavirus  noise=0.02 WIRE-P=1.366e-02±1.6e-03(n=10) | WIRE-P-A=1.364e-02±1.7e-03(n=10) | MV-Morlet=1.334e-02±1.6e-03(n=10) | Tanh=1.319e-02±1.8e-03(n=10)
  Hantavirus  noise=0.05 WIRE-P=3.228e-02±4.3e-03(n=10) | WIRE-P-A=3.252e-02±4.3e-03(n=10) | MV-Morlet=3.394e-02±4.3e-03(n=10) | Tanh=3.276e-02±5.1e-03(n=10)
  SARS-2003   noise=0.02 WIRE-P=1.227e-02±2.3e-03(n=10) | WIRE-P-A=1.235e-02±2.5e-03(n=10) | MV-Morlet=1.146e-02±4.1e-03(n=10) | Tanh=1.299e-02±3.2e-03(n=10)
  SARS-2003   noise=0.05 WIRE-P=2.886e-02±6.2e-03(n=10) | WIRE-P-A=2.946e-02±6.3e-03(n=10) | MV-Morlet=3.094e-02±6.6e-03(n=10) | Tanh=3.051e-02±6.3e-03(n=10)
  COVID-19    noise=0.02 WIRE-P=1.264e-02±3.1e-03(n=10) | WIRE-P-A=1.258e-02±3.0e-03(n=10) | MV-Morlet=1.215e-02±3.4e-03(n=10) | Tanh=1.299e-02±2.6e-03(n=10)
  COVID-19    noise=0.05 WIRE-P=2.797e-02±7.0e-03(n=10) | WIRE-P-A=2.876e-02±6.6e-03(n=10) | MV-Morlet=2.837e-02±7.2e-03(n=10) | Tanh=2.773e-02±6.3e-03(n=10)
  Hantavirus  noise=0.02 WIRE-P vs WIRE-P-A   ratio=1.002 wins=6/10 p_W=0.8457 p_W,Holm=0.8457
  Hantavirus  noise=0.02 WIRE-P vs MV-Morlet  ratio=1.025 wins=3/10 p_W=0.1055 p_W,Holm=0.2109
  Hantavirus  noise=0.02 WIRE-P vs Tanh       ratio=1.038 wins=3/10 p_W=0.0371 p_W,Holm=0.1113
  Hantavirus  noise=0.05 WIRE-P vs WIRE-P-A   ratio=0.993 wins=8/10 p_W=0.0195 p_W,Holm=0.0391
  Hantavirus  noise=0.05 WIRE-P vs MV-Morlet  ratio=0.950 wins=9/10 p_W=0.0039 p_W,Holm=0.0117
  Hantavirus  noise=0.05 WIRE-P vs Tanh       ratio=0.988 wins=8/10 p_W=0.1602 p_W,Holm=0.1602
  SARS-2003   noise=0.02 WIRE-P vs WIRE-P-A   ratio=0.997 wins=6/10 p_W=0.6953 p_W,Holm=0.8633
  SARS-2003   noise=0.02 WIRE-P vs MV-Morlet  ratio=1.108 wins=4/10 p_W=0.4316 p_W,Holm=0.8633
  SARS-2003   noise=0.02 WIRE-P vs Tanh       ratio=0.955 wins=7/10 p_W=0.2754 p_W,Holm=0.8262
  SARS-2003   noise=0.05 WIRE-P vs WIRE-P-A   ratio=0.980 wins=8/10 p_W=0.0371 p_W,Holm=0.0371
  SARS-2003   noise=0.05 WIRE-P vs MV-Morlet  ratio=0.933 wins=10/10 p_W=0.0020 p_W,Holm=0.0059
  SARS-2003   noise=0.05 WIRE-P vs Tanh       ratio=0.944 wins=8/10 p_W=0.0137 p_W,Holm=0.0273
  COVID-19    noise=0.02 WIRE-P vs WIRE-P-A   ratio=1.002 wins=5/10 p_W=0.7695 p_W,Holm=1.0000
  COVID-19    noise=0.02 WIRE-P vs MV-Morlet  ratio=1.050 wins=2/10 p_W=0.1055 p_W,Holm=0.3164
  COVID-19    noise=0.02 WIRE-P vs Tanh       ratio=0.967 wins=5/10 p_W=0.5566 p_W,Holm=1.0000
  COVID-19    noise=0.05 WIRE-P vs WIRE-P-A   ratio=0.968 wins=7/10 p_W=0.2754 p_W,Holm=0.8262
  COVID-19    noise=0.05 WIRE-P vs MV-Morlet  ratio=0.986 wins=4/10 p_W=0.9219 p_W,Holm=1.0000
  COVID-19    noise=0.05 WIRE-P vs Tanh       ratio=1.005 wins=6/10 p_W=0.9219 p_W,Holm=1.0000

## E3 smaller network 3x32
  Hantavirus  noise=0.00 WIRE-P=6.666e-04±1.5e-04(n=10) | WIRE-P-A=6.960e-04±9.6e-05(n=10) | MV-Morlet=6.884e-04±9.3e-05(n=10) | Tanh=9.079e-04±3.1e-04(n=10)
  SARS-2003   noise=0.00 WIRE-P=2.014e-03±5.2e-04(n=10) | WIRE-P-A=2.326e-03±6.7e-04(n=10) | MV-Morlet=2.212e-03±7.4e-04(n=10) | Tanh=1.665e-03±4.5e-04(n=10)
  COVID-19    noise=0.00 WIRE-P=2.579e-03±7.1e-04(n=10) | WIRE-P-A=2.782e-03±6.7e-04(n=10) | MV-Morlet=2.928e-03±1.0e-03(n=10) | Tanh=5.308e-03±2.2e-03(n=10)
  Hantavirus  noise=0.00 WIRE-P vs WIRE-P-A   ratio=0.944 wins=6/10 p_W=0.4922 p_W,Holm=0.9844
  Hantavirus  noise=0.00 WIRE-P vs MV-Morlet  ratio=0.954 wins=6/10 p_W=0.5566 p_W,Holm=0.9844
  Hantavirus  noise=0.00 WIRE-P vs Tanh       ratio=0.756 wins=7/10 p_W=0.1309 p_W,Holm=0.3926
  SARS-2003   noise=0.00 WIRE-P vs WIRE-P-A   ratio=0.870 wins=7/10 p_W=0.3750 p_W,Holm=0.7500
  SARS-2003   noise=0.00 WIRE-P vs MV-Morlet  ratio=0.930 wins=5/10 p_W=0.8457 p_W,Holm=0.8457
  SARS-2003   noise=0.00 WIRE-P vs Tanh       ratio=1.208 wins=3/10 p_W=0.1309 p_W,Holm=0.3926
  COVID-19    noise=0.00 WIRE-P vs WIRE-P-A   ratio=0.919 wins=6/10 p_W=0.3750 p_W,Holm=0.7500
  COVID-19    noise=0.00 WIRE-P vs MV-Morlet  ratio=0.899 wins=6/10 p_W=0.4316 p_W,Holm=0.7500
  COVID-19    noise=0.00 WIRE-P vs Tanh       ratio=0.523 wins=8/10 p_W=0.0137 p_W,Holm=0.0410