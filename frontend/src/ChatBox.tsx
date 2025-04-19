import React, { useState } from 'react';
import axios from 'axios';

interface Message {
  type: 'user' | 'bot';
  text: string;
  showFeedback?: boolean;
  userQuery?: string;
  matchedQuestion?: string;
  answer?: string;
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { type: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post('http://localhost:8000/ask', {
        question: input,
      });

      const { answer, matched_question, found } = response.data;

      const botMessage: Message = {
        type: 'bot',
        text: found
          ? answer
          : "We couldn't find an answer to your question. It has been logged for review.",
        showFeedback: found,
        userQuery: input,
        matchedQuestion: matched_question,
        answer: answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: 'bot', text: 'Sorry, something went wrong!' },
      ]);
    }

    setInput('');
  };

  const submitFeedback = async (
    feedback: 'yes' | 'no',
    message: Message
  ) => {
    try {
      await axios.post('http://localhost:8000/feedback', {
        user_query: message.userQuery,
        matched_question: message.matchedQuestion,
        answer: message.answer,
        feedback,
      });

      setMessages((prev) =>
        prev.map((msg) =>
          msg === message ? { ...msg, showFeedback: false } : msg
        )
      );
    } catch (err) {
      console.error('Feedback failed', err);
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow h-[70vh] overflow-y-auto">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-3 text-${msg.type === 'user' ? 'right' : 'left'}`}>
            <div className={`inline-block px-4 py-2 rounded-lg ${msg.type === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 dark:bg-gray-700 dark:text-white'
              }`}>
              {msg.text}
            </div>
            {msg.showFeedback && (
              <div className="mt-1 text-sm text-gray-500 flex gap-2 justify-start">
                Helpful?
                <button
                  onClick={() => submitFeedback('yes', msg)}
                  className="text-green-500 hover:underline"
                >
                  Yes
                </button>
                <button
                  onClick={() => submitFeedback('no', msg)}
                  className="text-red-500 hover:underline"
                >
                  No
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="flex mt-4">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          className="flex-grow p-2 border rounded-l dark:bg-gray-900 dark:text-white"
          placeholder="Ask a question..."
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-4 rounded-r"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
