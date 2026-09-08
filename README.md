# mncs-fluid

Machine-native computational fluid dynamics for MNCS.

`mncs-fluid` is a scientific CFD framework and a high-pressure `mncs-language` workload for multidimensional fields, PDE discretization, sparse/iterative solvers, stencil computation, parallel reductions, memory layouts, domain decomposition and heterogeneous CPU/GPU execution.

## Initial scope

- structured/unstructured field and mesh foundations
- governing-equation and discretization abstractions
- incompressible flow as the first validated solver family
- boundary and initial conditions
- pressure/Poisson and iterative solver integration
- explicit/implicit time integration and CFL/stability evidence
- conservation, residual and convergence verification
- SIMD, multithreaded and CUDA execution paths

## Repository layout

- `docs/ARCHITECTURE.md`
- `docs/rfcs/0001-foundation.md`
- `docs/LANGUAGE_PRESSURES.md`
- `AGENTS.md`
