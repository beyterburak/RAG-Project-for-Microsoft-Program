/** FastAPI backend istemcisi (127.0.0.1:8000 — tamamen yerel). */

const API_BASE = "http://127.0.0.1:8000";

export type Variant = "v1" | "v2";

export interface Chunk {
  source: string;
  chunk_index: number;
  score: number;
  text: string;
}

export interface CorrectiveMeta {
  attempts: number;
  graded_out: number;
  rewritten_query: string | null;
  forced_refusal: boolean;
}

export interface AskResult {
  variant: Variant;
  question: string;
  answer: string;
  is_refusal: boolean;
  chunks: Chunk[];
  retrieval_seconds: number;
  llm_seconds: number;
  corrective?: CorrectiveMeta;
}

export async function ask(question: string, variant: Variant): Promise<AskResult> {
  const res = await fetch(`${API_BASE}/api/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, variant }),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => null);
    throw new Error(detail?.detail ?? `API hatası (${res.status})`);
  }
  return res.json();
}

export async function health(): Promise<{ status: string; chat_model: string } | null> {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { cache: "no-store" });
    return res.ok ? res.json() : null;
  } catch {
    return null;
  }
}
