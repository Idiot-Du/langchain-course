import gradio as gr

# with gr.Blocks() as demo:
#     with gr.Row(equal_height=True):
#         gr.Text(scale=1)
#         gr.TextArea()
#         gr.Audio()

with gr.Blocks(fill_height=True,fill_width=True) as demo:
    gr.Chatbot(scale=1)

    gr.Text()

if __name__ == "__main__":
    demo.launch()