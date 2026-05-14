import os
from shap_e.util.notebooks import decode_latent_mesh

def export(latents, xm, output_path, format):
    format = format.lower()
    if format not in ['obj', 'glb']:
        raise ValueError("Unsupported format. Please use 'obj' or 'glb'.")
    
    for i, latent in enumerate(latents):
        mesh = decode_latent_mesh(xm, latent).tri_mesh()
        
        file_name = f"{output_path}_{i}.{format}"
        mode = 'w' if format == 'obj' else 'wb'
        
        with open(file_name, mode) as f:
            if format == 'obj':
                mesh.write_obj(f)
            elif format == 'glb':
                mesh.write_glb(f)
        
        print(f"Exported {format} mesh to {file_name}")