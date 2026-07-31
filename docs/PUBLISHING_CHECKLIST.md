# GitHub publishing checklist

**Repository owner and maintainer:** Dr. Awanish Pratap Singh

## Before the first push

- [ ] Use the repository name `DFG-Research-Grant-LaTeX-Template`.
- [ ] Create an empty repository without an additional README, license or
      ignore file.
- [ ] Confirm the local default branch is `main`.
- [ ] Confirm the local author and committer identity:

  ```bash
  git var GIT_AUTHOR_IDENT
  git var GIT_COMMITTER_IDENT
  ```

- [ ] Confirm the working tree is clean:

  ```bash
  git status --short --branch
  ```

- [ ] Confirm no generated or third-party document files are tracked:

  ```bash
  git ls-files "*.pdf" "*.rtf" "*.log" "*.aux" "*.synctex.gz"
  ```

- [ ] Inspect all tracked files:

  ```bash
  git ls-files
  ```

- [ ] Build and validate both language templates:

  ```powershell
  powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1 -Language all
  ```

## Recommended repository information

- Description: `Unofficial reusable LaTeX template for DFG Research Grant project descriptions.`
- Topics: `latex`, `dfg`, `research-proposal`, `grant-writing`,
  `scientific-writing`
- Default branch: `main`
- License: `MIT`

## Push commands

After creating the empty repository:

```bash
git remote add origin https://github.com/awanishsingh009/DFG-Research-Grant-LaTeX-Template.git
git remote -v
git push -u origin main
```

Review the remote URL before pushing.

## After the first push

- [ ] Confirm GitHub displays the README and MIT license.
- [ ] Confirm GitHub recognises `CITATION.cff`.
- [ ] Confirm the author is shown as Dr. Awanish Pratap Singh.
- [ ] Open every relative documentation link.
- [ ] Confirm no proposal data or local paths appear in repository search.
- [ ] Create release `v1.0.0` from the verified commit if a release is wanted.

## Before every future release

- [ ] Recheck the live DFG forms page.
- [ ] Update `guideline-versions.tex`, the source register and changelog.
- [ ] Compile both languages in guidance mode and run automated QA.
- [ ] Compile a strict example separately when suitable test content is
      available.
- [ ] Inspect every rendered page.
- [ ] Run credential and private-data scans.
- [ ] Review the full commit diff and commit identities.
- [ ] Tag only a clean, verified commit.
