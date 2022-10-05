import gradio as gr
import json5 as json
from glob import glob
from time import sleep
import os
import shutil


def generate(text, h, w):
    with open('settings.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    f.close()
    data['prompt'] = text
    data["batch_name"] = 'gradio'
    data["height"] = int(h)
    data["width"] = int(w)
    with open('gradio_settings.json', 'w+', encoding='utf8') as f:
        json.dump(data, f, indent=4)
    f.close()
    shutil.copy('gradio_settings.json', 'job_cuda_0.json')
    list_of_files = glob('out/gradio/*.png') # * means all if need specific format then *png
    latest_png = max(list_of_files, key=os.path.getctime)
    while latest_png == max(list_of_files, key=os.path.getctime):
        list_of_files = glob('out/gradio/*.png')
        print('waiting')
        sleep(5)
    latest_png = max(list_of_files, key=os.path.getctime)
    return latest_png

with gr.Blocks() as demo:
    gr.Markdown("VisualDiffusion by KnoBuddy")
    with gr.Tab("Txt2Img"):
        with gr.Row():
            with gr.Column():
                prompt_text = gr.Textbox("Text", lines=3, placeholder="Text to generate image from")
                h = gr.Slider(64, 704, 512, step=64, label="Height")
                w = gr.Slider(64, 704, 512, step=64, label="Width")
            with gr.Column():
                image_output = gr.Image(height=h, width=w, label="Image")
    generate_btn = gr.Button(label="Generate")
    
    generate_btn.click(generate, inputs=[prompt_text, h, w], outputs=image_output)

demo.launch(share=True, auth=['admin', 'password'], show_api=False)
