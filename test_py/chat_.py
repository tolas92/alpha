from ollama import chat
import ollama




class Ai():

 def load_ai(self):
      ollama.pull('gorilla')

     
 def talk_(self):   
    messages = [
    {
        'role': 'user',
        'content':"move the robot to the kitchen"
    },
    ]

    stream = ollama.chat(
    model='tinyllama',
    messages=[{'role': 'user', 'content': why }],
    stream=True,
)

    
    for chunk in stream:
     print(chunk['message']['content'], end='', flush=True)
 

def main():
    ai=Ai()
   # ai.load_ai()
    print('done')
    ai.talk_()

if __name__ == "__main__":
    main()
   

