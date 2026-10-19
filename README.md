# catshop-labs — your repository for the whole course

One repository. One folder per lab. Seven labs and the capstone all land here, so by December this
repo *is* your portfolio: a commit history that shows an application going from a laptop to
production.

| Folder | What it is | Announced | Due |
|---|---|---|---|
| `lab-01/` | containers and the image | **22 Oct** | **12 Nov** |
| `lab-02/` | test, build, publish | 29 Oct | 19 Nov |
| `lab-03/` | a pipeline that does not repeat itself | 5 Nov | 26 Nov |
| `lab-04/` | Terraform, and the first environment | 12 Nov | 3 Dec |
| `lab-05/` | many environments, no secrets in Git | 19 Nov | 10 Dec |
| `lab-06/` | into the cluster | 26 Nov | 17 Dec |
| `lab-07/` | release without downtime | 3 Dec | 20 Dec |
| `capstone/` | ship it to production | 26 Nov | 20 Dec |

Each folder arrives with the application and its fixtures already in it. What is **missing** from a
lab folder is the work: that is what you write.

**The labs overlap on purpose.** Lab 1 is still open when lab 2 opens. Three weeks is slack for when
a week goes badly — it is not three weeks of expected work, and the content is serial, so putting
one off blocks the next.

**From lab 4 you need your own AWS account.** Open it early: the free tier is a **12-month clock**
from the day you create the account, and lab 4's load balancer is only free inside it. Labs 1 to 3
need no cloud account at all.

---

## How a lab is passed

**1 · A lab opens at the Thursday lecture.** The folder appears, and its `ASSIGNMENT.md` tells you
the sections, what each one is checked on, and what has to go in the pull request.

**2 · Work on a branch named after the lab.**

```bash
git switch -c lab-01
```

**3 · Push. The pipeline grades you immediately.** Every lab has its own workflow, which runs only
when that lab's folder changes. You get one named check per section:

```
✓ section · dockerfile      17 checks
✓ section · hardening       16 checks
✓ section · compose         18 checks
– section · wiremock        bonus, never fails the build
```

Click any check to see the table: every check that passed, every one that failed, and why. The same
script decides your mark, so there is no hidden rubric — **you are handed the grader in advance, on
purpose.**

Run it locally first if you prefer not to wait on CI:

```bash
./scripts/verify.sh --section dockerfile --path lab-01
```

**4 · Open a pull request into `main`** when the required sections are green. The template asks you
for three things, and they are worth marks:

- the **alternatives** you considered, and the price of the one you chose
- the **measurements** the assignment asked for — build times, image sizes, the error text
- your **AI-tool disclosure**: which tool, what you asked, how you changed the output

**5 · You get a code review on the diff**, not a grade in a spreadsheet. Reply to the comments. One
resubmission is allowed within a week of the review.

**6 · Merge it.** The folder is then frozen. Lab 3 never edits `lab-01/`, which is why its workflow
keeps passing for the rest of the course.

---

## How it is marked

Each lab is worth the points stated in its `ASSIGNMENT.md`, split three ways:

| | Points | Decided by |
|---|---|---|
| **Correctness** | ⅓ | the required sections are green |
| **Engineering quality and reasoning** | ⅓ | the pull request: alternatives, price, readable config, no secrets where they do not belong |
| **Automation and reproducibility** | ⅓ | it works from code, on a clean machine, not from steps you performed by hand |

A **red required section** costs correctness marks. A **bonus section** runs with
`continue-on-error`, so it can only ever add.

Two things score zero regardless of how green the checks are:

- **a committed `.env`** — the grader checks your git *history*, not just your working tree. A
  secret that was ever committed is a leaked secret. Remove it and rotate the value.
- **configuration you cannot explain.** Copying from documentation, a blog post or a classmate is
  fine and is part of the real job — *when you name the source in the pull request and can explain
  every line*. Submitting config whose behaviour you cannot explain is not.

**After the deadline the maximum for that lab is 80% of its points.** The deadline is in
`ASSIGNMENT.md` and labs overlap — lab 1 is still open when lab 2 opens. That is deliberate slack,
not three weeks of expected work.

---

## Where to look things up

**[catshop-examples](https://github.com/kse-ci-cd-basics-course/catshop-examples)** has the same
application built one step at a time: a Dockerfile, then the build cache measured across eight
scenarios, then multi-stage, then Compose, then Postgres, then a stubbed partner API, then closed
networks. Each step has its own README with the commands and the expected output.

**Read it, run it, diff the steps against each other.** It is not a solution to copy — the folder
layout is different and the measurements are from a different machine — but every mechanism you need
is demonstrated there with its output shown.

```bash
diff -ru -x README.md -x .env 2-compose-postgres-no-volume 3-compose-postgres-volume
```

That diff is persistence, entire: one mount and one `volumes:` key.

---

## Before you push

```bash
cp lab-01/.env.example lab-01/.env     # never commit .env
git check-ignore lab-01/.env           # must print the path. If it prints nothing, stop
```
