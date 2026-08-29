# Install development skills

This repository contains atomic development skills and installable flows for Codex. Install each flow with every atomic skill it names.

## Repository structure

- `backend/`: backend skills grouped by language and framework
- `frontend/`: frontend skills
- `framework-agnostic-languages/`: language skills without framework coupling
- `flows/`: workflows that compose atomic skills

Each installable directory contains a `SKILL.md` file. Folder name becomes installed skill name.

## Install Spring backend flow from GitHub

The Spring backend flow needs six atomic skills. Run bundled Codex installer from any directory:

```bash
codex_dir="${CODEX_HOME:-$HOME/.codex}"
installer_dir="$codex_dir/skills/.system/skill-installer"

python3 "$installer_dir/scripts/install-skill-from-github.py" \
  --repo muhammadismailkhan0009/dev-skills \
  --path \
    backend/java/spring/modular-architecture \
    backend/java/spring/spring-services \
    backend/java/spring/spring-api \
    backend/java/spring/spring-data-jpa \
    backend/java/spring/testing \
    backend/java/mappers/mapstruct \
    flows/spring-backend
```

Installer places each directory under `${CODEX_HOME:-$HOME/.codex}/skills`. It stops when destination skill already exists. Remove or rename old installation before reinstalling; do not overwrite without reviewing local changes.

Use `--ref branch_or_tag` when installing version other than repository default branch. GitHub installation can only use committed and pushed files.

Start new Codex turn after installation. Invoke complete flow with `$spring-backend`, or invoke atomic skill directly.

## Install from local clone

Set destination, verify names do not exist, then copy required directories:

```bash
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills_dir"

cp -R backend/java/spring/modular-architecture "$skills_dir/"
cp -R backend/java/spring/spring-services "$skills_dir/"
cp -R backend/java/spring/spring-api "$skills_dir/"
cp -R backend/java/spring/spring-data-jpa "$skills_dir/"
cp -R backend/java/spring/testing "$skills_dir/"
cp -R backend/java/mappers/mapstruct "$skills_dir/"
cp -R flows/spring-backend "$skills_dir/"
```

Run commands from repository root. Copying into existing directory may merge files, so verify destination names first.

## Install one atomic skill

Use one repository path when full flow is unnecessary:

```bash
codex_dir="${CODEX_HOME:-$HOME/.codex}"
installer_dir="$codex_dir/skills/.system/skill-installer"

python3 "$installer_dir/scripts/install-skill-from-github.py" \
  --repo muhammadismailkhan0009/dev-skills \
  --path backend/java/spring/spring-api
```

Atomic skills work independently. Flow needs every atomic skill referenced by its `SKILL.md`.

## Verify installation

Check installed folders:

```bash
find "${CODEX_HOME:-$HOME/.codex}/skills" -maxdepth 2 -name SKILL.md -print
```

Expected Spring backend skill names:

- `modular-architecture`
- `spring-services`
- `spring-api`
- `spring-data-jpa`
- `spring-testing`
- `mapstruct`
- `spring-backend`

## Update installed skills

Installer does not replace existing skill directories. Review upstream changes, remove old installed directory, then run installation again. Preserve local edits before removal.
