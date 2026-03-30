---
title: "Build an AI Image Generation App with Flux: Complete Tutorial"
excerpt: "Flux is the hottest open-source image model in 2026. This tutorial walks you through building a full image generation web app from setup to deployment."
category: "Tutorials"
categorySlug: "tutorials"
image: "/images/build-ai-image-app-with-flux.webp"
date: "2026-03-30"
readTime: "15 min read"
author: "EgoistAI"
featured: false
tags: ["flux", "image generation", "python", "web app", "tutorial"]
sources:
  - name: "Black Forest Labs - Flux"
    url: "https://blackforestlabs.ai"
  - name: "Replicate - Flux API"
    url: "https://replicate.com/black-forest-labs"
  - name: "Hugging Face Diffusers Documentation"
    url: "https://huggingface.co/docs/diffusers"
  - name: "Gradio Documentation"
    url: "https://www.gradio.app/docs"
  - name: "FastAPI Documentation"
    url: "https://fastapi.tiangolo.com"
---

Flux, developed by Black Forest Labs (the team behind Stable Diffusion), has become the go-to open-source image generation model in 2026. It produces images that rival Midjourney in quality, runs on consumer GPUs, and — critically — is available under open licenses that let you build commercial products without worrying about usage restrictions.

This tutorial takes you from zero to a deployed web application that generates images using Flux. We'll cover two approaches: running Flux locally with a GPU, and using the Replicate API for cloud-based generation. By the end, you'll have a working app you can customize, extend, and deploy.

## What Is Flux and Why Should You Use It?

Flux is a family of text-to-image models from Black Forest Labs:

| Model | Parameters | Quality | Speed | License | GPU Requirement |
|-------|-----------|---------|-------|---------|----------------|
| **Flux.1 [pro]** | Undisclosed | Excellent | Fast | API only | Cloud (via API) |
| **Flux.1 [dev]** | 12B | Excellent | Medium | Open (non-commercial) | 24GB+ VRAM |
| **Flux.1 [schnell]** | 12B | Very Good | Fast | Apache 2.0 | 12GB+ VRAM |

**Flux.1 [schnell]** is the most practical for building applications — it's Apache 2.0 licensed (fully commercial use), fast (generates images in 1-4 seconds on an RTX 4090), and produces quality that's a significant step above Stable Diffusion XL.

**Flux.1 [dev]** is higher quality but restricted to non-commercial use and requires more VRAM. It's great for personal projects and experimentation.

**Flux.1 [pro]** is the highest quality variant, available only through the API (not downloadable). Best for production applications where you want maximum quality and don't mind API costs.

## Approach 1: Cloud-Based App with Replicate API

If you don't have a GPU (or want to build something deployable without managing GPU infrastructure), the Replicate API is the fastest path to a working app.

### Prerequisites

- Python 3.9+
- A Replicate account (free to sign up, pay-per-use for generation)
- Basic familiarity with Python and web frameworks

### Step 1: Set Up Your Project

```bash
mkdir flux-image-app && cd flux-image-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install replicate gradio python-dotenv Pillow
```

Create a `.env` file:
```
REPLICATE_API_TOKEN=r8_your_token_here
```

Get your API token from [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens).

### Step 2: Build the Core Generation Function

Create `app.py`:

```python
import replicate
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

load_dotenv()

def generate_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    num_inference_steps: int = 4,
    guidance_scale: float = 3.5,
    model: str = "schnell"
) -> Image.Image:
    """Generate an image using Flux via Replicate API."""

    model_map = {
        "schnell": "black-forest-labs/flux-schnell",
        "dev": "black-forest-labs/flux-dev",
        "pro": "black-forest-labs/flux-1.1-pro",
    }

    output = replicate.run(
        model_map[model],
        input={
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "output_format": "png",
        }
    )

    # Replicate returns a URL (or list of URLs)
    image_url = output[0] if isinstance(output, list) else output
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    return image
```

### Step 3: Build the Web Interface with Gradio

Add the Gradio interface to `app.py`:

```python
import gradio as gr

def generate_ui(prompt, width, height, steps, guidance, model_choice):
    """Gradio wrapper for image generation."""
    if not prompt.strip():
        return None

    image = generate_image(
        prompt=prompt,
        width=int(width),
        height=int(height),
        num_inference_steps=int(steps),
        guidance_scale=float(guidance),
        model=model_choice,
    )
    return image

# Build the interface
with gr.Blocks(title="Flux Image Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Flux Image Generator")
    gr.Markdown("Generate images using Black Forest Labs' Flux models.")

    with gr.Row():
        with gr.Column(scale=1):
            prompt_input = gr.Textbox(
                label="Prompt",
                placeholder="A cyberpunk city at sunset, neon signs reflecting in rain puddles...",
                lines=3,
            )

            with gr.Row():
                width_input = gr.Slider(
                    minimum=512, maximum=1536, value=1024,
                    step=64, label="Width"
                )
                height_input = gr.Slider(
                    minimum=512, maximum=1536, value=1024,
                    step=64, label="Height"
                )

            with gr.Row():
                steps_input = gr.Slider(
                    minimum=1, maximum=50, value=4,
                    step=1, label="Inference Steps"
                )
                guidance_input = gr.Slider(
                    minimum=1.0, maximum=20.0, value=3.5,
                    step=0.5, label="Guidance Scale"
                )

            model_input = gr.Dropdown(
                choices=["schnell", "dev", "pro"],
                value="schnell",
                label="Model"
            )

            generate_btn = gr.Button("Generate", variant="primary")

        with gr.Column(scale=1):
            output_image = gr.Image(label="Generated Image", type="pil")

    generate_btn.click(
        fn=generate_ui,
        inputs=[prompt_input, width_input, height_input,
                steps_input, guidance_input, model_input],
        outputs=output_image,
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
```

### Step 4: Run It

```bash
python app.py
```

Open `http://localhost:7860` in your browser. You now have a working AI image generation app. Type a prompt, hit generate, and watch Flux work.

**Replicate pricing:** Flux Schnell runs at approximately $0.003 per image. Flux Dev at $0.03 per image. Flux Pro at $0.05 per image. For development and moderate usage, costs are trivial.

## Approach 2: Local Generation with GPU

If you have an NVIDIA GPU with 12GB+ VRAM (RTX 3060 or better), you can run Flux locally with zero API costs.

### Step 1: Set Up the Environment

```bash
mkdir flux-local && cd flux-local
python -m venv venv
source venv/bin/activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate safetensors sentencepiece gradio
```

### Step 2: Build the Local Generation Function

Create `app_local.py`:

```python
import torch
from diffusers import FluxPipeline
from PIL import Image

# Load model (this downloads ~24GB on first run)
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")

# Enable memory optimizations for consumer GPUs
pipe.enable_model_cpu_offload()  # Offloads to CPU when not in use
# pipe.enable_sequential_cpu_offload()  # More aggressive, for <12GB VRAM


def generate_image_local(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    num_inference_steps: int = 4,
    guidance_scale: float = 0.0,  # Schnell uses 0.0 guidance
) -> Image.Image:
    """Generate an image using local Flux model."""

    with torch.inference_mode():
        result = pipe(
            prompt=prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=torch.Generator("cuda").manual_seed(
                torch.randint(0, 2**32, (1,)).item()
            ),
        )

    return result.images[0]
```

### Step 3: Add the Gradio Interface

The Gradio interface code is nearly identical to the API version — just swap `generate_image` for `generate_image_local` and remove the model selector (since you're running Schnell locally):

```python
import gradio as gr

def generate_ui(prompt, width, height, steps, seed):
    if not prompt.strip():
        return None

    image = generate_image_local(
        prompt=prompt,
        width=int(width),
        height=int(height),
        num_inference_steps=int(steps),
    )
    return image

with gr.Blocks(title="Flux Local Generator") as demo:
    gr.Markdown("# Flux Image Generator (Local)")

    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(label="Prompt", lines=3)
            with gr.Row():
                width = gr.Slider(512, 1536, 1024, step=64, label="Width")
                height = gr.Slider(512, 1536, 1024, step=64, label="Height")
            steps = gr.Slider(1, 8, 4, step=1, label="Steps")
            seed = gr.Number(label="Seed (0 = random)", value=0)
            btn = gr.Button("Generate", variant="primary")

        with gr.Column():
            output = gr.Image(label="Result", type="pil")

    btn.click(generate_ui, [prompt, width, height, steps, seed], output)

demo.launch(server_name="0.0.0.0", server_port=7860)
```

### Performance Expectations

| GPU | Flux Schnell (4 steps, 1024x1024) |
|-----|-----------------------------------|
| RTX 4090 (24GB) | ~1.5 seconds |
| RTX 4080 (16GB) | ~3 seconds |
| RTX 3090 (24GB) | ~4 seconds |
| RTX 3060 (12GB) | ~8 seconds (with CPU offload) |

## Building a Production API with FastAPI

For a real application, you'll want an API endpoint that other services can call. Here's a FastAPI implementation:

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from io import BytesIO
import replicate
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Flux Image API")

class GenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    width: int = Field(default=1024, ge=512, le=1536)
    height: int = Field(default=1024, ge=512, le=1536)
    num_inference_steps: int = Field(default=4, ge=1, le=50)
    model: str = Field(default="schnell")

@app.post("/generate")
async def generate(request: GenerationRequest):
    try:
        model_map = {
            "schnell": "black-forest-labs/flux-schnell",
            "dev": "black-forest-labs/flux-dev",
            "pro": "black-forest-labs/flux-1.1-pro",
        }

        if request.model not in model_map:
            raise HTTPException(400, f"Invalid model: {request.model}")

        output = replicate.run(
            model_map[request.model],
            input={
                "prompt": request.prompt,
                "width": request.width,
                "height": request.height,
                "num_inference_steps": request.num_inference_steps,
                "output_format": "png",
            }
        )

        image_url = output[0] if isinstance(output, list) else output

        import requests
        response = requests.get(image_url)
        return StreamingResponse(
            BytesIO(response.content),
            media_type="image/png"
        )

    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
```

Run with:
```bash
pip install fastapi uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000
```

Test with:
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a serene mountain lake at dawn"}' \
  --output test.png
```

## Deploying to Production

### Option 1: Deploy on Railway or Render

Both platforms support Python apps with minimal configuration. Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Push to GitHub and connect to Railway/Render for automatic deployments.

### Option 2: Deploy on Hugging Face Spaces

For the Gradio version, Hugging Face Spaces offers free hosting:

1. Create a new Space on huggingface.co
2. Choose Gradio as the SDK
3. Push your `app.py` and `requirements.txt`
4. Set your `REPLICATE_API_TOKEN` as a Space Secret

Your app will be live at `https://huggingface.co/spaces/your-username/your-app`.

## Prompt Engineering Tips for Flux

Flux responds well to detailed, descriptive prompts. Some tips:

**Be specific about style:** Instead of "a cat," write "a ginger tabby cat sitting on a vintage leather armchair, warm afternoon light streaming through venetian blinds, shot on 35mm film, shallow depth of field."

**Specify technical parameters:** Flux understands photography terms — "macro photography," "wide-angle lens," "golden hour lighting," "studio lighting with softbox" all produce relevant results.

**Quality modifiers that work:** "highly detailed," "professional photography," "award-winning," "8K resolution" — these cliches actually affect Flux's output positively.

**Negative prompting:** Flux Schnell doesn't use negative prompts (it's a rectified flow model). If you want to avoid certain elements, focus on describing what you DO want rather than what you don't.

## FAQ: Building with Flux

### Is Flux really free to use commercially?

Flux.1 Schnell is Apache 2.0 licensed — fully open for commercial use, modification, and redistribution. Flux.1 Dev has a non-commercial license. Flux.1 Pro is commercial but API-only (pay per use). For commercial applications, use Schnell locally or Pro via API.

### How does Flux compare to Midjourney and DALL-E 3?

Flux Pro and Dev produce images on par with Midjourney v6 for most prompts. Flux Schnell is slightly below Midjourney quality but significantly faster. DALL-E 3 is generally considered below Flux in image quality and flexibility but better at text rendering within images. The key advantage of Flux: you can run it locally with no API dependency.

### Can Flux generate text in images?

Flux has improved text rendering compared to earlier diffusion models but it's still inconsistent. Short text (1-3 words) works reasonably well. Longer text or specific fonts are unreliable. For applications that require accurate text in images, generate the image with Flux and add text in a post-processing step.

### How much does it cost to run Flux in production?

Via Replicate API: ~$0.003-0.05 per image depending on the model. For 10,000 images/month on Schnell, that's about $30. Locally on your own GPU: electricity cost only (negligible). On a cloud GPU (Lambda, RunPod): $0.50-1.50/hour for an A100, generating hundreds of images per hour.

### Can I fine-tune Flux on my own images?

Yes. Flux supports LoRA fine-tuning similar to Stable Diffusion. You can train custom styles, characters, or concepts with as few as 20-30 images. Tools like Kohya's sd-scripts and the Hugging Face Diffusers library both support Flux LoRA training. Expect 1-2 hours of training on a single GPU for a basic LoRA.

## The Bottom Line

Flux has made professional-quality image generation accessible to anyone who can write a Python script. The combination of open licensing, strong quality, and reasonable hardware requirements means you can build commercial image generation products without depending on any external API — though the API option exists for those who prefer it.

The app we built in this tutorial is a starting point. From here, you can add user authentication, image history, prompt templates, style presets, batch generation, or integrate it into a larger product. The hard part — getting high-quality image generation working — is solved. The rest is product development.

Build something. The tools are ready.
