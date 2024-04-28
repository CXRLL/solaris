import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import wikipedia
import wolframalpha

# Configuration
WOLFRAM_APP_ID = 'R55QKE-PQ6GH3KYWG'

class ChatbotUI:
    def __init__(self, master):
        self.master = master
        master.title("AspireAI")

        self.chat_log = ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(master)
        self.msg_entry.pack(padx=10, pady=5, fill=tk.X)
        self.msg_entry.bind("<Return>", self.on_send)

        self.send_button = tk.Button(master, text="Send", command=self.on_send)
        self.send_button.pack(pady=5)

        self.wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)

    def on_send(self, event=None):
        user_query = self.msg_entry.get()
        if not user_query.strip():
            return

        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, "You: " + user_query + '\n\n')
        self.chat_log.config(state='disabled')

        self.msg_entry.delete(0, tk.END)

        answer = self.get_answer(user_query)
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, "AspireAI: " + answer + '\n\n')
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

    def get_answer(self, query):
        try:
            # Try Wolfram Alpha first
            res = self.wolfram_client.query(query)
            answer = next(res.results).text
            return answer
        except Exception as e:
            # Fallback to Wikipedia
            try:
                wikipedia.set_lang("en")
                answer = wikipedia.summary(query, sentences=2)
                return answer
            except Exception as e:
                return "Sorry, I cannot do this. I am stil in development"

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()
