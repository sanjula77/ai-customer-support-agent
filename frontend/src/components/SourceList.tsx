import { SourceInfo } from '@/types/api';
import styles from './SourceList.module.css';

interface SourceListProps {
  sources: SourceInfo[];
}

export default function SourceList({ sources }: SourceListProps) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className={styles.container}>
      <div className={styles.title}>Sources</div>
      <div className={styles.list}>
        {sources.map((src, idx) => (
          <div key={idx} className={styles.item}>
            <span className={styles.sourceTitle}>{src.title || src.source_file}</span>
            <div className={styles.meta}>
              {src.section && <span>{src.section}</span>}
              {src.score && (
                <span className={styles.score}>
                  {(src.score * 100).toFixed(0)}% match
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
