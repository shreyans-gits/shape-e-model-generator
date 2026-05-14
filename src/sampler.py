from shap_e.diffusion.sample import sample_latents

def sample(prompt, model, diffusion, batch_size, guidance_scale, steps):
    """Runs the diffusion loop to generate 3D latents."""
    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=steps,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )
    return latents