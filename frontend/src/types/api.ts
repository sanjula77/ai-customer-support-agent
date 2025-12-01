export interface QuestionRequest {
  question: string;
  k?: number;
  include_sources?: boolean;
}

export interface AgentAskRequest {
  session_id: string;
  question: string;
  k?: number;
  force_rag?: boolean | null;
}

export interface ChatRequest {
  session_id: string;
  message: string;
  k?: number;
}

export interface SourceInfo {
  title?: string;
  score?: number;
  category?: string;
  source_file?: string;
  section?: string;
}

export interface AnswerResponse {
  answer: string;
  sources?: SourceInfo[] | null;
}

export interface AgentAskResponse {
  session_id: string;
  message: string;
  answer: string;
  sources: SourceInfo[];
  tool_used: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceInfo[];
}

export interface HealthResponse {
  status: "ok";
  message: string;
  api_key_configured: boolean;
}
