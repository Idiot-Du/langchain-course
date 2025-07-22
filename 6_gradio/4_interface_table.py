import gradio as gr

hello_world = gr.Interface(lambda name:"hello" + name,"text","text")
bye_world = gr.Interface(lambda name:"bye" + name,"text","text")

demo = gr.TabbedInterface([hello_world,bye_world],["打招呼!","再见!"])

if __name__ == "__main__":
    demo.launch()