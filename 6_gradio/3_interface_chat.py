import gradio as gr
import random
import time
# def random_response(message,history):
#     return random.choice(["yes","no"])

# demo = gr.ChatInterface(random_response,title="随机回答机器人")

# if __name__ == "__main__":
#     demo.launch()

def slow_echo(message,history):
    for i in range(len(message)):
        time.sleep(0.1)
        yield "You typed:" + message[ : i+1]

demo = gr.ChatInterface(slow_echo,title="聊天机器人").queue()

if __name__ == "__main__":
    demo.launch()