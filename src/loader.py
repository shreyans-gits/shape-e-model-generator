import torch
from shap_e.models.download import load_model, load_config
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config


def load_models(device):
    transmitter = load_model('transmitter', device=device)
    text300M = load_model('text300M', device=device)    
    diffusion_config = load_config('diffusion')
    diffusion = diffusion_from_config(diffusion_config)
    return transmitter, text300M, diffusion