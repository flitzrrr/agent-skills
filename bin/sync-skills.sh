#!/bin/bash
# Sync DDM (DasDigitaleMomentum) skills from agent-skills repo to agy
# Run after: git pull in agent-skills repo
SKILLS_DIR="/Users/Martin/.gemini/antigravity/skills"
SOURCE="/Users/Martin/git/agent-skills/vendor/opencode-processing-skills/skills"

DDM_SKILLS="archive-legacy-docs author-and-verify-implementation-plan create-plan execute-work-package generate-docs generate-handover resume-plan update-docs update-plan"

for skill in $DDM_SKILLS; do
    rm -rf "$SKILLS_DIR/$skill"
    cp -R "$SOURCE/$skill" "$SKILLS_DIR/$skill"
    echo "Synced: $skill"
done

echo "Done. Total SKILL.md: $(find $SKILLS_DIR -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
