# Shap-E 3D Model Pipeline

A text-to-3D model pipeline built on top of OpenAI's open-source Shap-E model.
Type a text prompt like "a wooden chair" or "a medieval helmet" and get back a
real 3D model file (.obj or .glb) you can open in Blender or any 3D viewer.

## What this does
- Takes a plain English text prompt as input
- Runs it through Shap-E's diffusion model on Google Colab (free T4 GPU)
- Outputs a usable 3D mesh file in .obj or .glb format

## Stack
- [Shap-E](https://github.com/openai/shap-e) by OpenAI
- Python 3
- Google Colab (T4 GPU)

## Project Status
Under active development. Following a phase-by-phase build:
- [ ] Phase 1 — Environment setup & dependency validation
- [ ] Phase 2 — Manual inference walkthrough
- [ ] Phase 3 — Pipeline module
- [ ] Phase 4 — Parameter tuning
- [ ] Phase 5 — Output validation
- [ ] Phase 6 — Prompt engineering

## Usage
_Will be updated as each phase completes._

## Output Examples
_Will be added once the pipeline is working._

## License
MIT
