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

export type StreamEvent =
  | { type: "graded"; attempt: number; kept: number; out: number }
  | { type: "high_confidence"; score: number }
  | { type: "rewritten"; query: string }
  | { type: "chunks"; chunks: Chunk[]; seconds: number }
  | { type: "token"; text: string }
  | { type: "verifying" }
  | { type: "revoked" }
  | {
      type: "done";
      answer: string;
      is_refusal: boolean;
      revoked: boolean;
      rewritten_query: string | null;
      retrieval_seconds: number;
      llm_seconds: number;
    }
  | { type: "error"; detail: string };

/** SSE akışını tüketir; her olay için onEvent çağrılır. */
export async function askStream(
  question: string,
  variant: Variant,
  onEvent: (ev: StreamEvent) => void
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/ask/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, variant }),
  });
  if (!res.ok || !res.body) throw new Error(`API hatası (${res.status})`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let sep;
    while ((sep = buffer.indexOf("\n\n")) >= 0) {
      const frame = buffer.slice(0, sep);
      buffer = buffer.slice(sep + 2);
      const dataLine = frame.split("\n").find((l) => l.startsWith("data: "));
      if (dataLine) onEvent(JSON.parse(dataLine.slice(6)) as StreamEvent);
    }
  }
}

export interface EvalSummary {
  questions: number;
  recall_at_k: number;
  top1_rate: number;
  answerable_accuracy: number;
  refusal_accuracy: number;
  overall_accuracy: number;
  avg_llm_seconds: number;
  median_total_seconds: number;
  top_k: number;
}

export interface EvalRow {
  id: number;
  type: "answerable" | "unanswerable";
  question: string;
  answer: string;
  retrieved: string[];
  is_refusal: boolean;
  retrieval_seconds: number;
  llm_seconds: number;
  recall_hit: boolean | null;
  top1_hit: boolean | null;
  correct: boolean;
}

export interface VariantResult {
  summary: EvalSummary;
  rows: EvalRow[];
}

export interface EvalResults {
  "v1-baseline"?: VariantResult;
  "v2-corrective"?: VariantResult;
  "v3-optimize"?: VariantResult;
}

export async function results(): Promise<EvalResults | null> {
  try {
    const res = await fetch(`${API_BASE}/api/results`, { cache: "no-store" });
    return res.ok ? res.json() : null;
  } catch {
    return null;
  }
}

export interface CorpusDoc {
  source: string;
  title: string;
  chunks: number;
  characters: number;
}

export interface Corpus {
  documents: CorpusDoc[];
  total_documents: number;
  total_chunks: number;
}

export async function corpus(): Promise<Corpus | null> {
  try {
    const res = await fetch(`${API_BASE}/api/corpus`, { cache: "no-store" });
    return res.ok ? res.json() : null;
  } catch {
    return null;
  }
}

export async function health(): Promise<{ status: string; chat_model: string } | null> {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { cache: "no-store" });
    return res.ok ? res.json() : null;
  } catch {
    return null;
  }
}
