import { AgentAskResponse, HealthResponse } from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function askAgent(
  sessionId: string,
  question: string,
  k: number = 5
): Promise<AgentAskResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/agent/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId,
        question: question,
        k: k,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Network error' }));
      throw new Error(error.detail || 'Failed to get response');
    }

    return response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

export async function checkHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
        throw new Error('Health check failed');
    }
    return response.json();
  } catch (error) {
    console.error("Health Check Error:", error);
    throw error;
  }
}
