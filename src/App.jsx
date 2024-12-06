import React, { useState, useEffect, useRef } from "react";

const App = () => {
  const [messages, setMessages] = useState([
    {
      sender: "Expert 1",
      text: "One effective strategy to prevent school bullying is implementing comprehensive anti-bullying policies that are clearly communicated to students, parents, and staff. This ensures everyone understands what constitutes bullying and the consequences of such behavior.",
    },
    {
      sender: "Expert 2",
      text: "I agree. Additionally, schools should provide regular training for teachers to recognize and intervene in bullying situations effectively. Educators equipped with the right tools can make a significant difference.",
    },
  ]);

  const [isFetching, setIsFetching] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [mode, setMode] = useState("experts");
  const [showModal, setShowModal] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchNextMessage = async (currentHistory) => {
    if (isFetching) return;
    setIsFetching(true);

    try {
      const response = await fetch("https://backend2202.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ history: currentHistory, mode }),
      });

      if (!response.ok) {
        console.error(`Server error: ${response.status}`);
        throw new Error("Failed to fetch message from the backend.");
      }

      const data = await response.json();

      if (data.response) {
        const [speaker, ...messageParts] = data.response.split(":");
        const message = messageParts.join(":").trim();

        setMessages((prev) => [
          ...prev,
          { sender: speaker.trim(), text: message },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { sender: "Error", text: "No response from backend." },
        ]);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "Error", text: "Failed to fetch message. Try again later." },
      ]);
    } finally {
      setIsFetching(false);
    }
  };

  const handleSendMessage = () => {
    if (inputValue.trim() === "") return;

    const sender = "Expert 2";
    const newMessage = { sender, text: inputValue };
    const updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);

    const newHistory = updatedMessages
      .map((msg) => `${msg.sender}: ${msg.text}`)
      .join("\n");

    if (mode === "expert2") {
      fetchNextMessage(newHistory);
    }

    setInputValue("");
  };

  useEffect(() => {
    if (!showModal && mode === "experts") {
      const interval = setInterval(() => {
        const currentHistory = messages
          .map((msg) => `${msg.sender}: ${msg.text}`)
          .join("\n");
        fetchNextMessage(currentHistory);
      }, 5000);

      return () => clearInterval(interval);
    }
  }, [mode, showModal, messages]);

  const toggleMode = () => {
    setMode((prevMode) => (prevMode === "experts" ? "expert2" : "experts"));
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-11/12 max-w-md relative">
            <button
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-200"
              onClick={() => setShowModal(false)}
            >
              &times;
            </button>
            <h2 className="text-2xl font-bold mb-4">Welcome!</h2>
            <p className="mb-6">
              This application features an AI-generated conversation between
              experts discussing strategies to prevent bullying. We've initiated
              the chat with two default messages to set the stage. You have the
              option to let the AI experts continue the discussion or to join in
              yourself. Simply use the toggle to switch modes. If you choose to
              participate, you'll become <strong>Expert 2</strong>!
            </p>
            <button
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 w-full"
              onClick={() => setShowModal(false)}
            >
              OK
            </button>
          </div>
        </div>
      )}

      <div className="flex flex-col w-[90%] max-w-4xl h-[80%] max-h-screen bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Dr. Yimin Yang GPT</h1>
          <button
            onClick={toggleMode}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            {mode === "experts"
              ? "Switch to Expert Interaction"
              : "Switch to Expert Mode"}
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 border border-gray-700 rounded-lg">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.sender === "Expert 1"
                  ? "justify-start items-start"
                  : "justify-end items-end"
              } my-3`}
            >
              {msg.sender === "Expert 1" && (
                <img
                  src="/src/assets/prof.JPG"
                  alt="Expert 1"
                  className="w-10 h-10 rounded-full mr-2"
                />
              )}
              <div
                className={`px-4 py-2 rounded-lg text-sm ${
                  msg.sender === "Expert 1"
                    ? "bg-blue-600 text-white"
                    : "bg-green-600 text-white"
                }`}
              >
                <strong>{msg.sender}: </strong>
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {mode === "expert2" && (
          <div className="mt-4 flex items-center">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message here..."
              className="flex-1 px-4 py-2 rounded-l-lg bg-gray-700 text-white border border-gray-600 focus:outline-none"
              onKeyDown={handleKeyDown}
            />
            <button
              onClick={handleSendMessage}
              disabled={isFetching}
              className="px-4 py-2 rounded-r-lg bg-blue-600 text-white border border-blue-500 hover:bg-blue-700 focus:outline-none disabled:opacity-50"
            >
              Send
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;