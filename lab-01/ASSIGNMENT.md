# Lab 1 — containers and the image

**Covers:** syllabus assignments 1 and 2 · **12 points** · **three sections**
**Opens:** Thursday 22 October · **Due:** Thursday 12 November
*Lab 2 (test, build, publish) opens 29 October while this one is still open. That is slack, not three weeks of work.*

---

## What you are given

```
app.py                 a small Flask app — do not change it
requirements.txt       its three dependencies
init-db/01-schema.sql  the schema, applied on the database's first boot
partner/mappings/      a third party's stubbed responses
.env.example           copy to .env. Never commit .env
```

## What you write

```
Dockerfile        sections 1 and 2
.dockerignore     section 1
compose.yaml      section 3
```

All of it inside `lab-01/`.

## The application

Three endpoints, chosen because each depends on a different kind of thing:

| Endpoint | Depends on | Section |
|---|---|---|
| `GET /health` | nothing | 1 |
| `GET /visits` | our own state — a file, then a database | 1, then 3 |
| `GET /price/<sku>` | an API we do not own | bonus |

Run it without Docker first, so you know what "working" looks like before you containerise it:

```bash
cd lab-01
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
COUNTER_FILE=./data/visits.txt ./.venv/bin/python app.py
```

> **One contract the grader depends on: publish the app on host port `8080`.**
> Sections 1 and 2 run your image directly; section 3 runs your `compose.yaml`. Both probe
> `localhost:8080`.

---

## Section 1 · a Dockerfile that runs

Write `Dockerfile` and `.dockerignore`. Build the image, run it, reach it from your host.

**Checked:** the base image is pinned (not `:latest`) · `requirements.txt` is copied *before* the
source · there is a `CMD` or `ENTRYPOINT` · `.dockerignore` excludes `.env` and `.git` · the image
builds · `/health` answers · `/visits` counts up.

**In the pull request:**

- **What does `EXPOSE` actually do?** Then run the container *without* `-p` and try to reach it.
  Paste what happened.
- **The cache, measured.** `time docker build` twice. Change one line of `app.py`. Build again.
  Then swap your `COPY requirements.txt` and `COPY app.py` lines and repeat. **Both sets of timings
  go in the pull request**, with the reason for the difference.
- What changed in the `transferring context` line when you added `.dockerignore`?

> `examples/1-dockerfile/` and `examples/1a-cache/` demonstrate all of this with output shown.
> `1a-cache` measures eight separate cache scenarios — two of them come out the opposite way round
> to how most people guess.

## Section 2 · multi-stage, and not root

Same application, built so that nothing the build needed ships to production.

**Checked:** two or more `FROM` stages · a non-root `USER` that is not `root`/`0` · no C compiler in
the runtime image · `apt-get update` never alone in its own layer · no `rm -rf /var/...` stranded in
its own `RUN` · the running process is not uid 0.

**In the pull request:**

- **Both image sizes.** Build it single-stage and multi-stage and report both numbers.
- **Prove the compiler is gone.** Ask both images for `gcc`. One answers; one cannot be asked.
- **Find out what dropping root costs.** Try to make the app listen on port **80** as your non-root
  user. Paste the error, and explain in one line why it listens on 8080 instead.
- **Why chain `apt`/install commands with `&&`?** Not "fewer layers are smaller" — that is mostly a
  myth. Give the two reasons that are actually true: what happens to a cleanup that sits in its own
  `RUN`, and what happens when `apt-get update` is cached in a layer of its own while the `install`
  line changes. Then the counter-pressure: why one giant `RUN` is also wrong.

## Section 3 · Compose, Postgres, and a volume

`compose.yaml` with your app and a database. Move the counter into Postgres by setting
`DATABASE_URL`. The database gets a `healthcheck`; the app gets
`depends_on: { condition: service_healthy }`. **Do not publish the database port.**

**Checked:** `compose.yaml` parses · a `volumes:` block exists · the database has a `healthcheck` ·
`depends_on` is gated on `service_healthy` · the database port is not published · `/visits` reports
`store=postgres` and counts up · **the rows survive `down` then `up`**.

**In the pull request:**

- **The data-loss transcript.** Hit `/visits` twice, `docker compose down`, `up` again — once
  *without* a named volume and once *with* one. **Paste both transcripts.** The first one must show
  the counter going backwards.
- What did plain `depends_on` do before you added the health gate? Try it, paste the log.
- One paragraph: a named volume versus a bind mount, and when you would use each.

---

## Bonus — adds marks, never costs them

Both bonus checks run with `continue-on-error`, so a red bonus job does not fail your pipeline.

**+ The partner API** (`section · wiremock`). Add the `partner` service — `wiremock/wiremock:3.6.0`,
stubs already in `partner/mappings/` — and set `PARTNER_URL`, so `/price/MK-II` answers. Then show
the two failure modes the real partner would never give you on demand: `/price/BOOM-1` and
`/price/SLOW-1`. Paste both.

**+ Closing the door** (`section · networks`). Put the database and the partner on `internal: true`
networks. Show that **neither can reach the internet** while the app still reaches both. Then reach
the database four ways and record all four with their real error text: `localhost:5432` · `db:5432`
on the default bridge · the container's **IP address** · `db:5432` on a network you created. Restart
the database after the IP attempt, and explain in two sentences why that attempt was wrong **even
though it worked**.

**+ Your own application** (+10). Do all three sections again against a service you wrote, in any
language. It must expose `/health` and read its configuration from the environment.

---

## Before you open the pull request

```bash
./scripts/verify.sh --section dockerfile --path lab-01
./scripts/verify.sh --section hardening  --path lab-01
./scripts/verify.sh --section compose    --path lab-01
```

Or just push — the pipeline runs the same checks and reports one per section.

Then fill in the pull request template. **The alternatives, the measurements and the AI disclosure
are each worth marks**, and the automated checks cannot award them.
