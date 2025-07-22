import gradio as gr

def greet(name):
    return "hello!" + name

with gr.Blocks() as demo:
    name = gr.Text(label="input your name.")
    output = gr.Text(label="output")
    btn = gr.Button("greet")
    btn.click(
        fn = greet,
        inputs=name,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()