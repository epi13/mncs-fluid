# Fluid model and ownership boundary

## What Fluid owns

Fluid-domain semantics, and only those:

- **State variables** — velocity profiles at node lanes (`[f64; N]`
  with walls at lanes 0/hi). Only velocity: the incompressible
  slice needs nothing else. No universal field dictionary.
- **Properties** — `FluidProps { density, viscosity }` (SI units
  documented per field), positivity validation as data outcomes,
  kinematic viscosity, Reynolds number.
- **Driving force** — `DrivingForce { gradient }` with the fixed sign
  convention G = -dp/dx. Negative (reversed) and zero (quiescent)
  gradients are legitimate physics, not errors.
- **Boundary conditions** — `WallLaw::NoSlip` with wall values,
  resolved against lane identities (0/hi), never strings.
- **Initial conditions** — `InitialState { kind, source }` with
  `Specified/Derived/Defaulted` provenance. The default quiescent
  start is marked defaulted so no consumer mistakes it for data.
- **Governing-equation terms** — the steady viscous operator
  `-u[i-1]+2u[i]-u[i+1] = G*h²/mu`, the FTCS update, face fluxes
  with +y orientation, each mapped math-term -> implemented-term in
  module headers.
- **Fluid discretization descriptors** — `ChannelGrid` (walls,
  interiors, faces of one channel slice). Not a generic mesh.
- **Fluid solvers** — Thomas direct solve and Jacobi iteration for
  the uniform-grid viscous system, with `ZeroPivot`/residual/
  convergence semantics. Not generic sparse solvers.
- **Derived quantities** — flow rate (trapezoid, O(h²)), wall shear
  (one-sided, O(h)), discrete conservation imbalance.
- **Simulation time** — `SimClock { t, step }` carried as data,
  advanced by validated dt. Never wall-clock time.
- **Results** — `ChannelN::Value { u, flow_rate, shear_lo,
  shear_hi, imbalance }` and `Transient5::Value { u, t, steps }`
  with `BadInput/Singular/Unstable` failure arms kept distinct.

## What Fluid does not own

- **Numeric** (`mncs-numerics`): f64 representation, `fabs`,
  `approx` tolerance policy, trap rule. Consumed, never duplicated.
- **Math** (`mncs-math`): generic matrices, exact solvers, sparse
  kernels, tensor algebra. Deliberately not a dependency of this
  slice; the uniform-grid kernels need nothing beyond Numeric.
- **Geometry** (`mncs-geometry`): point/vector/transform semantics.
  The 1D slice carries scalar lane coordinates; 2D+ work must
  consume Geometry, not wrap it.
- **FEM** (`mncs-fem`): finite-element topology/assembly. Fluid
  uses finite differences/volumes here and forces nothing into FEM
  abstractions. A future FEM-based fluid formulation would consume
  FEM mechanics with the fluid weak form owned here.
- **Data** (`mncs-data`): no field serialization in Fluid.
- **Generic solvers**: variable-coefficient tridiagonal, Krylov,
  Newton methods belong in Math/a numerical component, not here.
- **Execution**: Forge/Fabric own admission/lifecycle; Store owns
  persistence; Lineage owns provenance graphs. Fluid persists
  nothing and schedules nothing.
- **Test/Debug/Doctor**: verification runs on `mncs-test`; failure
  evidence is structured data for Debug/Doctor to consume.

## Deliberately out of scope

Turbulence, shocks, multiphase, high-Re CFD, pressure-velocity
coupling (SIMPLE/projection), FEM-based formulations, 2D/3D meshes,
parallel domain decomposition, CUDA, checkpoint/restart, generic PDE
frameworks, private units systems. The architecture layers reserve
space for them; the foundation slice proves the semantic structure.

## RFC scope classification (0001-foundation)

1. **Foundational Fluid semantics** (implemented): props, walls,
   driving force, initialization provenance, flux orientation,
   conservation identity, sim time.
2. **Generic numerical/PDE infrastructure** (proven-needed, kept
   local): fixed-count drivers, residual/convergence predicates —
   recorded as pressures, not new repositories.
3. **FEM-owned** (untouched): element topology/assembly; no FVM
   semantics forced into FEM.
4. **Math/Numeric/Geometry responsibility** (consumed or
   pressured): scalar discipline (consumed), generic solvers and
   tensor/field algebra (pressured).
5. **Future Fluid scope** (deferred): Couette flow, cavity
   benchmark, FEM-based fluids, 2D, pressure-velocity coupling.
6. **Obsolete/over-ambitious** (cut): SIMD/CUDA paths before one
   verified solver; framework-first interfaces; multiphase and
   turbulence in the foundation.

## Historical note

The repository bootstrapped with architecture docs only (no host
CFD code, no prior consumers anywhere in the family). There was no
legacy implementation to port or remove: the foundation below is
the first and only canonical implementation, built directly against
the current language and the modernized Numeric/Test libraries. No
`fluid-v1/v2`, no `native-fluid`, no compatibility layers exist.
