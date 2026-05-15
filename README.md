# Shap-E 3D Model Pipeline

A text-to-3D model pipeline built on OpenAI's open-source Shap-E model. Type a prompt from your laptop's terminal and get a real `.obj` or `.glb` file in your `outputs/` folder — no Colab interaction needed after setup.

Generation runs on Google Colab's free T4 GPU. Your laptop and Colab communicate asynchronously through Google Drive, so there's no live connection, no tunneling, and no paid services involved.

---

## How It Works

```
Your Terminal → generate.py → Google Drive (pending folder)
                                      ↓
                              Colab watches Drive
                                      ↓
                              Shap-E generates .obj
                                      ↓
                         Drive (result uploaded back)
                                      ↓
                     generate.py downloads → outputs/
```

You run one command. Colab picks up the job, generates the model, and uploads it back. Your script polls Drive until the file appears, downloads it, and cleans up. The whole thing takes about 60–90 seconds per model.

---

## Stack

- [Shap-E](https://github.com/openai/shap-e) by OpenAI — text-to-3D diffusion model
- Google Colab (free T4 GPU) — runs the generation
- Google Drive API — job queue between laptop and Colab
- Python 3.10+

---

## One-Time Setup

### 1. Google Drive Folders

Create two folders in your Google Drive:

- `pending` — where job requests and results are exchanged
- `jobs` — archive (optional, for logging)

Note both folder IDs from the URL when you open them (`drive.google.com/drive/folders/<FOLDER_ID>`). Add them to `drive_client.py`:

```python
PENDING_FOLDER_ID = "your_pending_folder_id"
JOBS_FOLDER_ID    = "your_jobs_folder_id"
```

### 2. Google OAuth Credentials

- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a project → Enable the Google Drive API
- Go to Credentials → Create OAuth 2.0 Client ID (Desktop app)
- Download the JSON file and save it as `two.json` in your project root

### 3. Generate Your Token

Run `generate.py` once with any prompt. It will open a browser window asking you to sign in with Google and grant Drive access. After you approve, a `token.json` file will be created in your project root. This token persists and auto-refreshes — you won't need to authenticate again.

```bash
python generate.py "a wooden chair"
```

### 4. Add Token to Colab Secrets

- Open the `token.json` file and copy its entire contents
- In Colab, click the key icon (Secrets) in the left sidebar
- Add a new secret named `GDRIVE_TOKEN` and paste the contents as the value
- Enable notebook access

### 5. Share Drive Folders with Your Account

Share both Drive folders with the Google account you authenticated with, giving it Editor permissions. This allows Colab to read and write to those folders using your token.

---

## Usage

### Step 1 — Start Colab (once per session)

Open `colab_watcher.ipynb` in Google Colab and run all 5 cells in order. The last cell starts the watcher loop which runs indefinitely, waiting for jobs.

> Make sure you select a T4 GPU runtime: Runtime → Change runtime type → T4 GPU

### Step 2 — Generate from your terminal

```bash
python generate.py "a wooden chair"
```

```bash
python generate.py "a fire hydrant" --format obj
```

```bash
python generate.py "a medieval helmet" --format glb --timeout 600
```

Your file will appear in the `outputs/` folder as `<job_id>.obj` (or `.glb`).

### Arguments

| Argument | Default | Description |
|---|---|---|
| `prompt` | required | Text description of the 3D object |
| `--format` | `obj` | Output format: `obj` or `glb` |
| `--timeout` | `300` | Seconds to wait before giving up |

---

## What Prompts Work Well

Based on testing across 10+ prompts with Shap-E's default parameters (guidance_scale=3.0, steps=64):

**Works well:**
- Specific, unambiguous objects — `"a fire hydrant"`, `"a wooden chair"`, `"a cup"`
- Architectural shapes — `"a house"`, `"a door"`
- Vehicles — `"a car"` (rough but recognizable)
- Simple symmetric shapes — `"a vase"`, `"a trophy"`

**Avoid:**
- Fictional objects — `"a dragon"` maps to nearest real equivalent
- Surface quality descriptors — `"a smooth round vase"` degrades quality
- Objects with many thin separate parts — `"a table"` often loses its legs
- Abstract concepts — `"happiness"`, `"chaos"`

**Rule of thumb:** short, specific, real-world nouns. 2–4 words is the sweet spot.

---

## Project Structure

```
shape-e-pipeline/
│
├── generate.py          # CLI entry point — run this from your terminal
├── drive_client.py      # Google Drive API helpers (upload, poll, download)
├── two.json             # OAuth credentials (not committed)
├── token.json           # Generated auth token (not committed)
│
├── src/
│   ├── loader.py        # Loads Shap-E models (transmitter, text300M, diffusion)
│   ├── sampler.py       # Runs the diffusion loop, returns latents
│   ├── exporter.py      # Decodes latents → TriMesh → .obj or .glb
│   └── pipeline.py      # Wires loader → sampler → exporter
│
├── notebooks/
│   ├── setup.ipynb      # Phase 1 environment setup reference
│   └── phase_2.ipynb    # Phase 2 manual inference reference
│
└── outputs/             # Generated 3D files land here (gitignored)
```

---

## Parameters

These are set inside `colab_watcher.ipynb` and were tuned through systematic experimentation:

| Parameter | Value | Notes |
|---|---|---|
| `guidance_scale` | 3.0 | Higher values (>15) break mesh geometry |
| `steps` | 64 | Sweet spot between speed and quality |
| `format` | obj | `.obj` for Blender, `.glb` for web viewers |

---

## Limitations

- Colab session must be running manually for generation to work
- Free Colab tier disconnects after ~12 hours and has GPU quota limits
- Model weights (~4GB) are re-downloaded each Colab session since Drive mounting is unreliable on some networks
- Generation takes ~60 seconds per model on T4

---

## License

MIT
