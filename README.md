# mncs-fluid

<!-- MNCS:generated:begin -->
<!-- MNCS:generated:end -->

Machine-native computational fluid dynamics for MNCS.

`mncs-fluid` is the canonical home of **fluid-domain semantics and
fluid formulations** — state variables, properties, pressure
gradients, fluxes, fluid boundary/initial conditions, governing
equations, and fluid discretization terms — expressed natively in
`mncs-language` (Profile 0.18). There is exactly one canonical
implementation: no `fluid-v1/v2`, no `native-fluid`, no parallel
reference/production forks, no compatibility layers.

## Ownership boundary

| Concern | Owner | Fluid relationship |
|---|---|---|
| Scalar representation, `fabs`, `approx` discipline | `mncs-numerics` | Consumed; never duplicated |
| Generic matrices, solvers, sparse kernels, tensors | `mncs-math` | Not a dependency; generic-solver pressure recorded |
| Points/vectors/transforms | `mncs-geometry` | Not a dependency of the 1D slice; 2D+ will consume it |
| Finite-element topology/assembly | `mncs-fem` | Untouched; FVM semantics not forced into it |
| Structured data / serialization | `mncs-data` | No model storage in Fluid |
| Test declarations, assertions, runner policy | `mncs-test` | Consumed via `mncs test`; no private harness |
| Execution/admission/lifecycle | Forge/Fabric | Fluid schedules nothing |
| Persistence / provenance graphs | Store/Lineage | Fluid persists nothing |
| Variable-coefficient/sparse generic solving | **nobody yet (P-FLUID-SOLVER)** | Fluid solves only its own uniform system natively |
| Props, driving force, walls, ICs, fluxes, viscous operators, Poiseuille models, derived quantities, sim time, results | **`mncs-fluid`** | Canonical home |

## Current capability (foundation slice)

Steady + transient plane-Poiseuille flow (incompressible, laminar,
Newtonian, fully developed), fully native except language-provided
float ops:

- `src/fluid/props.mncs` — `FluidProps` validation, kinematic
  viscosity, Reynolds number.
- `src/fluid/grid1d.mncs` — channel lanes, uniform builder,
  wall/interior identity.
- `src/fluid/bc.mncs` — no-slip walls, driving gradient with sign
  convention, initial state with Specified/Derived/Defaulted
  provenance.
- `src/fluid/poiseuille.mncs` — analytic comparators
  (u/umax/Q/Umean/shear), independently spelled.
- `src/fluid/stencil1d.mncs` — second difference, oriented face
  flux, diffusion number, r ≤ 1/2 stability gate, FTCS step,
  8/32-step drivers, `SimClock` + dt/src construction.
- `src/fluid/tridiag.mncs` — native Thomas for the uniform
  viscous system (1/3/7 lanes) with structured `ZeroPivot`.
- `src/fluid/jacobi.mncs` — native Jacobi sweeps, 8/32/128
  drivers, max-abs residual, convergence predicate.
- `src/fluid/derived.mncs` — trapezoidal flow rate, one-sided
  wall shears, discrete conservation imbalance.
- `src/fluid/model1d.mncs` — end-to-end 3/5/9-node steady models
  + 32-step transient model with distinct
  `BadInput/Singular/Unstable` arms.

## Verification

74 native `mncs test` declarations across 9 suites
(`scripts/run_tests.py`), exact `==` on dyadic values with
explicit `approx` where rounding genuinely occurs, plus the
independent exact-rational oracle `tools/oracle_fluid.py`
(48 checks, Fraction-based, no shared code). Analytical agreement,
discrete conservation, measured refinement orders (flow rate 2nd,
shear 1st), symmetry, limiting cases, cross-solver agreement, and
degenerate-model rejection. See `docs/VERIFICATION.md` and
`evidence/fluid-capabilities.json`.

## Layout

- `src/fluid/` — the library (`.mncs` only, no host semantics)
- `tests/native/` — in-language contracts via `mncs test`
- `scripts/run_tests.py` — canonical runner (suites + oracle)
  with revision-bound JSON evidence
- `tools/oracle_fluid.py` — independent exact-arithmetic oracle
- `docs/ARCHITECTURE.md` — layers and milestone status
- `docs/FLUID_MODEL.md` — ownership boundary and RFC classification
- `docs/VERIFICATION.md` — analytic/reference evidence
- `docs/LANGUAGE_PRESSURES.md` — pressure ledger with reproducers
- `docs/rfcs/0001-foundation.md` — foundation RFC (implemented
  slice noted)

## Adding a new formulation

1. Create `src/fluid/<name>.mncs` (`module mncs.fluid.<name>.v1`;
   the file path must mirror the module segments).
2. State governing equations, assumptions, units, stability
   limits, and solver tolerances in the header; map every math
   term to its implemented term.
3. Validate all inputs into data outcomes (no traps for bad models).
4. Add a native suite under `tests/native/` + runner entry, with
   known-answer, conservation, symmetry, and degenerate cases plus
   oracle cross-checks. Do not infer correctness from convergence.
