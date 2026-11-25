# Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

I pushed two commits one right after the other:

- cancelled: [run #3](https://github.com/SofiiaChurikova/catshop-labs-churikova/actions/runs/45674355163) (`lab-03: published digest`)
- it was cancelled by: [run #4](https://github.com/SofiiaChurikova/catshop-labs-churikova/actions/runs/45674377006) (`lab-03: cache timings`)

```
Canceling since a higher priority waiting request for lab-03 publish-refs/heads/lab-03 exists
```

Run #3 was cancelled in `build / test`, so nothing was built or pushed. It was safe because the newer
commit has everything the old one had, and run #4 published it anyway. Even if it had been cancelled
in the middle of the push, the image would only be under its own sha tag, and `published.txt` is
written only by `promote` after QA, so nothing would point to a half-done image.

On `main` cancel-in-progress is false: runs there queue and every merged commit is published.
