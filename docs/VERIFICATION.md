# Verification

Canonical parameters everywhere: H = 2 m, G = 4 Pa/m, mu = 1 Pa·s,
rho = 1 kg/m³, nu = 1 m²/s.

## Analytic reference (poiseuille)

u(y) = G/(2mu)·y(H−y); umax = 2; Q = 8/3; Umean = 4/3;
tau_wall = 4; Re = 8/3. Suites `poiseuille` (8 tests) and `props`
(Re, 9 tests) pin these against independently spelled formulas.

## Discrete solutions vs analysis

| grid (cells) | h | center | Q_trap | Q err | shear_lo | shear err | imbalance |
|---|---|---|---|---|---|---|---|
| 2 | 1 | 2 (exact) | 2 (exact) | 2/3 | 2 (exact) | 2 | 0 (exact) |
| 4 | 1/2 | 2 (±ulp) | 5/2 | 1/6 | 3 (±ulp) | 1 | 0 (±ulp) |
| 8 | 1/4 | 2 (±ulp) | 21/8 | 1/24 | 7/2 (±ulp) | 1/2 | 0 (±ulp) |

Suites `tridiag` (8), `model1d` (10): Thomas solutions within
1e-12 of analysis; 3-node path bit-exact.

## Grid refinement (measured, not assumed)

- Flow rate errors 2/3 → 1/6 → 1/24: ratios exactly 4 →
  **second order** (trapezoid), asserted with tol 1e-9.
- Wall-shear errors 2 → 1 → 1/2: ratios exactly 2 →
  **first order** (one-sided), asserted with tol 1e-9.
- Nodal velocities are exact to rounding on every grid (the
  second-order central scheme reproduces quadratics): the error
  story lives in the derived quantities, honestly reported.

## Conservation

Discrete identity (F_top − F_bottom) = G·span holds to rounding on
all three grids (`derived` 6 tests exact `==` on dyadic paths,
`model1d` approx 1e-12 post-Thomas). Tends to G·H = 2·tau as h→0.

## Solvers

- Thomas (direct): `ZeroPivot` structured on (1,1,1)-type triples
  and zero diagonals; agrees with Jacobi-128 to 1e-12
  (cross-solver, `jacobi`).
- Jacobi (iterative): sweep-1 exact from rest; residual strictly
  decreases 8→32→128 sweeps; 128-sweep residual ≤ 1e-12 and profile
  within 1e-12 of analysis; `residual_converged` rejects
  non-positive tolerances.
- Solver failure vs invalid model: `Singular` (pivot) vs
  `BadInput` (physics/grid) vs `Unstable` (stability) are distinct
  variants asserted separately.

## Transient

- Steps 1–2 from rest exact dyadic (`stencil1d` 12 tests).
- 32 steps at r = 1/4: t = 2.0 exact, center within 0.05 of 2,
  symmetry bitwise, walls pinned.
- r = 3/4 → structured `Unstable`; r = 0 → `BadInput`.
- Zero drive preserves zero (exact); quiescent default marked
  `Defaulted`.
- Fixed point: one FTCS step from the Thomas state reproduces it
  to 1e-12 (steady/transient formulation agreement).

## Degenerate / invalid coverage

Zero/negative density and viscosity, zero/negative height, zero
cells, out-of-range lanes, single-cell grid (valid, no interior),
zero pivots, unstable and non-positive r/dt, wrong-size grids per
model path, conflicting... (no conflicting-BC concept exists yet:
one law only — noted, not tested vacuously).

## Independent oracle

`tools/oracle_fluid.py`: 48 Fraction-exact checks (analytic,
exact discrete solves by independent Gaussian elimination, trap
values, shear values, refinement ratios, transient steps,
fixed point, clock) plus a double-literal validity check. No
shared code with the MNCS implementation. Runs inside
`scripts/run_tests.py`; verdict joins the evidence JSON.

## Totals

74 native `mncs test` declarations across 9 suites + 48 oracle
checks. Full run ≈ 3m45s wall (dominated by per-suite toolchain
invocations, not by the physics: the largest case is 9 nodes ×
128 sweeps). Evidence: `target/test-evidence-*.json`
(schema `mncs-fluid.test-evidence/1`, revision-bound).

## What is NOT claimed

Production CFD; 2D/3D; turbulence/compressibility/multiphase;
pressure-velocity coupling; generic solvers; cross-backend float
bitwise identity (single-backend determinism only: same inputs →
same outputs on the verified backend); performance beyond tiny
verification grids.
