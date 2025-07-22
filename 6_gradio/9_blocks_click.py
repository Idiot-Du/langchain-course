import gradio as gr

def say_hi(name):
    return "hello!" + name
def say_no(name):
    return "no!" + name
with gr.Blocks() as demo:
    inp = gr.Text(label="请输入你的姓名")
    otp1 = gr.Text(label="打招呼")
    otp2 = gr.Text(label="不打招呼")

    btn_hi = gr.Button("打招呼")
    btn_no = gr.Button("不打招呼")

    btn_hi.click(
        fn = say_hi,
        inputs = inp,
        outputs = otp1
    )
    btn_no.click(
        fn = say_no,
        inputs = inp,
        outputs = otp2
    )

if __name__ == "__main__":
    demo.launch()