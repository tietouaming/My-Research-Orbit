# COMSOL Model Audit Note

Problem: A COMSOL model review can become unreliable if formulas are copied from memory
instead of a structured extraction layer.

Action: Review parameters, variables, weak forms, boundary conditions, solver settings,
and result groups from a structured model summary. Treat raw `.mph` and `.mphbin` files
as private source artifacts that must not be committed.

Rule: Preserve original expressions and domain mappings before interpreting physics.

Verification: t=0 whole-field comparison is the first trusted migration gate; later time
steps require DOF ordering and boundary-condition checks.

Tags: comsol, mesh, weak form, solver
