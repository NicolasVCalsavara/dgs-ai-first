import { z } from "zod";
import { logger } from "../shared/logger";

/**
 * Decisões de contrato:
 * 1) Structured output usa `answer` (spec do provedor); no boundary adapter, `answer`
 *    mapeia para `response` de QueryResponse.
 * 2) `confidence_score` segue intervalo inclusivo [0, 1].
 * 3) `url` é OPCIONAL: o corpus de recuperação (Anexo B) identifica documentos por
 *    código/seção (ex.: POL-001, Seção 3.2) e não fornece URL. Exigir `url` faria toda
 *    resposta fiel ao corpus ser rejeitada — ou forçaria o modelo a inventar uma URL,
 *    justamente a alucinação que estes guardrails existem para impedir.
 *    TODO(reconciliação): tornar `SourceDocument.url` opcional em shared/types.ts e
 *    ajustar o boundary adapter para tratar `url` ausente.
 * 4) Os schemas usam `.strict()`: um output de formato fixo com campos inesperados é
 *    rejeitado e logado, não silenciosamente descartado.
 * 5) O guardrail de conteúdo é fail-safe: se a resposta trata de devolução de carga
 *    perigosa, a negativa obrigatória PRECISA estar presente; na sua ausência, bloqueia.
 */
export const SourceDocumentSchema = z
  .object({
    id: z.string().min(1),
    title: z.string().min(1),
    url: z.string().min(1).optional(),
    relevance_score: z.number(),
  })
  .strict();

export const StructuredOutputSchema = z
  .object({
    answer: z.string().min(1),
    source_document: SourceDocumentSchema,
    confidence_score: z.number().min(0).max(1),
  })
  .strict();

export type StructuredOutput = z.infer<typeof StructuredOutputSchema>;

export interface StructuredOutputValidationError {
  message: string;
  formErrors: string[];
  fieldErrors: Record<string, string[]>;
  issues: Array<{
    path: string;
    message: string;
    code: z.ZodIssueCode;
  }>;
}

export type StructuredOutputSafeParseResult =
  | { success: true; data: StructuredOutput }
  | { success: false; error: StructuredOutputValidationError };

export function safeParseStructuredOutput(
  input: unknown,
): StructuredOutputSafeParseResult {
  const result = StructuredOutputSchema.safeParse(input);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const flattened = result.error.flatten();

  return {
    success: false,
    error: {
      message: "Structured output validation failed",
      formErrors: flattened.formErrors,
      fieldErrors: flattened.fieldErrors,
      issues: result.error.issues.map((issue) => ({
        path: issue.path.join("."),
        message: issue.message,
        code: issue.code,
      })),
    },
  };
}

export const SAFE_FALLBACK_STRUCTURED_OUTPUT: StructuredOutput = {
  answer:
    "Não foi possível validar esta resposta com segurança. Reformule a solicitação ou encaminhe o caso para um atendente humano.",
  source_document: {
    id: "safe-fallback-human-handoff",
    title: "Escalonamento para atendimento humano",
    relevance_score: 0,
  },
  confidence_score: 0,
};

/** Guardrail 1 (estrutural): valida o formato. Sem `source_document` válido, reprova. */
export function applyStructuralGuardrail(
  input: unknown,
): StructuredOutputSafeParseResult {
  return safeParseStructuredOutput(input);
}

/**
 * Guardrail 2 (conteúdo): fail-safe. Se a resposta menciona carga perigosa E devolução,
 * a negativa obrigatória precisa estar presente; caso contrário, bloqueia (retorna false).
 * Avalia o texto inteiro — não fatia por frase, para não deixar a afirmação escapar entre
 * orações. É uma rede determinística grosseira que complementa o prompt probabilístico:
 * não interpreta semântica completa e prefere bloquear na dúvida.
 */
export function applyContentGuardrail(output: StructuredOutput): boolean {
  const answer = normalizeText(output.answer);
  const aboutDangerousReturn =
    mentionsDangerousCargo(answer) && mentionsReturn(answer);

  if (!aboutDangerousReturn) {
    return true;
  }

  return deniesReturn(answer);
}

export function validateStructuredResponse(input: unknown): StructuredOutput {
  const structureResult = applyStructuralGuardrail(input);

  if (!structureResult.success) {
    logger.error("response_validation_failed", {
      guardrail: "structure",
      reason: "Output não bate com o schema do structured output",
      fieldErrors: structureResult.error.fieldErrors,
      issues: structureResult.error.issues,
    });
    return SAFE_FALLBACK_STRUCTURED_OUTPUT;
  }

  if (!applyContentGuardrail(structureResult.data)) {
    logger.error("response_validation_failed", {
      guardrail: "content",
      reason:
        "Resposta trata de devolução de carga perigosa sem a negativa obrigatória (POL-001, Seção 3.2)",
      answer: structureResult.data.answer,
    });
    return SAFE_FALLBACK_STRUCTURED_OUTPUT;
  }

  return structureResult.data;
}

function normalizeText(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function mentionsDangerousCargo(value: string): boolean {
  return /\bcarga(s)? perigosa(s)?\b|\bprodutos? perigosos?\b|\bmercadoria(s)? perigosa(s)?\b|\bmaterial perigoso\b|\bmateriais perigosos\b/.test(
    value,
  );
}

function mentionsReturn(value: string): boolean {
  return /\bdevolucao\b|\bdevolver\b|\bdevolvid[ao]s?\b/.test(value);
}

/**
 * Detecta a negativa: uma negação/proibição próxima da devolução. Janela de 30 chars
 * para tolerar orações curtas ("não pode ser devolvida"). Limitação conhecida: paráfrases
 * distantes ou dupla negação podem não casar — por isso o guardrail bloqueia na ausência
 * da negativa, em vez de exigir o casamento de uma afirmação.
 */
function deniesReturn(value: string): boolean {
  return (
    /\bnao\b.{0,30}\b(devolucao|devolver|devolvid[ao]s?)\b/.test(value) ||
    /\b(devolucao|devolver|devolvid[ao]s?)\b.{0,30}\b(nao|proibid[ao]s?|vedad[ao]s?|inelegivel|impossivel|excecao|excecoes)\b/.test(
      value,
    )
  );
}
