# Cache

Two caches in `publish-lab-02.yml`:

- pip downloads: `actions/setup-python` with `cache: pip`, keyed on the hash of `lab-02/requirements*.txt`
- docker layers: `docker/build-push-action` with `type=gha,scope=lab-02,mode=max`, so both stages of the Dockerfile are cached

| run | cache | test job | image job |
|---|---|---|---|
| #1, commit 2ba1b1c | cold | 25 s | 1 min 12 s |
| #3, commit 7670066 | warm | 19 s | 33 s |

The image job got about twice as fast, because the build stage with `pip install` came from the layer cache instead of running again. Run #1 failed on the push (403), so its image time is the build, the smoke test and the failed push.
