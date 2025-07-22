import gradio as gr

def greet(name,is_morning,temperature):
    salutation = "Good Morning" if is_morning else "Good Evening"
    greeting = f"{salutation} {name}.It is {temperature} degrees today!"
    celsius = (temperature - 32) / 1.8
    return greeting,round(celsius,2)

theme = gr.themes.Soft(
    primary_hue="rose",
    text_size = "lg",
)
demo = gr.Interface(
    fn = greet,
    inputs = ["text","checkbox",gr.Slider(0,100)],
    outputs = ["text","number"],
    clear_btn="清除",
    submit_btn="送出",
    theme=theme
)

if __name__ == "__main__":
    demo.launch()