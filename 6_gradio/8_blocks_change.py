import gradio as gr
def say_hi(name):
    return "hello!" + name

with gr.Blocks() as demo:
    inp = gr.Radio(["cat","dog","pig"])
    otp = gr.Text(label="结果为")
    inp.change(say_hi,inp,otp)

if __name__ == "__main__":
    demo.launch()
