Decyphra Setup Guide

TRL 3 Proof of Concept | AI-Powered Blockchain Wallet Investigation

Decyphra combines blockchain data retrieval, deterministic parsing, structured evidence, and AI reasoning to turn raw wallet activity into understandable investigations.

«Investigate → Understand → Ask → Investigate deeper.»

---

Table of Contents

1. "Quick Start" (#quick-start)
2. "API Key Configuration" (#api-key-configuration)
3. "Architecture" (#architecture)
4. "Security & Evidence Philosophy" (#security--evidence-philosophy)
5. "AI Reasoning & Hallucination Risk" (#ai-reasoning--hallucination-risk)
6. "Evidence-First Reasoning" (#evidence-first-reasoning)
7. "Current Limitations" (#current-limitations)
8. "Future Roadmap" (#future-roadmap)
9. "Troubleshooting" (#troubleshooting)

---

Quick Start

Prerequisites

- Python 3.x
- "pip"
- Alchemy API key
- OpenRouter API key

Installation

# 1. Clone the repository
git clone https://github.com/kiliancool/AI_powered_wallet_investigator.git
cd AI_powered_wallet_investigator

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r ai/requirements.txt

# 4. Create your environment file
cp .env.example .env

# 5. Add your API keys
nano .env

# 6. Run Decyphra
python main.py

First Run

Enter a wallet address: 0x1234567890123456789012345678901234567890

Gathering onchain intelligence...

Decyphra is here to help you decipher onchain intelligence. What do you need?

You: [Ask a follow-up question or type 'exit' to quit]

---

API Key Configuration

Decyphra currently uses two external services:

- Alchemy — blockchain data
- OpenRouter — AI reasoning

Both offer options suitable for experimentation, although usage limits and availability can vary.

1. Alchemy

Alchemy provides Ethereum blockchain data used to construct the investigation evidence.

Setup

1. Visit "https://www.alchemy.com/"
2. Create an account.
3. Create an application.
4. Select Ethereum → Mainnet.
5. Copy the API key.
6. Add it to ".env":

API_KEY=your_alchemy_api_key_here

Used For

- Native ETH transfers
- ERC-20 transfers
- ERC-721 transfers
- ERC-1155 transfers
- Token metadata
- Historical blockchain data

Alchemy usage is measured in Compute Units (CUs) and depends on the API methods and number of requests made. Monitor usage through the Alchemy dashboard rather than assuming a fixed cost per investigation.

---

2. OpenRouter

OpenRouter provides the model interface for Decyphra's reasoning layer.

Setup

1. Visit "https://openrouter.ai/"
2. Create an account.
3. Open API Keys.
4. Create an API key.
5. Add it to ".env":

OPENROUTER_API_KEY=your_openrouter_api_key_here

Models

The configured models are defined in the project configuration.

Example:

DEFAULT_MODEL=cohere/north-mini-code:free
FALLBACK_MODEL=your_configured_fallback_model

Free models can have model/provider-specific rate limits and availability.

Why OpenRouter?

- Model abstraction
- Easy model switching
- Fallback support
- Centralized API access
- Faster experimentation during development

---

Architecture

Decyphra separates data acquisition from AI reasoning.

┌─────────────────────────────────────────┐
│              USER INPUT                 │
│       Wallet Address + Questions        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       BLOCKCHAIN DATA LAYER             │
│               api.py                    │
│                                         │
│  • Alchemy requests                     │
│  • Transfer retrieval                   │
│  • Pagination                           │
│  • Metadata                             │
│  • Error handling                       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       PARSING & VALIDATION              │
│                                         │
│  • Type validation                      │
│  • Hex conversion                       │
│  • Numeric conversion                   │
│  • Timestamp normalization              │
│  • Missing-data detection               │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│        STRUCTURED EVIDENCE              │
│                                         │
│  • Normalized data                      │
│  • Metadata                             │
│  • Completeness flags                   │
│  • Truncation indicators                │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│          AI REASONING LAYER             │
│             ai/engine.py                │
│                                         │
│  • Evidence-first reasoning             │
│  • System prompt constraints            │
│  • Conversation context                 │
│  • Uncertainty handling                 │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         INVESTIGATION RESULTS           │
│                                         │
│  Facts → Patterns → Interpretation      │
│          → Follow-up questions          │
└─────────────────────────────────────────┘

---

Security & Evidence Philosophy

Blockchain data is not instructions.

External data such as token names, symbols, labels, and metadata is treated as untrusted content.

The application parses and structures the data before supplying it to the reasoning layer.

The AI is not the blockchain.

The reasoning engine interprets supplied evidence. It does not independently:

- Query blockchain APIs
- Execute transactions
- Sign transactions
- Change retrieved evidence
- Establish facts outside the supplied dataset

Evidence is the foundation.

Decyphra separates conclusions into:

FACT → DERIVED → OBSERVATION → INTERPRETATION → HYPOTHESIS → UNKNOWN

This prevents the system from presenting an interpretation as if it were a blockchain fact.

---

AI Reasoning & Hallucination Risk

LLMs can produce plausible but unsupported statements. Decyphra therefore uses multiple layers of mitigation.

1. Evidence-First System Prompt

The system prompt instructs the model to:

- Avoid fabrication
- Separate facts from interpretations
- Respect data boundaries
- Acknowledge uncertainty
- Reject correlation-as-causation
- Treat user claims as hypotheses rather than blockchain facts

These are model-level constraints, not absolute guarantees.

2. Deterministic Data Processing

Basic blockchain data processing happens before AI reasoning.

def hex_to_int(value):
    if not isinstance(value, str):
        raise TypeError("hex_to_int() expects a string")

    if not value.startswith(("0x", "0X")):
        raise ValueError(f"Not a hexadecimal value: {value}")

    return int(value, 16)

3. Structured Evidence

Example:

{
  "transaction": {
    "hash": "0xabc...",
    "block_number": 18500000,
    "timestamp": "15 Aug 2024, 10:30:45 UTC",
    "from_address": "0x123...",
    "to_address": "0x456...",
    "value_eth": "1.5",
    "token_address": "0x...",
    "token_symbol": "USDC",
    "token_decimals": 6,
    "category": "erc20"
  },
  "metadata": {
    "source": "Alchemy API",
    "page_limit_reached": false
  }
}

The token contract address remains the authoritative identifier; metadata such as symbols is descriptive.

4. Conversation Limits

Conversation memory is intentionally bounded to control context size and reduce stale conversational assumptions.

MAX_MESSAGES = 15

5. Fallback Models

If the configured model encounters a temporary failure or rate limit, Decyphra can switch to a configured fallback model.

---

Evidence-First Reasoning

Decyphra avoids jumping directly from activity to intent.

Example

Instead of:

"This wallet is suspicious because it received
money and immediately moved it elsewhere."

The system should reason more carefully:

OBSERVATION:
The wallet received 50 ETH during the observed period
and subsequently transferred approximately 50 ETH out.

INTERPRETATION:
The pattern is consistent with several possible explanations,
including treasury distribution or other rapid fund movement.

HYPOTHESIS:
The activity may warrant further investigation.

UNKNOWN:
The available evidence does not establish the intent behind
the transfers.

Data boundaries matter.

If only a limited transaction history was retrieved, the AI should say:

«"Within the retrieved history..."»

rather than:

«"This wallet always..."»

Similarly, missing token metadata should be reported as unknown rather than guessed.

Correlation ≠ Causation

- Sending funds to an exchange does not prove exchange ownership.
- Interacting with a suspicious contract does not prove a scam.
- Rapid transactions do not automatically prove bot activity.

Patterns can justify investigation without establishing intent.

---

Current Limitations

Decyphra is a TRL 3 proof of concept, not a production-grade forensic platform.

Blockchain Coverage

Capability| Status
Ethereum Mainnet| ✅ Supported
ERC-20 transfers| ✅ Supported
ERC-721 transfers| ⚠️ Partial
ERC-1155 transfers| ⚠️ Partial
L2 networks| ❌ Not currently supported
Bitcoin| ❌ Not currently supported
Solana| ❌ Not currently supported
Advanced contract analysis| ❌ Not currently supported
Liquidity-pool analysis| ❌ Not currently supported

Data Limitations

- Transfer retrieval is intentionally bounded by the application's pagination settings.
- Current configuration can retrieve up to 5 pages × 500 transfer records per configured retrieval path.
- Coverage depends on wallet activity and the API queries being performed.
- Historical price enrichment is not currently supported.
- Token metadata may be incomplete.
- Missing token decimals should be treated as unknown rather than assuming 18.

AI Limitations

Decyphra cannot reliably:

- Identify the real-world owner of an address
- Prove criminal activity
- Determine intent from blockchain activity alone
- Predict future behavior
- Replace professional blockchain forensic tools
- Guarantee that an AI interpretation is correct

Infrastructure

Component| Current State
Interface| CLI
Users| Single-user/local
Authentication| Not implemented
Memory| Local JSON
Database| Not implemented
Caching| Limited/not implemented
API availability| External-provider dependent
AI availability| Model/provider dependent

---

Future Roadmap

Phase 1 — Proof of Concept

Goal: Demonstrate evidence-first AI wallet investigation.

Phase 2 — Investigation Intelligence

Goal: Expand wallet investigation depth, data coverage, and investigative capabilities.

Phase 3 — Advanced Intelligence

Goal: Build broader blockchain intelligence through deeper relationships, contract analysis, and cross-wallet investigation.

Phase 4 — Productization

Goal: Transform the investigation engine into a scalable product for individuals, researchers, security teams, and institutions.

For the full product vision and roadmap, see "README.md" (README.md).

---

Troubleshooting

"API_KEY is missing from the environment"

Check that ".env" exists:

ls -la .env

If missing:

cp .env.example .env
nano .env

Add:

API_KEY=your_alchemy_api_key_here

---

"OPENROUTER_API_KEY is missing"

Add the key to ".env":

OPENROUTER_API_KEY=your_openrouter_api_key_here

Restart Decyphra after saving.

---

"Error: Invalid wallet address"

An Ethereum address contains:

- "0x"
- 40 hexadecimal characters

Example:

0x1234567890123456789012345678901234567890

For real investigations, copy addresses from a trusted source instead of manually typing them.

---

Rate Limit / Too Many Requests

Alchemy

Check your Compute Unit usage in the Alchemy dashboard.

If necessary:

- Reduce repeated investigations
- Avoid unnecessary API calls
- Add caching
- Consider a higher usage tier

OpenRouter

Free models can have provider-specific limits.

If requests fail:

- Wait and retry
- Check model availability
- Use the configured fallback model
- Check your OpenRouter account limits

---

Transfer Data Is Incomplete

If Decyphra reports truncation, the configured retrieval boundary was reached.

This means:

«The investigation covers the retrieved dataset.»

It does not mean:

«The wallet has no older activity.»

---

The AI Seems to Be Hallucinating

If the response doesn't match the evidence:

1. Verify the transaction using a primary blockchain explorer.
2. Compare the response with the evidence supplied to the model.
3. Check for missing or truncated data.
4. Record the failure for investigation/testing.

Useful information to preserve:

- Wallet address
- User question
- AI response
- Relevant transaction evidence
- Data supplied to the model

These failures are valuable test cases for improving Decyphra's reasoning layer.

---

Final Principle

«The blockchain provides the evidence.
Decyphra structures it.
AI helps interpret it.
The user investigates further.»

Investigate → Understand → Ask → Investigate deeper.
---

## Additional Resources

| Resource | Link |
|----------|------|
| Full Vision Statement | [README.md](README.md) |
| System Prompt Design | [ai/system_prompt.py](ai/system_prompt.py) |
| API Documentation | [api.py](api.py) |
| Architecture Diagram | [README.md - Prototype Architecture](README.md#prototype-architecture) |
| Alchemy Docs | https://docs.alchemy.com/ |
| OpenRouter Docs | https://openrouter.ai/docs |
| Ethereum Basics | https://ethereum.org/en/developers/docs/ |

---
