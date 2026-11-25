# Cache

| run | cache | build / test | build / image | whole run |
|---|---|---|---|---|
| [#1 cold](https://github.com/SofiiaChurikova/catshop-labs-churikova/actions/runs/45672389352) | nothing saved yet | 12 s | 117 s | 193 s |
| [#2 warm](https://github.com/SofiiaChurikova/catshop-labs-churikova/actions/runs/45673376613) | pip + layers | 9 s | 25 s | 94 s |

Saved 99 s on the whole run, about 2x faster. Most of it is the layer cache: the image job went
from 117 s to 25 s because the build stage with `pip install` came from the cache. The pip cache
saved only 3 s.

Run #2 restored pip from the old key through `restore-keys`:
```
key: pip-Linux-bbb2e68d860ffa913f796d1e5a760b9d784a99b88286639e1db72088df988d58
Cache hit for restore-key: pip-Linux-
```
