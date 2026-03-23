from flask import Flask, request, abort

app = Flask(__name__)

# list of AI crawlers SEO tools and aggressive scrapers
BANNED_BOTS = [
    'GPTBot', 'OAI-SearchBot', 'ChatGPT-User',
    'ClaudeBot', 'Claude-Web',
    'Meta-ExternalAgent',
    'Google-Extended',
    'Applebot-Extended',
    'PerplexityBot', 'Amazonbot', 'Bytespider',
    'AhrefsBot', 'SemrushBot', 'DotBot', 'MJ12bot', 'Rogerbot',
    'CCBot', 'Diffbot', 'ImagesiftBot'
]


@app.before_request
def block_bots():
    """
    This function runs before every request to the server.
    It checks the User-Agent header to identify and block bots.
    """
    # get the User-Agent header from the incoming request
    user_agent = request.headers.get('User-Agent', '').lower()

    # check if any banned bot name exists in the current User-Agent
    for bot in BANNED_BOTS:
        if bot.lower() in user_agent:
            return "Access Denied", 403
    return None


@app.route('/welcome-in')
def web_to_me():
    return "Welcome to the secured welcome-in page!"


@app.route('/runners-world/')
def go_in():
    return "Welcome to runners-world!"


@app.route('/')
def home():
    return "Home Page."


if __name__ == '__main__':
    app.run(debug=True)