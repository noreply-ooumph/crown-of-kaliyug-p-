"""
Crown of Kaliyug — WhatsApp Notifier
Phase 0: Foundation
"""
import os
import requests
from loguru import logger

class WhatsAppNotifier:
    def __init__(self):
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_id}/messages"

    def send_approval_request(self, to: str, episode_id: str, script_preview: str):
        """
        Sends an interactive button message to WhatsApp for HITL approval.
        """
        if not self.token or not self.phone_id:
            logger.error("WhatsApp credentials missing. Skipping notification.")
            return

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {"type": "text", "text": f"Script Ready: {episode_id}"},
                "body": {"text": f"Preview: {script_preview[:100]}..."},
                "footer": {"text": "Crown of Kaliyug Production Engine"},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "approve", "title": "Approve"}},
                        {"type": "reply", "reply": {"id": "reject", "title": "Reject"}}
                    ]
                }
            }
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            logger.info(f"WhatsApp approval request sent for {episode_id}")
        except Exception as e:
            logger.error(f"WhatsApp Notify Error: {str(e)}")

wa_notifier = WhatsAppNotifier()
