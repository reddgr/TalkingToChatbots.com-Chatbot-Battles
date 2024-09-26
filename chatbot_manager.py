class ChatbotManager:
    def __init__(self):
        self.chatbots = []

    def add_chatbot(self, name, link, scores):
        self.chatbots.append({'name': name, 'link': link, 'scores': scores})

    def generate_html(self, title):
        header_html = f'''
        <h2>Chatbot Battle: {title}</h2>
        <table border="1">
            <tr>
                <th>Chatbot</th>
                <th>Rank (SCBN)</th>
                <th>Specificity</th>
                <th>Coherency</th>
                <th>Brevity</th>
                <th>Novelty</th>
                <th>Link</th>
            </tr>
        '''
        # Sort chatbots based on total score
        sorted_chatbots = sorted(self.chatbots, key=lambda x: sum(x['scores'].values()), reverse=True)
        
        # Prepare rankings
        ranks = ["🥇 Winner", "🥈 Runner-up", "🥉 Contender"]
        previous_score = None
        rank_idx = 0

        chatbot_rows = ""
        for chatbot in sorted_chatbots:
            total_score = sum(chatbot['scores'].values())
            if total_score != previous_score:
                previous_score = total_score
                if rank_idx < len(ranks):
                    chatbot['rank'] = ranks[rank_idx]
                    rank_idx += 1
                else:
                    chatbot['rank'] = ""

            emoji_scores = {category: '🤖' * score + '🕹️' * (3 - score) for category, score in chatbot['scores'].items()}
            
            chatbot_rows += f'''
            <tr>
                <td>{chatbot["name"]}</td>
                <td>{chatbot.get('rank', '')}</td>
                <td>{emoji_scores["Specificity"]}</td>
                <td>{emoji_scores["Coherency"]}</td>
                <td>{emoji_scores["Brevity"]}</td>
                <td>{emoji_scores["Novelty"]}</td>
                <td><a href="{chatbot["link"]}" target="_blank">View Chat</a></td>
            </tr>
            '''
        
        footer_html = "</table>"
        return header_html + chatbot_rows + footer_html