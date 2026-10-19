# catshop-labs — your repository for the whole course

One repository. One folder per lab. Every lab lands here, so by December this repo *is* your
portfolio: a commit history that shows an application going from a laptop to production.

A folder appears when its lab is announced. Each one arrives with the application and its fixtures
already in it — what is **missing** from a lab folder is the work, and that is what you write.

```
lab-01/   containers and the image        ← open now
```

Deadlines are announced in the lecture. Labs overlap: an earlier one may still be open when the next
appears, and the content is serial, so putting one off blocks the next.

---

## How a lab is passed

**1 · A lab opens at the lecture.** The folder appears, and its `ASSIGNMENT.md` tells you the
sections, what each one is checked on, and what has to go in the pull request.

**2 · Work on a branch named after the lab.**

```bash
git switch -c lab-01
```

**3 · Push. The pipeline grades you.** Every lab has its own workflow, which runs only when that
lab's folder changes. You get one named check per section:

```
✓ section · dockerfile          17 checks
✓ section · hardening           15 checks
✓ section · compose             18 checks
– section · wiremock (bonus)    never fails the build
```

Click any check to see the table: every check that passed, every one that failed, and why. **That
table is the whole rubric — there is nothing hidden behind it.** Push early and push often; the
pipeline is how you find out where you stand, and it costs you nothing to run.

**4 · Open a pull request into `main`** when the required sections are green. The template asks you
for three things, and each is worth marks:

- the **alternatives** you considered, and the price of the one you chose
- the **measurements** the assignment asked for — build times, image sizes, the error text
- your **AI-tool disclosure**: which tool, what you asked, how you changed the output

A pull request with an empty template section is sent back automatically, before anyone reads it.

**5 · You review two classmates' pull requests**, against the same rubric. This is part of your mark,
and it is a course objective in its own right — reading someone else's configuration and saying
something useful about it is the job.

**6 · You get a code review on the diff**, not a grade in a spreadsheet. Reply to the comments. One
resubmission is allowed within a week of the review.

**7 · Merge it.** The folder is then frozen. A later lab never edits an earlier lab's folder, which
is why its checks keep passing for the rest of the course.

---

## How it is marked

| | Decided by |
|---|---|
| **Correctness** | the required sections are green |
| **Engineering quality and reasoning** | the pull request: alternatives, price, readable configuration, no secrets where they do not belong |
| **Automation and reproducibility** | it works from code, on a clean machine, not from steps you performed by hand |

Half the mark is the automated checks. A **red required section** costs correctness marks; a **bonus
section** runs with `continue-on-error`, so it can only ever add.

Two things score zero regardless of how green the checks are:

- **a committed `.env`** — the checks read your git *history*, not just your working tree. A secret
  that was ever committed is a leaked secret. Remove it and rotate the value.
- **configuration you cannot explain.** Copying from documentation, a blog post or a classmate is
  fine and is part of the real job — *when you name the source in the pull request and can explain
  every line*. Submitting configuration whose behaviour you cannot explain is not.

After the deadline, the maximum for that lab is 80% of its points.

---

## Where to look things up

**[catshop-examples](https://github.com/kse-ci-cd-basics-course/catshop-examples)** has the same
application built one step at a time: a Dockerfile, then the build cache measured across eight
scenarios, then multi-stage, then Compose, then Postgres, then a stubbed partner API, then closed
networks. Each step has its own README with the commands and the expected output.

**Read it, run it, diff the steps against each other.** The folder layout differs from yours and the
measurements come from a different machine, but every mechanism you need is demonstrated there with
its output shown.

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
