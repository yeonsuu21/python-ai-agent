import { useState } from "react";
import "./App.css";

type Message = {
  role: "user" | "assistant";
  content: string;
};

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "안녕하세요! 👋\n공연 일정 조회와 업무 자동화를 도와드릴게요.",
    },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) {
      return;
    }

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: message,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      });

      if (!response.ok) {
        throw new Error("Agent API 요청에 실패했습니다.");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.result,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "요청을 처리하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <header className="chat-header">
          <div className="agent-icon">AI</div>

          <div>
            <h1>AI 업무 Agent</h1>
            <p>
              <span className="status-dot" />
              Online
            </p>
          </div>
        </header>

        <main className="chat-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.role}`}
            >
              {message.role === "assistant" && (
                <div className="message-avatar">AI</div>
              )}

              <div className={`message ${message.role}`}>
                {message.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="message-avatar">AI</div>

              <div className="message assistant loading-message">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}
        </main>

        <footer className="chat-input-area">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Agent에게 업무를 요청해보세요..."
            disabled={loading}
          />

          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
          >
            전송
          </button>
        </footer>
      </div>
    </div>
  );
}

export default App;