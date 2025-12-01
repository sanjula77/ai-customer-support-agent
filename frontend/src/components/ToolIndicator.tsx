import styles from './ToolIndicator.module.css';
import clsx from 'clsx';

interface ToolIndicatorProps {
  tool: string;
}

export default function ToolIndicator({ tool }: ToolIndicatorProps) {
  if (!tool) return null;

  const getToolLabel = (tool: string) => {
    switch (tool) {
      case 'rag': return 'Knowledge Base';
      case 'order_lookup': return 'Order System';
      case 'direct_llm': return 'AI Reasoning';
      case 'ticket_creator': return 'Support Ticket';
      case 'update_address': return 'Address Update';
      case 'error': return 'Error';
      default: return tool.replace('_', ' ');
    }
  };

  return (
    <span className={clsx(styles.badge, styles[tool] || styles.default)}>
      {getToolLabel(tool)}
    </span>
  );
}
