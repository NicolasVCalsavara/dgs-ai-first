import { z } from "zod";
import type { SourceDocument } from "../shared/types";
import { ValidationError } from "../shared/errors";
import { logger } from "../shared/logger";

/**
 * Decisoes de contrato:
 * 1) Structured output usa `answer` (spec do provedor); no boundary adapter, `answer` mapeia para `response` de QueryResponse.
 * 2) `confidence_score` segue intervalo inclusivo [0, 1].
 * 3) `url` permanece obrigatoria porque faz parte de SourceDocument em shared/types.ts; o identificador do corpus nao substitui esse contrato.
 */
export const SourceDocumentSchema: z.ZodType<SourceDocument> = z.object({
	id: z.string().min(1),
	title: z.string().min(1),
	url: z.string().min(1),
	relevance_score: z.number(),
});

export const StructuredOutputSchema = z.object({
	answer: z.string().min(1),
	source_document: SourceDocumentSchema,
	confidence_score: z.number().min(0).max(1),
});

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
	| {
			success: true;
			data: StructuredOutput;
		}
	| {
			success: false;
			error: StructuredOutputValidationError;
		};

export function safeParseStructuredOutput(
	input: unknown,
): StructuredOutputSafeParseResult {
	const result = StructuredOutputSchema.safeParse(input);

	if (result.success) {
		return {
			success: true,
			data: result.data,
		};
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

const SAFE_FALLBACK_SOURCE_DOCUMENT: SourceDocument = {
	id: "safe-fallback-human-handoff",
	title: "Escalonamento para atendimento humano",
	url: "https://novatech.example/human-handoff",
	relevance_score: 0,
};

export const SAFE_FALLBACK_STRUCTURED_OUTPUT: StructuredOutput = {
	answer:
		"Nao foi possivel validar esta resposta com seguranca. Reformule a solicitacao ou encaminhe o caso para um atendente humano.",
	source_document: SAFE_FALLBACK_SOURCE_DOCUMENT,
	confidence_score: 0,
};

export function applyStructuralGuardrail(
	input: unknown,
): StructuredOutputSafeParseResult {
	return safeParseStructuredOutput(input);
}

export function applyContentGuardrail(output: StructuredOutput): boolean {
	const normalizedAnswer = normalizeText(output.answer);
	const segments = normalizedAnswer
		.split(/[.!?;\n]+/)
		.map((segment) => segment.trim())
		.filter((segment) => segment.length > 0);

	for (const segment of segments) {
		if (!mentionsDangerousCargo(segment) || !mentionsReturn(segment)) {
			continue;
		}

		if (deniesReturn(segment)) {
			continue;
		}

		if (affirmsReturn(segment)) {
			return false;
		}
	}

	return true;
}

export function validateStructuredResponse(input: unknown): StructuredOutput {
	const structureResult = applyStructuralGuardrail(input);

	if (!structureResult.success) {
		const error = new ValidationError(
			"Structured output failed schema validation",
			structureResult.error.fieldErrors,
		);

		logger.error("response_validation_failed", {
			guardrail: "structure",
			errorName: error.name,
			message: error.message,
			details: error.details,
			validation: structureResult.error,
		});

		return SAFE_FALLBACK_STRUCTURED_OUTPUT;
	}

	if (!applyContentGuardrail(structureResult.data)) {
		const error = new ValidationError("Structured output failed content guardrail", {
			answer: [
				"Answer states that dangerous cargo can be returned, which conflicts with POL-001 section 3.2.",
			],
		});

		logger.error("response_validation_failed", {
			guardrail: "content",
			errorName: error.name,
			message: error.message,
			details: error.details,
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
	return /\bcarga(s)? perigosa(s)?\b|\bprodutos? perigosos?\b/.test(value);
}

function mentionsReturn(value: string): boolean {
	return /\bdevolucao\b|\bdevolver\b|\bdevolvid[ao]s?\b/.test(value);
}

function deniesReturn(value: string): boolean {
	return /\bnao\b.{0,20}\b(devolucao|devolver|devolvid[ao]s?)\b|\b(devolucao|devolver|devolvid[ao]s?)\b.{0,20}\b(nao|proibid[ao]s?|vedad[ao]s?|inelegivel|impossivel)\b/.test(
		value,
	);
}

function affirmsReturn(value: string): boolean {
	/*
	 * Heuristica textual: so bloqueamos quando um mesmo trecho menciona carga perigosa,
	 * devolucao e um termo de permissao/elegibilidade sem negacao explicita proxima.
	 * Limitacao: a regra nao faz interpretacao semantica completa; ela complementa o prompt,
	 * mas pode nao capturar formulacoes indiretas ou ambiguas.
	 */
	return /\b(pode|podem|permitid[ao]s?|possivel|elegivel|autorizad[ao]s?)\b.{0,20}\b(devolucao|devolver|devolvid[ao]s?)\b|\b(devolucao|devolver|devolvid[ao]s?)\b.{0,20}\b(pode|podem|permitid[ao]s?|possivel|elegivel|autorizad[ao]s?)\b/.test(
		value,
	);
}
