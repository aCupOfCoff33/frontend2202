# backend.py

import signal
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response  # Import Response for handling OPTIONS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from pydantic import BaseModel
from typing import Optional
from sentence_transformers import SentenceTransformer, util

# Initialize the FastAPI application
app = FastAPI()

# Configure CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define phrases that should be filtered out as bad responses
BAD_RESPONSES = [
    "", " ", "Expert 1:", "Expert 2:", "This is a great idea.", "That's an excellent point.",
    "That's great!", "Good idea.", "Good point.", "I agree.", "Thank you.", "Certainly.",
    "Absolutely.", "Indeed.", "Sure.", "Of course.", "That's true.", "You're right.",
    "I think so too.", "Let's continue.", "That's helpful.", "I would agree.",
    "I would agree with you.", "great idea", "fantastic idea", "good idea", "excellent idea",
    "wonderful idea", "amazing idea", "superb idea", "thanks for your time", "thank you for your time",
    "Thanks for the information."
]

# Determine the device for running the model
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
print(f"Using device: {device}")

# Load the pre-trained language model (flan-t5-large)
MODEL_NAME = "google/flan-t5-xl"

# Initialize the tokenizer for encoding/decoding text
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the sentence-transformers model for semantic similarity checks
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the main transformer model with appropriate device settings
if device.type in ["mps", "cuda"]:  # Use GPU if available
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        torch_dtype=torch.float16,  # Use half-precision for efficiency
        low_cpu_mem_usage=True
    )
else:  # Use CPU otherwise
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,  # Use full precision on CPU
        low_cpu_mem_usage=True
    ).to(device)
print("Model loaded successfully.")

def is_repeated_idea(response, history):
    """
    Check if the newly generated response is semantically similar to any prior responses in the chat history.
    """
    history_lines = [line.split(": ", 1)[1] for line in history.split("\n") if ": " in line]
    if not history_lines:  # If no history exists, no repetition
        return False

    history_embeddings = similarity_model.encode(history_lines, convert_to_tensor=True)
    response_embedding = similarity_model.encode(response, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(response_embedding, history_embeddings)
    max_similarity = similarities.max().item()

    if max_similarity > 0.8:
        print(f"Rejected response as repeated idea (similarity={max_similarity:.2f}): {response}")
        return True
    return False

def generate_response(prompt, current_speaker, max_length=150, temperature=0.8, top_p=0.9, no_repeat_ngram_size=3):
    """
    Generate a response from the model and prepend the speaker label.
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(model.device)

    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=temperature,
        do_sample=True,
        top_p=top_p,
        no_repeat_ngram_size=no_repeat_ngram_size,
        repetition_penalty=1.2,
        eos_token_id=tokenizer.eos_token_id,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return f"{current_speaker}: {response}"

class ChatHistory(BaseModel):
    """
    Pydantic model for validating the chat history received in POST requests.
    """
    history: str
    mode: Optional[str] = "experts"

def determine_current_speaker(history: str, mode: str) -> Optional[str]:
    """
    Determine the next speaker (Expert 1 or Expert 2) based on the conversation history and mode.
    """
    lines = history.strip().split("\n")

    if mode == "experts":
        if lines and lines[-1].startswith("Expert 1:"):
            return "Expert 2"
        elif lines and lines[-1].startswith("Expert 2:"):
            return "Expert 1"
        else:
            return "Expert 1"  # Default to Expert 1
    elif mode == "expert2":
        if lines and lines[-1].startswith("Expert 1:"):
            return "Expert 2"  # User's turn
        elif lines and lines[-1].startswith("Expert 2:"):
            return "Expert 1"  # Backend's turn
        else:
            return "Expert 1"  # Default to Expert 1
    else:
        return None  # Invalid mode

@app.post("/chat")
def chat(data: ChatHistory):
    """
    Handle chat requests. Generate responses from the appropriate expert.
    """
    history = data.history
    mode = data.mode

    print("Received chat request.")
    print(f"Mode: {mode}")
    print(f"History:\n{history}")

    current_speaker = determine_current_speaker(history, mode)
    print(f"Current speaker: {current_speaker}")

    if current_speaker is None:
        print("No speaker determined. Returning empty response.")
        return {"response": ""}

    # Define instructions based on the mode
    if mode == "experts":
        instruction = (
            "The following is a conversation between Expert 1 and Expert 2 about strategies to eliminate bullying in classrooms. "
            "Both experts specialize in educational psychology and student welfare. "
            "They provide actionable, research-based insights, avoiding repetition or generic statements."
        )
    elif mode == "expert2":
        instruction = (
            "The following is a conversation between Expert 1 and Expert 2 about strategies to eliminate bullying in classrooms. "
            "Expert 1 is an AI expert in educational psychology, while Expert 2 is a human with experience in student welfare. "
            "Only Expert 1 generates responses, focusing on clear, actionable strategies."
        )
    else:
        print("Invalid mode provided. Returning empty response.")
        return {"response": ""}

    # Prepare the prompt
    prompt = f"{instruction}\n{history}\n{current_speaker}:"
    print(f"Prompt for model:\n{prompt}")

    # Attempt to generate a valid response
    for attempt in range(5):
        response_text = generate_response(prompt, current_speaker)
        response_clean = response_text.strip()

        print(f"Attempt {attempt + 1}: Generated response: {response_clean}")

        # Validate the response
        if ": " not in response_clean:
            print("Invalid response format. Rejecting.")
            continue

        speaker_label, message = response_clean.split(": ", 1)

        if speaker_label not in ["Expert 1", "Expert 2"]:
            print("Invalid speaker label in response. Rejecting.")
            continue

        if response_clean in BAD_RESPONSES or is_repeated_idea(message, history):
            print("Response rejected due to bad content or repetition.")
            continue

        # All checks passed; return the response
        print(f"Returning response: {response_clean}")
        return {"response": response_clean}

    # Fallback response if all attempts fail
    fallback_response = f"{current_speaker}: Empowering bystanders to report bullying and supporting victims is a proven method."
    print(f"Fallback response: {fallback_response}")
    return {"response": fallback_response}

# Handle preflight OPTIONS requests globally (optional, as CORSMiddleware should handle it)
@app.options("/chat")
async def options_chat(request: Request):
    return Response(status_code=200)

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=False)