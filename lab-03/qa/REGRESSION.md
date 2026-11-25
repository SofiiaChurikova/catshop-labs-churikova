# Regression

Incident: in lab 1 the app started before Postgres was ready and logged
`db not ready (1/30): ... Connection refused`. It got the db on the second try, but if the db never
came up the app would still start, and `/health` would still say `ok` because it doesn't check the db.

Case: `test_ready_uses_postgres` checks `/ready` and that the store is `postgres`, not the file
fallback. `test_visits_are_stored_in_postgres` does the same for the counter.

Required check: `qa / qa (none)` and `qa / qa (partner)` in the `lab-03 publish` workflow. That's the
job name, so if the job is renamed the branch rule has to change too.
