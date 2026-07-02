from flask import Flask, jsonify, request, render_template_string, redirect, url_for
from chat_backend import handle_chat_request
from auth import get_current_user, login_user, logout_user
from document_utils import build_context_with_document, extract_text_from_upload

app = Flask(__name__)
app.secret_key = "super-secret-key"

HTML_PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Chat App</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; }
    .app { max-width: 900px; margin: 0 auto; padding: 24px; }
    .card { background: #111827; border: 1px solid #334155; border-radius: 16px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }
    h1 { margin-top: 0; }
    #messages { min-height: 380px; max-height: 560px; overflow-y: auto; padding: 12px; background: #020617; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 12px; }
    .msg { margin: 10px 0; padding: 10px 12px; border-radius: 10px; }
    .user { background: #2563eb; margin-left: 40px; }
    .bot { background: #1f2937; margin-right: 40px; }
    .msg-content p { margin: 0 0 8px; }
    .msg-content code { background: #0f172a; padding: 2px 4px; border-radius: 4px; }
    .msg-content pre { background: #0f172a; padding: 10px; border-radius: 6px; overflow-x: auto; }
    .msg-content ul, .msg-content ol { margin: 6px 0 6px 20px; }
    .msg-content strong { font-weight: 700; }
    .composer { display: flex; gap: 10px; }
    input { flex: 1; padding: 12px; border-radius: 10px; border: 1px solid #475569; background: #0f172a; color: #fff; }
    button { padding: 12px 16px; border: none; border-radius: 10px; background: #8b5cf6; color: white; cursor: pointer; }
    button:hover { background: #7c3aed; }
    .hint { color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px; }
    .auth-bar { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 12px; }
    .auth-bar a { color: #cbd5e1; text-decoration: none; }
    .login-form { display: flex; gap: 8px; }
    .login-form input { padding: 8px 10px; border-radius: 8px; }
    .suggestions { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
    .chip { background: #1f2937; border: 1px solid #374151; border-radius: 999px; padding: 7px 10px; cursor: pointer; color: #cbd5e1; font-size: 0.9rem; }
    .chip:hover { background: #334155; }
    .loading { color: #94a3b8; font-style: italic; }
    .typing-dots { display: inline-flex; gap: 4px; }
    .typing-dots span { width: 6px; height: 6px; background: #94a3b8; border-radius: 50%; animation: bounce 1.2s infinite ease-in-out; }
    .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
    .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
      0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
      40% { transform: translateY(-4px); opacity: 1; }
    }
  </style>
</head>
<body>
  <div class="app">
    <div class="card">
      <h1>AI Chat App</h1>
      <div class="hint">{{ welcome_text }}</div>
      <div class="auth-bar">
        {% if username %}
          <span>Signed in as {{ username }}</span>
          <a href="/logout">Logout</a>
        {% else %}
          <form action="/login" method="post" class="login-form">
            <input name="username" placeholder="Enter your name" required />
            <button type="submit">Login</button>
          </form>
        {% endif %}
      </div>
      <div class="suggestions">
        <span class="chip" onclick="usePrompt('Explain quantum computing in simple terms')">Explain quantum computing</span>
        <span class="chip" onclick="usePrompt('Summarize the benefits of exercise')">Summarize benefits of exercise</span>
        <span class="chip" onclick="usePrompt('Help me write a short email')">Write a short email</span>
      </div>
      <div id="messages"></div>
      <form id="chat-form" class="composer" enctype="multipart/form-data">
        <input id="message" name="message" placeholder="Ask anything..." />
        <input id="file" name="file" type="file" accept=".pdf,.docx" />
        <button type="submit">Send</button>
      </form>
    </div>
  </div>
  <script>
    const sessionId = 'guest-session';

    function escapeHtml(text) {
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function renderMarkdown(text) {
      const escaped = escapeHtml(text);
      const withCode = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
      const withBold = withCode.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      const withBreaks = withBold.replace(/\n/g, '<br>');
      return withBreaks;
    }

    function appendMessage(role, content) {
      const messages = document.getElementById('messages');
      const wrapper = document.createElement('div');
      wrapper.className = 'msg ' + (role === 'user' ? 'user' : 'bot');
      const label = role === 'user' ? 'You' : 'AI';
      const contentDiv = document.createElement('div');
      contentDiv.className = 'msg-content';
      contentDiv.innerHTML = `<strong>${label}:</strong> ${renderMarkdown(content)}`;
      wrapper.appendChild(contentDiv);
      messages.appendChild(wrapper);
      messages.scrollTop = messages.scrollHeight;
    }

    function usePrompt(text) {
      document.getElementById('message').value = text;
      document.getElementById('message').focus();
    }

    async function sendMessage(event) {
      if (event) event.preventDefault();
      const input = document.getElementById('message');
      const fileInput = document.getElementById('file');
      const text = input.value.trim();
      if (!text && !fileInput.files.length) return;

      appendMessage('user', text || (fileInput.files[0] ? '[Uploaded document]' : ''));
      input.value = '';
      fileInput.value = '';
      const loading = document.createElement('div');
      loading.className = 'msg bot loading';
      loading.innerHTML = '<strong>AI:</strong> <span class="typing-dots"><span></span><span></span><span></span></span>';
      document.getElementById('messages').appendChild(loading);

      const formData = new FormData();
      formData.append('message', text);
      formData.append('session_id', sessionId);
      if (fileInput.files.length) {
        formData.append('file', fileInput.files[0]);
      }

      const response = await fetch('/api/chat', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      document.getElementById('messages').removeChild(loading);
      appendMessage('assistant', data.reply);
    }

    document.getElementById('chat-form').addEventListener('submit', sendMessage);
    document.getElementById('message').addEventListener('keydown', function (event) {
      if (event.key === 'Enter') sendMessage(event);
    });
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    username = get_current_user()
    welcome_text = f"Welcome, {username}!" if username else "Sign in to save your own chat history."
    return render_template_string(HTML_PAGE, username=username, welcome_text=welcome_text)


@app.post("/login")
def login():
    username = (request.form.get("username") or "").strip()
    if username:
        login_user(username)
    return redirect(url_for("index"))


@app.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.post("/api/chat")
def chat():
    message = request.form.get("message", "")
    session_id = request.form.get("session_id") or "default"
    username = get_current_user()
    if username:
        session_id = f"user:{username}"

    document_text = ""
    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename:
        document_text = extract_text_from_upload(uploaded_file)

    payload = {"message": message, "session_id": session_id}
    if document_text:
        payload["document_text"] = document_text

    result = handle_chat_request(payload)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
