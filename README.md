# Neuromatch Project

Working repo for our Neuromatch Academy project on Zhong et al. 2025 (mouse visual
cortex, supervised/unsupervised learning).

## Git workflow (start here if you're new to GitHub)

We use one simple rule: **nobody commits to `master` directly. You make a branch,
push it, and open a Pull Request (PR).** Akeel reviews and merges. This keeps
`master` always working and makes it easy to see who changed what.

### One-time setup

```bash
# Clone the repo (only do this once, creates a `neuromatch` folder)
git clone https://github.com/Akeel-Majeed/neuromatch.git
cd neuromatch

# Tell git who you are (use your GitHub email)
git config user.name "Your Name"
git config user.email "you@example.com"
```

### The daily loop

```bash
# 1. Get the latest master before you start ANY new work
git checkout master
git pull

# 2. Make a branch for what you're about to do (pick a short descriptive name)
git checkout -b my-analysis

# 3. ...edit files, do your work...

# 4. See what you changed
git status              # which files changed
git diff                # the actual changes

# 5. Stage and commit
git add .               # stage everything (or `git add <file>` for specific files)
git commit -m "Add PSTH plot for V1 neurons"

# 6. Push your branch to GitHub
git push -u origin my-analysis
```

After the push, GitHub prints a link — open it to create a **Pull Request**.
Or run `gh pr create` if you have the [GitHub CLI](https://cli.github.com/).

### Staying in sync

Before starting new work each day, pull the latest `master` so you don't drift:

```bash
git checkout master
git pull
git checkout -b my-next-thing
```

If your branch is behind `master` and you want the newest changes in it:

```bash
git checkout my-branch
git merge master        # pulls master's changes into your branch
```

### "Help, I messed up"

| Situation | Fix |
|-----------|-----|
| Committed to `master` by accident (not pushed) | `git branch my-branch` then `git reset --hard origin/master` |
| Want to undo uncommitted changes to a file | `git checkout -- <file>` |
| Wrong commit message (last commit, not pushed) | `git commit --amend -m "better message"` |
| Not sure what state you're in | `git status` — it almost always tells you what to do next |

### Golden rules

1. **Always `git pull` on `master` before starting new work.**
2. **Never work directly on `master`** — branch first, always.
3. **Commit small and often** with clear messages.
4. **When in doubt, run `git status`** before doing anything else.
