"""Fine-tune Gemma 4 for scam detection using Unsloth.

This script fine-tunes a smaller Gemma 4 model on a curated scam detection
dataset, creating a specialized model that runs efficiently on consumer hardware.

Requirements:
    pip install unsloth datasets transformers trl

Usage:
    python training/finetune.py
"""

import json
from pathlib import Path

# Unsloth for fast, memory-efficient fine-tuning
from unsloth import FastLanguageModel
from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# ---- Configuration ----

MODEL_NAME = "google/gemma-4-4b"  # Base model (smaller variant for fine-tuning)
MAX_SEQ_LENGTH = 2048
LORA_R = 16
LORA_ALPHA = 16
LORA_DROPOUT = 0
OUTPUT_DIR = Path(__file__).parent / "outputs" / "beacon-scam-detector"
DATA_PATH = Path(__file__).parent / "data" / "scam_training.jsonl"


def load_training_data():
    """Load and format training data for instruction fine-tuning."""
    examples = []

    # Load from JSONL if it exists
    if DATA_PATH.exists():
        with open(DATA_PATH) as f:
            for line in f:
                examples.append(json.loads(line))
    else:
        # Use built-in examples for demonstration
        examples = get_builtin_examples()

    # Format as chat-style instruction pairs
    formatted = []
    for ex in examples:
        formatted.append({
            "text": format_training_example(ex)
        })

    return Dataset.from_list(formatted)


def format_training_example(ex):
    """Format a single training example in Gemma chat format."""
    system = (
        "You are Beacon's scam analysis engine. Analyze the given message for "
        "fraud indicators and respond with a JSON object containing: trust_score "
        "(0-100), risk_level, scam_type, red_flags (array), explanation (plain "
        "language), recommended_actions (array), and safe_alternatives."
    )

    user_msg = f"Analyze this message for scam indicators:\n\n{ex['message']}"
    assistant_msg = json.dumps(ex['analysis'], indent=2)

    return (
        f"<start_of_turn>user\n{system}\n\n{user_msg}<end_of_turn>\n"
        f"<start_of_turn>model\n{assistant_msg}<end_of_turn>"
    )


def get_builtin_examples():
    """Built-in training examples for scam detection."""
    return [
        {
            "message": "URGENT: Your Bank of America account has been suspended due to suspicious activity. Click here to verify: http://boa-secure-login.xyz/verify. You have 24 hours before permanent closure.",
            "analysis": {
                "trust_score": 5,
                "risk_level": "DANGEROUS",
                "scam_type": "Phishing",
                "red_flags": [
                    "Urgency pressure with 24-hour deadline",
                    "Suspicious URL (boa-secure-login.xyz is not Bank of America)",
                    "Threat of account closure to create panic",
                    "Asks you to click a link to 'verify' credentials"
                ],
                "explanation": "This is a phishing scam designed to steal your Bank of America login credentials. The link goes to a fake website that looks like Bank of America but is run by criminals. Real banks never send emails with urgent deadlines threatening to close your account.",
                "recommended_actions": [
                    "Do NOT click the link",
                    "Delete this email immediately",
                    "If concerned about your account, log in directly at bankofamerica.com",
                    "Report to Bank of America's fraud department: 1-800-432-1000",
                    "Forward to reportphishing@bankofamerica.com"
                ],
                "safe_alternatives": "Open a new browser window and type bankofamerica.com directly. Log in there to check your account status. Never click links in emails claiming to be from your bank."
            }
        },
        {
            "message": "Hi! This is a reminder that your Amazon order #402-8891247 has shipped and will arrive Tuesday. Track your package: amazon.com/track",
            "analysis": {
                "trust_score": 82,
                "risk_level": "LIKELY_SAFE",
                "scam_type": "None detected",
                "red_flags": [],
                "explanation": "This appears to be a legitimate Amazon shipping notification. It has a specific order number, a reasonable delivery timeline, and uses the correct Amazon domain for tracking. However, always verify by checking your Amazon account directly.",
                "recommended_actions": [
                    "If you recently ordered from Amazon, this is likely legitimate",
                    "You can verify by logging into your Amazon account and checking order history",
                    "The tracking link appears to use the correct amazon.com domain"
                ],
                "safe_alternatives": "To be extra safe, instead of clicking the link, open the Amazon app or go to amazon.com directly and check your orders there."
            }
        },
        {
            "message": "Congratulations! You've won $5,000,000 in the Microsoft International Lottery. To claim, send $250 processing fee via Western Union to our agent James Peterson. Reply with your full name, address, and bank account for direct deposit.",
            "analysis": {
                "trust_score": 2,
                "risk_level": "DANGEROUS",
                "scam_type": "Advance fee fraud (lottery scam)",
                "red_flags": [
                    "You cannot win a lottery you never entered",
                    "Asks for upfront payment via Western Union (untraceable)",
                    "Requests sensitive personal and banking information",
                    "Microsoft does not run lotteries",
                    "Unrealistic prize amount",
                    "Western Union payment is a classic scam payment method"
                ],
                "explanation": "This is a classic advance-fee lottery scam. There is no prize. If you send the $250, they will ask for more money and more fees, and you will never receive anything. Microsoft does not run lotteries. No legitimate lottery requires you to pay to claim winnings.",
                "recommended_actions": [
                    "Do NOT respond or send any money",
                    "Do NOT share any personal information",
                    "Block the sender",
                    "Report to the FTC at reportfraud.ftc.gov",
                    "Warn family members about this type of scam"
                ],
                "safe_alternatives": "Remember: if you didn't enter a lottery, you can't win one. Any 'prize' that requires payment is a scam. Legitimate lottery winnings are never claimed by sending money or personal information via email."
            }
        },
        {
            "message": "This is the Social Security Administration. Your Social Security number has been suspended due to suspicious activity. Press 1 to speak with an agent immediately or a warrant will be issued for your arrest today.",
            "analysis": {
                "trust_score": 3,
                "risk_level": "DANGEROUS",
                "scam_type": "Government impersonation",
                "red_flags": [
                    "SSA never calls to threaten you with arrest",
                    "Social Security numbers cannot be 'suspended'",
                    "Extreme urgency and threat of arrest",
                    "Government agencies communicate by mail, not threatening phone calls",
                    "Trying to get you to speak with a fake 'agent' who will steal your information"
                ],
                "explanation": "This is a government impersonation scam. The Social Security Administration will NEVER call you and threaten arrest. They don't suspend Social Security numbers. Scammers use fear of arrest to pressure people into giving up personal information or money. This is one of the most common scams targeting seniors.",
                "recommended_actions": [
                    "Hang up immediately",
                    "Do NOT press any buttons",
                    "Do NOT give any personal information",
                    "Report to SSA's Inspector General: 1-800-269-0271",
                    "Report to the FTC at reportfraud.ftc.gov",
                    "Tell friends and family about this scam"
                ],
                "safe_alternatives": "If you're worried about your Social Security account, contact SSA directly at 1-800-772-1213 or visit your local SSA office. Never trust incoming calls claiming to be from the government."
            }
        },
        {
            "message": "Hey, it's Sarah from your office. Can you do me a quick favor? I'm stuck in a meeting and need you to buy some gift cards for a client appreciation event. Get 5 Amazon gift cards at $100 each and text me the codes. I'll reimburse you. Don't tell anyone, it's a surprise!",
            "analysis": {
                "trust_score": 8,
                "risk_level": "DANGEROUS",
                "scam_type": "Gift card scam (business email compromise)",
                "red_flags": [
                    "Urgent request for gift cards is a classic scam pattern",
                    "Asks you to buy gift cards and share the codes",
                    "Says to keep it secret ('don't tell anyone')",
                    "Claims to be a colleague but may be an impersonator",
                    "Gift cards are untraceable once codes are shared",
                    "Promises reimbursement that will never come"
                ],
                "explanation": "This is almost certainly a gift card scam, even if it appears to come from someone you know. Scammers hack or impersonate coworkers' email/phone to trick people into buying gift cards. Once you share the codes, the money is gone instantly and cannot be recovered. No legitimate business transaction involves buying gift cards and texting the codes.",
                "recommended_actions": [
                    "Do NOT buy any gift cards",
                    "Call your actual colleague directly (not using the contact info in this message) to verify",
                    "Report to your IT department if this came via work email",
                    "If you already shared codes, contact the gift card company immediately",
                    "Report to the FTC at reportfraud.ftc.gov"
                ],
                "safe_alternatives": "If a colleague truly needs gift cards for work, they should go through official purchasing channels and never ask someone to buy them personally and share codes via text."
            }
        },
        {
            "message": "Your Xfinity bill of $142.87 is due on March 15. Pay at xfinity.com or call 1-800-XFINITY. Paperless billing is active on your account.",
            "analysis": {
                "trust_score": 88,
                "risk_level": "LIKELY_SAFE",
                "scam_type": "None detected",
                "red_flags": [],
                "explanation": "This appears to be a routine billing reminder from Xfinity/Comcast. It references a specific bill amount, a reasonable due date, and provides the correct official website and phone number. This matches the pattern of legitimate utility billing notifications.",
                "recommended_actions": [
                    "If you have an Xfinity account, this is likely a normal bill reminder",
                    "Verify by logging into your Xfinity account at xfinity.com directly",
                    "Check that the amount matches your expected bill"
                ],
                "safe_alternatives": "For extra peace of mind, go directly to xfinity.com or open the Xfinity app to confirm your bill amount and due date rather than clicking any links in the message."
            }
        },
    ]


def main():
    print("=" * 60)
    print("Beacon Scam Detector -- Fine-tuning with Unsloth")
    print("=" * 60)

    # Load model with Unsloth optimizations
    print(f"\nLoading {MODEL_NAME}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,  # Auto-detect
        load_in_4bit=True,
    )

    # Apply LoRA adapters
    print("Applying LoRA adapters...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=LORA_R,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    # Load training data
    print("Loading training data...")
    dataset = load_training_data()
    print(f"Training examples: {len(dataset)}")

    # Training
    print("\nStarting fine-tuning...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LENGTH,
        args=TrainingArguments(
            output_dir=str(OUTPUT_DIR),
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            num_train_epochs=3,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=1,
            save_strategy="epoch",
            seed=42,
        ),
    )

    trainer.train()

    # Save model
    print(f"\nSaving fine-tuned model to {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    # Export to GGUF for Ollama
    gguf_path = OUTPUT_DIR / "beacon-scam-detector.gguf"
    print(f"Exporting to GGUF: {gguf_path}...")
    model.save_pretrained_gguf(
        str(OUTPUT_DIR),
        tokenizer,
        quantization_method="q4_k_m",
    )

    print("\n" + "=" * 60)
    print("Fine-tuning complete!")
    print(f"Model saved to: {OUTPUT_DIR}")
    print(f"GGUF file: {gguf_path}")
    print()
    print("To use with Ollama:")
    print(f"  ollama create beacon-scam-detector -f {OUTPUT_DIR / 'Modelfile'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
