import { z } from "zod";
import type { SourceDocument } from "../shared/types";

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
