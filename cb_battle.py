### TalkingToChatbots.com ###
### reddgr.com            ###

import tkinter as tk
from tkinter import ttk, Text, messagebox

class ChatbotRankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Chatbot Ranking Generator')
        
        self.chatbots = []
        
        # Text box for Chatbot Battle Title
        ttk.Label(root, text="Chatbot Battle Title:").grid(row=0, column=0)
        self.battle_title = ttk.Entry(root)
        self.battle_title.grid(row=0, column=1)
        
        # Create labels and entry fields for Chatbot details
        ttk.Label(root, text="Chatbot Name:").grid(row=1, column=0)
        self.chatbot_name = ttk.Entry(root)
        self.chatbot_name.grid(row=1, column=1)
        
        ttk.Label(root, text="Link:").grid(row=2, column=0)
        self.link = ttk.Entry(root)
        self.link.grid(row=2, column=1)
        
        self.scores = {}
        for idx, category in enumerate(["Specificity", "Coherency", "Brevity", "Novelty"], start=3):
            ttk.Label(root, text=f"{category}:").grid(row=idx, column=0)
            self.scores[category] = ttk.Combobox(root, values=[0, 1, 2, 3])
            self.scores[category].grid(row=idx, column=1)
        
        # Button to add chatbot details
        self.add_button = ttk.Button(root, text="Add Chatbot", command=self.add_chatbot)
        self.add_button.grid(row=7, column=0)
        
        # Button to generate HTML
        self.generate_button = ttk.Button(root, text="Generate HTML", command=self.generate_html)
        self.generate_button.grid(row=7, column=1)
        
        # Button to copy HTML to clipboard
        self.copy_button = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=8, column=0)
        
        # Button to clear the screen
        self.clear_button = ttk.Button(root, text="Clear Screen", command=self.clear_screen)
        self.clear_button.grid(row=8, column=1)
        
        # Text widget to display generated HTML
        self.html_output = Text(root, wrap='word')
        self.html_output.grid(row=9, column=0, columnspan=2, pady=20)

    def add_chatbot(self):
        # Retrieve values
        name = self.chatbot_name.get()
        link = self.link.get()
        scores = {category: int(self.scores[category].get()) for category in self.scores}
        self.chatbots.append({'name': name, 'link': link, 'scores': scores})

        # Clear input fields for next chatbot
        self.chatbot_name.delete(0, tk.END)
        self.link.delete(0, tk.END)
        for category in self.scores:
            self.scores[category].set('')

        messagebox.showinfo("Info", "Chatbot added successfully!")

    def generate_html(self):
        title = self.battle_title.get()
        
        # CSS Styles and Header
        header_html = f'''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap');

    h2 {{
        font-family: 'Josefin Sans', sans-serif;
        background-color: #c9c1f2; 
        padding: 10px;
    }}

    table {{
        border-collapse: collapse;
        width: 100%;
    }}

    th, td {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        white-space: nowrap; /* Prevent line breaks in cells by default */
    }}

    .breakable {{
        white-space: normal; /* Allow line breaks for the Chatbot column */
    }}

    th {{
        background-color: #c9c1f2;
    }}

    a {{
        color: #c171f4;
        text-decoration: none;
    }}

    a:hover {{
        text-decoration: underline;
    }}

    .table-container {{
        overflow-x: auto;
    }}

    @media (max-width: 768px) {{
        th, td {{
            padding: 4px;
        }}
    }}
</style>

<h2>Chatbot Battle: {title}</h2>

<div class="table-container">
    <table>
        <tr>
            <th class="breakable">Chatbot</th>
            <th>Rank (SCBN)</th>
            <th>Specificity</th>
            <th>Coherency</th>
            <th>Brevity</th>
            <th>Novelty</th>
            <th>Link</th>
        </tr>
'''

        # Sort chatbots based on score
        self.chatbots.sort(key=lambda x: sum(x['scores'].values()), reverse=True)

        # Adjust rankings for ties
        ranks = ["🥇 Winner", "🥈 Runner-up", "🥉 Contender"]
        previous_score = None
        rank_idx = 0
        
        chatbot_rows = ''
        for chatbot in self.chatbots:
            total_score = sum(chatbot['scores'].values())
            
            if total_score != previous_score:
                previous_score = total_score
                if rank_idx < len(ranks):
                    current_rank = ranks[rank_idx]
                    rank_idx += 1
                else:
                    current_rank = ""

            emoji_scores = {category: '🤖' * score + '🕹️' * (3-score) for category, score in chatbot['scores'].items()}
            
            chatbot_rows += f'''
<tr>
    <td class="breakable">{chatbot["name"]}</td>
    <td>{current_rank}</td>
    <td>{emoji_scores["Specificity"]}</td>
    <td>{emoji_scores["Coherency"]}</td>
    <td>{emoji_scores["Brevity"]}</td>
    <td>{emoji_scores["Novelty"]}</td>
    <td><a href="{chatbot["link"]}" target="_blank">View Chat</a></td>
</tr>
'''

        footer_html = "</table></div>"

        total_html = header_html + chatbot_rows + footer_html

        self.html_output.delete(1.0, tk.END)
        self.html_output.insert(tk.END, total_html)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.html_output.get(1.0, tk.END))
        messagebox.showinfo("Info", "HTML copied to clipboard!")

    def clear_screen(self):
        self.html_output.delete(1.0, tk.END)
        self.chatbots = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotRankingApp(root)
    root.mainloop()
