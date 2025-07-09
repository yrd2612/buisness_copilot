from dotenv import load_dotenv
import os
load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
model_name = "gemini-2.0-flash" 
twilio_access_token = os.getenv("TWILIO_ACCESS")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")