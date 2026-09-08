# Agent and contributor contract

- Prefer `mncs-language` for implementation.
- State governing equations, discretization, mesh, boundary conditions, timestep/stability criteria, precision and solver tolerance explicitly.
- Validate conservation, residuals and convergence; a visually plausible flow field is not scientific verification.
- Use analytic/manufactured solutions and established benchmark cases where possible.
- Keep numerical method semantics distinct from parallel/GPU implementation strategy.
- Record language/compiler/runtime pressure in `docs/LANGUAGE_PRESSURES.md`.
- Do not weaken stability or convergence checks merely to make an accelerated path pass.
