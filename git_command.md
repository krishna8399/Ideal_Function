# Git Workflow for Ideal Function Assignment Project

This document describes the standard Git workflow for collaborating on this project.

## Clone the Repository and Switch to Develop Branch

```bash
git clone <repo-url>
cd <repo-folder>
git checkout develop
```

## Make Changes and Stage Them

```bash
git add <changed-files>
```

## Commit Your Changes

```bash
git commit -m "Describe your changes"
```

## Push Your Changes to the Remote Develop Branch

```bash
git push origin develop
```

## Create a Pull Request

- Go to your Git platform (e.g., GitHub, GitLab, Bitbucket).
- Create a pull request from your develop branch.
- After review, your changes will be merged into the develop branch.

---

**Note:**  
Replace `<repo-url>`, `<repo-folder>`, and `<changed-files>` with your actual repository URL, folder name, and file names.