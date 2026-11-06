---
name: git-workflow
description: Branch naming, Conventional Commits, and commit and push cadence rules. Use whenever creating a branch, writing a commit message, committing, or pushing — in remote repositories and in session working folders alike.
---

# Git workflow

All work on remote repositories happens on feature branches, never directly on `main` or `master`.

- **Branch names**: follow conventional format — `<type>/<short-description>` (e.g. `feat/add-subject-validator`, `fix/missing-modality-field`, `chore/update-deps`)
- **Commit messages**: use [Conventional Commits](https://www.conventionalcommits.org/) — `<type>(<scope>): <description>` (e.g. `feat(schema): add optional funder field`)

Common types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`

- **Commit often**: commit after every major step (e.g. a working script, a completed transformation, a plan change), in both remote repositories and session working folders. Don't let significant work accumulate uncommitted.
- **Keep published branches current**: once a feature branch is published (pushed to the remote), push every local commit to it as you make them, not in one batch at the end. The remote should never lag far behind local work, so progress is visible and nothing is lost if the local copy goes away.
