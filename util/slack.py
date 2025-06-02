import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackAlert:
    def __init__(self, slack_token: str, env: str, test_alerts_slack_channel_id: str, ai_copilot_errors_slack_channel_id: str):
        self.slack_client = WebClient(token=slack_token)
        self.env = env
        self.test_alerts_slack_channel_id = test_alerts_slack_channel_id
        self.ai_copilot_errors_slack_channel_id = ai_copilot_errors_slack_channel_id

    def send_slack_message(self, message: str, is_error: bool = False, slack_channel: str = None):
        """
        Send a message to a Slack channel.

        Args:
            message (str): The message to send
            is_error (bool, optional): Whether this is an error message. Defaults to False.
            slack_channel (str, optional): The Slack channel ID to send to. Defaults to AI_COPILOT_ERRORS_SLACK_CHANNEL_ID.

        Returns:
            dict: The Slack API response if successful, None if failed
        """
        if not slack_channel:
            slack_channel = self.ai_copilot_errors_slack_channel_id

        if self.env != "production":
            slack_channel = self.test_alerts_slack_channel_id

        emoji = "🚨" if is_error else "ℹ️"
        formatted_message = f"{emoji} {message}"

        try:
            response = self.slack_client.chat_postMessage(
                channel=slack_channel,
                text=formatted_message,
                blocks=[
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": formatted_message},
                    }
                ],
            )
            return response

        except SlackApiError as err:
            logging.error("Failed to send Slack message: %s", err.response["error"])
            return None

    def send_message_at_ai_copilot_errors(self, message: str):
        self.send_slack_message(message=message, is_error=True, slack_channel=self.ai_copilot_errors_slack_channel_id)
