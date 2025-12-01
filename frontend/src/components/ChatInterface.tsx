'use client';

import { useState, useEffect, useRef } from 'react';
import { askAgent } from '@/lib/api';
import { getOrCreateSessionId } from '@/lib/session';
import { SourceInfo } from '@/types/api';
import MessageBubble from './MessageBubble';
import InputArea from './InputArea';
import TypingIndicator from './TypingIndicator';
import styles from './ChatInterface.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceInfo[];
  toolUsed?: string;
  timestamp: Date;
}

export default function ChatInterface() {
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setSessionId(getOrCreateSessionId());
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await askAgent(sessionId, text);
      
      const agentMessage: Message = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        toolUsed: response.tool_used,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error(error);
      const errorMessage: Message = {
        role: 'assistant',
        content: "I&apos;m sorry, I encountered an error processing your request. Please try again later.",
        toolUsed: 'error',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.title}>
          <div className={styles.logo}>AI</div>
          NeuraHome Support
        </div>
        <div className={styles.status}>
          <div className={styles.statusDot}></div>
          Online
        </div>
      </header>

      <div className={styles.messages}>
        {messages.length === 0 ? (
          <div className={styles.emptyState}>
            <svg className={styles.emptyIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <h2 className={styles.emptyTitle}>How can I help you today?</h2>
            <p className={styles.emptyDesc}>
              Ask me about your orders, product manuals, or troubleshooting steps. I&apos;m here to assist you.
            </p>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <MessageBubble
                key={idx}
                role={msg.role}
                content={msg.content}
                sources={msg.sources}
                toolUsed={msg.toolUsed}
                timestamp={msg.timestamp}
              />
            ))}
            {loading && (
              <div className={styles.agent}>
                <TypingIndicator />
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputContainer}>
        <InputArea onSend={handleSend} disabled={loading} />
      </div>
    </div>
  );
}
