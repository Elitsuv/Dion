#!/usr/bin/env bash
# Deletes default GitHub labels and creates the Dion "Di: ..." label suite.
# Prerequisites: GitHub CLI (`gh auth login`)

set -e

DEFAULT_LABELS=(
  "bug"
  "documentation"
  "duplicate"
  "enhancement"
  "good first issue"
  "help wanted"
  "invalid"
  "question"
  "wontfix"
)

echo "Deleting default GitHub labels..."
for label in "${DEFAULT_LABELS[@]}"; do
  gh label delete "$label" --yes 2>/dev/null || true
done

echo "Creating Dion 'Di: ...' labels..."
gh label create "Di: Skill"            --color "1d76db" --description "New agent skill proposal or addition" --force
gh label create "Di: Update"           --color "5319e7" --description "Enhancement or update to an existing skill" --force
gh label create "Di: Fix"              --color "d93f0b" --description "Bug fix or correction in a skill's instructions" --force
gh label create "Di: Chore"            --color "7057ff" --description "Repository maintenance, templates, or workflows" --force
gh label create "Di: Docs"             --color "0075ca" --description "Improvements to README, CONTRIBUTING, or guides" --force
gh label create "Di: Pedagogy"         --color "fbca04" --description "Curriculum alignment or conceptual clarity for students" --force
gh label create "Di: Good First Issue" --color "008672" --description "Friendly task for students and first-time contributors" --force
gh label create "Di: Help Wanted"      --color "b60205" --description "Extra domain expertise or student feedback requested" --force

echo "Label setup complete!"

