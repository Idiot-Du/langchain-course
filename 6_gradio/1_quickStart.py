import gradio as gr

def greet(name,intensity):
    return "hello," + name + "？"*int(intensity)
my_demo = gr.Interface(
    fn=greet,
    inputs=["text","slider"],
    outputs=["text"]
)
my_demo.launch()
# 使用该命令：gradio 6_gradio/1_quickStart.py --demo-name=my_demo 可以避免每次调试的时候重新运行的步骤