import gradio as gr

with gr.Blocks() as demo:
    with gr.Tab("AAA"):
        with gr.Tab("tab1"):
            with gr.Row():
                gr.Text()
                gr.Text()
                with gr.Row():
                    gr.Text()
                    gr.Text()
        with gr.Tab("tab2"):
            with gr.Row():
                gr.Text()
                gr.Text()
                with gr.Row():
                    gr.Text()
                    gr.Text()

            with gr.Row():
                gr.Text()
                gr.Text()
    with gr.Tab("BBB"):
        with gr.Tab("tab1"):
            with gr.Row():
                gr.Text()
                gr.Text()
                with gr.Row():
                    gr.Text()
                    gr.Text()
        with gr.Tab("tab2"):
            with gr.Row():
                gr.Text()
                gr.Text()
                with gr.Row():
                    gr.Text()
                    gr.Text()

            with gr.Row():
                gr.Text()
                gr.Text()

if __name__ == "__main__":
    demo.launch()
