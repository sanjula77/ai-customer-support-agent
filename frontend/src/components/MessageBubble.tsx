import { SourceInfo } from '@/types/api';
import ToolIndicator from './ToolIndicator';
import SourceList from './SourceList';
import styles from './MessageBubble.module.css';
import clsx from 'clsx';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceInfo[];
  toolUsed?: string;
  timestamp?: Date;
}

export default function MessageBubble({ role, content, sources, toolUsed, timestamp }: MessageBubbleProps) {
  return (
    <div className={clsx(styles.container, role === 'user' ? styles.user : styles.agent)}>
      <div className={styles.bubble}>
        <div className={styles.content}>{content}</div>
      </div>
      
      {(toolUsed || (sources && sources.length > 0) || timestamp) && (
        <div className={styles.footer}>
          {toolUsed && <ToolIndicator tool={toolUsed} />}
          {sources && sources.length > 0 && <SourceList sources={sources} />}
          {timestamp && (
            <span className={styles.timestamp}>
              {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
