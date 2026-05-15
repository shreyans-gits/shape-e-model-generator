import torch

from loader import load_models
from sampler import sample
from exporter import export

def generate(prompt, output_path, format='glb', guidance_scale=3.0, steps=64):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    print("Initializing models and diffusion...")
    xm, model, diffusion = load_models(device)

    print(f"Sampling latents for: '{prompt}'...")
    latents = sample(
        prompt=prompt,
        model=model,
        diffusion=diffusion,
        batch_size=1,
        guidance_scale=guidance_scale,
        steps=steps
    )

    print(f"Converting latents and exporting to {format.upper()}...")
    export(
        latents=latents,
        xm=xm,
        output_path=output_path,
        format=format
    )

    print(f"Process complete. File saved to: {output_path}.{format}")
