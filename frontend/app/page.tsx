"use client";
import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

type Provider = 'ollama' | 'nvidia' | 'ragwithollama' | 'ragwithnvidia';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: "Hello! How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [provider, setProvider] = useState<Provider>('ollama');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
    const { data } = await axios.post('http://127.0.0.1:8000/llm/ask', { 
        prompt: input,
        model: provider 
      });
      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'assistant', content: "**Error:** Failed to connect to the backend API." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#f8fafc] text-slate-900 font-sans">
      <main className="flex-1 flex flex-col relative max-w-5xl mx-auto w-full bg-white shadow-2xl">
        
        {/* Header with Selection Menu */}
        <header className="px-8 py-4 border-b border-slate-100 flex justify-between items-center bg-white/80 backdrop-blur-md sticky top-0 z-10">
          <div>
            <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest">AI Interface</h2>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              <span className="text-xs font-semibold text-slate-500">Ready</span>
            </div>
          </div>

          <div className="flex flex-col items-end">
            <label className="text-[10px] font-bold text-slate-400 uppercase mb-1">Model Provider</label>
            <select 
              value={provider}
              onChange={(e) => setProvider(e.target.value as Provider)}
              className="bg-slate-50 border border-slate-200 text-slate-700 text-xs rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-1.5 outline-none"
            >
              <option value="ollama">Ollama</option>
              <option value="nvidia">NVIDIA</option>
              <option value="ragwithollama">Ollama + RAG</option>
              <option value="ragwithnvidia">NVIDIA + RAG</option>
            </select>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`group relative max-w-[85%] px-5 py-4 rounded-2xl transition-all duration-200 ${
                msg.role === 'user' 
                  ? 'bg-indigo-600 text-white shadow-indigo-100 shadow-lg rounded-tr-none' 
                  : 'bg-slate-100 text-slate-800 rounded-tl-none border border-slate-200'
              }`}>
                <div className="prose prose-sm max-w-none prose-slate break-words prose-p:leading-relaxed prose-pre:bg-slate-800 prose-pre:text-white">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex gap-1 p-4 bg-slate-100 rounded-2xl">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
              </div>
            </div>
          )}
          <div ref={scrollRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 bg-white">
          <form onSubmit={sendMessage} className="relative flex items-center group">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={`Send a message via ${provider}...`}
              className="w-full pl-6 pr-24 py-4 bg-slate-50 border border-slate-200 rounded-2xl 
                focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 
                transition-all text-slate-800 placeholder:text-slate-400"
            />
            <button 
              type="submit"
              disabled={isLoading}
              className="absolute right-3 px-5 py-2 bg-indigo-600 text-white font-medium rounded-xl 
                hover:bg-indigo-700 active:scale-95 transition-all disabled:opacity-50"
            >
              Send
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}