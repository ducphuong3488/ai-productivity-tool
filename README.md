# ai-productivity-tool
An open-source AI-powered productivity tool designed to automate repetitive workflows and help users work more efficiently

## Skills

### `seedance-video` — Seedance 2.0 prompt writer

A Claude Code skill (`.claude/skills/seedance-video/`) that turns a short idea into a ready-to-paste Seedance 2.0 video prompt: subject, action, camera, lighting, style, audio, and timecoded multi-shot breakdowns for clips up to 15 seconds.

- `SKILL.md` — workflow and output format
- `references/` — prompt formula, camera/lighting/style vocabulary, 15s shot templates, worked examples
- `scripts/build_prompt.py` — builds a timecoded prompt from a JSON shot list and checks duration, missing camera moves and prompt length

```bash
python3 .claude/skills/seedance-video/scripts/build_prompt.py shots.json
```

The skill writes prompts only; video generation happens on your Seedance platform under its own quotas and terms.
