import { CosmosClient, Container } from "@azure/cosmos";
import { app, HttpRequest, HttpResponseInit } from "@azure/functions";
import { validateFeedbackRequest } from "./validator";
import { config, getFeedbackConfig } from "../../shared/config";
import { ValidationError } from "../../shared/errors";
import { logger } from "../../shared/logger";

interface FeedbackDocument {
  queryId: string;
  rating: number;
  comment?: string;
  attendantEmail: string;
  timestamp: string;
}

let cachedContainer: Container | null = null;

function getFeedbackContainer(): Container {
  if (cachedContainer) {
    return cachedContainer;
  }

  const feedbackConfig = getFeedbackConfig();
  const client = new CosmosClient(feedbackConfig.cosmosConnectionString);

  cachedContainer = client
    .database(feedbackConfig.cosmosDatabaseName)
    .container(feedbackConfig.cosmosFeedbackContainerName);

  return cachedContainer;
}

export async function feedbackHandler(
  request: HttpRequest
): Promise<HttpResponseInit> {
  try {
    const body: unknown = await request.json().catch(() => ({}));
    const feedbackRequest = validateFeedbackRequest(body);
    const feedback: FeedbackDocument = {
      queryId: feedbackRequest.queryId,
      rating: feedbackRequest.rating,
      comment: feedbackRequest.comment,
      attendantEmail: feedbackRequest.attendantEmail,
      timestamp: new Date().toISOString(),
    };

    await getFeedbackContainer().items.create(feedback);

    logger.info("feedback_created", {
      queryId: feedback.queryId,
      rating: feedback.rating,
      hasComment: typeof feedback.comment === "string" && feedback.comment.length > 0,
    });

    return {
      status: 201,
      jsonBody: {
        message: "Feedback registrado com sucesso",
      },
    };
  } catch (error) {
    if (error instanceof ValidationError) {
      return {
        status: 400,
        jsonBody: {
          error: error.message,
          details: error.details,
        },
      };
    }

    logger.error("feedback_persistence_failed", {
      errorMessage: error instanceof Error ? error.message : String(error),
    });

    return {
      status: 500,
      jsonBody: {
        error: "Internal server error",
        message:
          config.environment === "development"
            ? error instanceof Error
              ? error.message
              : String(error)
            : "An unexpected error occurred",
      },
    };
  }
}

app.http("feedback", {
  methods: ["POST"],
  authLevel: "function",
  handler: feedbackHandler
});