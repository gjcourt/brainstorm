# Copilot Instructions: Branching and PR Workflow

When working in this repository, you must strictly adhere to the following branching and Pull Request workflow:

## 1. Branching Strategy
- **Never commit directly to the `main` branch.**
- Always create a new branch for any changes, features, or bug fixes.
- Use descriptive branch names following this convention:
  - `feature/<short-description>` for new features or projects.
  - `fix/<short-description>` for bug fixes.
  - `docs/<short-description>` for documentation updates.
  - `chore/<short-description>` for maintenance tasks (e.g., linting, CI updates).

## 2. Committing Changes
- Write clear, concise, and descriptive commit messages.
- Use the imperative mood in the subject line (e.g., "Add project tracking structure", not "Added" or "Adds").
- Group related changes into logical commits.

## 3. Pull Request Workflow
- Once changes are committed to your branch, push the branch to the remote repository.
- Create a Pull Request (PR) targeting the `main` branch.
- The PR title should clearly summarize the changes.
- The PR description must include:
  - A summary of the changes made.
  - The motivation or context for the changes.
  - Any relevant issue numbers or project references.
- Ensure all CI checks (linting, formatting) pass before requesting a review or merging.
- Do not merge your own PR without approval (if branch protection rules are in place).

## 4. Project Tracking Structure
- Projects are tracked within their respective category folders (e.g., `audio-midi/`).
- Each category has a `projects/` subfolder containing individual project files.
- Project files must be named using a numbered prefix and a slug (e.g., `001-midi-controller.md`).
- The main `projects.md` file in each category serves as an index/dashboard linking to the individual project files.
- Use Markdown and YAML frontmatter for structured data within project files.

## 5. Linting and Formatting
- This repository uses local npm scripts for linting and formatting Markdown and YAML files.
- Always run the formatting and linting scripts before committing changes to ensure CI checks pass.
