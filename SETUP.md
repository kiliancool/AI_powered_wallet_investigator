# Decyphra Setup Guide

**TRL 3 Proof of Concept | AI-Powered Blockchain Wallet Investigation**

---

## Table of Contents

1. [Quick Start (5 Minutes)](#quick-start-5-minutes)
2. [API Key Configuration](#api-key-configuration)
3. [Architecture & Security Philosophy](#architecture--security-philosophy)
4. [AI Security & Hallucination Risk](#ai-security--hallucination-risk)
5. [System Prompt & Evidence-First Reasoning](#system-prompt--evidence-first-reasoning)
6. [Current Limitations](#current-limitations)
7. [Future Roadmap](#future-roadmap)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start (5 Minutes)

### Prerequisites

- Python
- `pip` (Python package manager)
- Two API keys (instructions below)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/kiliancool/AI_powered_wallet_investigator.git
cd AI_powered_wallet_investigator

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r ai/requirements.txt

# 4. Copy the environment template
cp .env.example .env

# 5. Add your API keys to .env (see section below)
# Edit .env with your keys

# 6. Run Decyphra
python main.py
```

### First Run

```
Enter a wallet address: 0x1234567890123456789012345678901234567890

Gathering onchain intelligence..

Decyphra is here to help you decipher onchain intelligence. What do you need?

You: [Ask a follow-up question or type 'exit' to quit]
```

---

## API Key Configuration

Decyphra requires **two API keys** to function. Both are free to obtain.

### 1. Alchemy API Key (Blockchain Data)

Alchemy provides the blockchain data layer. It's free and includes 300M compute units/month (more than enough for experimentation).

**Steps:**

1. Go to https://www.alchemy.com/
2. Click **"Sign Up"** and create an account
3. Verify your email
4. Create a new app:
   - Select **"Ethereum"** as the chain
   - Select **"Mainnet"** as the network
   - Name it "Decyphra" (or whatever)
5. Copy your **API Key** from the dashboard
6. Add it to `.env`:
   ```
   API_KEY=your_alchemy_api_key_here
   ```

**Rate Limits:**
- Free tier: 300M compute units/month (~3,000 wallet investigations)
- Each wallet investigation uses approximately 100K compute units

**What Alchemy Provides:**
- `alchemy_getAssetTransfers` – ERC20, ERC721, ERC1155, and native ETH transfers
- Token metadata (decimals, symbols)
- Full transaction history (paginated)
- Historical block data

### 2. OpenRouter API Key (AI Reasoning)

OpenRouter provides a unified interface to multiple LLMs. Free tier available with rate limits.

**Steps:**

1. Go to https://openrouter.ai/
2. Click **"Sign Up"** and create an account
3. Verify your email
4. Go to **API Keys** in your dashboard
5. Create a new API key
6. Copy it and add to `.env`:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

**Models Used:**

- **Default:** `cohere/north-mini-code:free` (fast, free tier)
- **Fallback:** `liquid/lfm-2.5-2.6b:free` (backup if default rate-limited)

**Rate Limits:**
- Free tier: 20 requests/minute, 200K tokens/day
- Plenty for investigation workflows

**Why OpenRouter Instead of Direct API?**
- Model abstraction (can swap models without code changes)
- Fallback mechanism for reliability
- Unified billing and monitoring
- Free tier is generous for proof-of-concept work

---

## Architecture & Security Philosophy

### Three-Layer Design

```
┌─────────────────────────────────────────┐
│  User Input (Wallet Address)            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  BLOCKCHAIN LAYER (api.py)              │
│  ✓ Alchemy API calls with retry logic   │
│  ✓ Pagination handling (5 pages max)    │
│  ✓ Error handling & timeout management  │
│  ✓ Metadata collection                  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  PARSING & VALIDATION LAYER             │
│  ✓ Type checking & sanitization         │
│  ✓ Hex conversion with fallbacks        │
│  ✓ Decimal precision (Wei → ETH)        │
│  ✓ Timestamp normalization              │
│  ✓ Missing data detection               │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  STRUCTURED EVIDENCE BUFFER             │
│  ✓ JSON with metadata                   │
│  ✓ Data completeness flags              │
│  ✓ Truncation warnings                  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  AI REASONING LAYER (ai/engine.py)      │
│  ✓ System prompt enforcement            │
│  ✓ Conversation memory management       │
│  ✓ Evidence-first reasoning             │
│  ✓ Hallucination detection              │
│  ✓ Confidence calibration               │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  Natural Language Investigation Results │
│  ✓ Structured reasoning output          │
│  ✓ Evidence traceback                   │
└─────────────────────────────────────────┘
```

### Key Separation Principles

**Blockchain data is NOT instructions.** Raw API responses are treated as untrusted data, normalized and validated before reaching the AI layer.

**The AI is NOT a blockchain.** The reasoning engine interprets evidence but cannot:
- Query additional data independently
- Access external APIs
- Execute transactions
- Change conclusions based on timing

**Evidence is the foundation.** Every claim must be traceable to:
1. Direct blockchain data (FACT)
2. Deterministic calculations from that data (DERIVED)
3. Visible patterns (OBSERVATION)
4. Reasonable interpretation (INTERPRETATION)
5. Or explicitly marked as UNKNOWN

---

## AI Security & Hallucination Risk

### The Problem: LLM Hallucination in Blockchain Analysis

**Why This Matters:**
- Users may make financial decisions based on the investigation
- Blockchain data is immutable; AI interpretations should not be
- Scam accusations based on false analysis could cause harm
- Supply-chain attacks on blockchain explorers can inject malicious data

### Our Mitigation Strategy

#### 1. **System Prompt Enforcement**

Your system prompt (in `ai/system_prompt.py`) is the primary defense. It explicitly:

- **Forbids fabrication** (24 hard prohibitions listed)
- **Requires evidence tracing** (FACT → DERIVED → OBSERVATION → INTERPRETATION)
- **Rejects correlation-as-causation** (common LLM error)
- **Handles uncertainty** (UNKNOWN is a valid answer)
- **Limits scope** (respects data limitations, doesn't extrapolate)

**Review the system prompt carefully.** Every restriction is there to prevent hallucination.

#### 2. **Input Sanitization**

Before evidence reaches the AI:

```python
# ✓ Type validation (parser.py)
def hex_to_int(value):
    if not isinstance(value, str):
        raise TypeError("hex_to_int() expects a string")
    if not value.startswith(("0x", "0X")):
        raise ValueError(f"Not a hexadecimal value: {value}")
    return int(value, 16)

# ✓ Null checks (formatter.py)
def hex_wei_to_eth(value):
    if value is None:
        return None
    # safe conversion
```

**Untrusted external data includes:**
- Token names and symbols
- Contract metadata
- Wallet labels
- Transaction calldata
- External API responses

#### 3. **Structured Evidence Buffer**

Blockchain data is converted to deterministic, validated JSON before the AI sees it:

```json
{
  "transaction": {
    "hash": "0xabc...",
    "block_number": 18500000,
    "timestamp": "15 Aug 2024, 10:30:45 UTC",
    "from_address": "0x123...",
    "to_address": "0x456...",
    "value_eth": "1.5",
    "token": "USDC",
    "token_decimals": 6,
    "category": "erc20"
  },
  "metadata": {
    "source": "Alchemy API",
    "query_time": "2024-08-15T10:35:00Z",
    "page_limit_reached": false,
    "data_confidence": "high"
  }
}
```

The AI receives this structured data, not free-form text.

#### 4. **Conversation Boundaries**

Memory management prevents context collapse:

```python
# Cap conversation at 15 messages
MAX_MESSAGES = 15

# Oldest messages deleted first (except system prompt)
if len(conversation) > MAX_MESSAGES:
    conversation[:] = [conversation[0]] + conversation[-(MAX_MESSAGES-1):]
```

**Why This Matters:**
- Prevents the AI from "remembering" false patterns across 100+ messages
- Keeps context window focused on current investigation
- Reduces cumulative hallucination risk

#### 5. **Fallback Model Strategy**

If the default model fails or is rate-limited:

```python
# ai/api.py
if response.status_code in [429, 500, 502, 503, 504]:
    print(f"Switching to fallback model: {FALLBACK_MODEL}")
    # Use a different, simpler model
    # Better to get a simple answer than a hallucinated one
```

The fallback model is more conservative—less prone to creative elaboration.

#### 6. **User-Supplied Claims Are Not Evidence**

If the user says "This wallet is a scammer," the system treats that as a hypothesis, not a fact:

```python
# From system prompt:
# "The user's statements may provide context or investigative hypotheses,
#  but they do not become blockchain facts merely because the user says them."
```

### Residual Risks (Be Honest)

Even with all mitigations, **some hallucination risk remains:**

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| AI invents token names | Low | Token names come from blockchain, not LLM |
| AI confuses addresses | Medium | Evidence shows exact addresses; AI can't "reinterpret" them |
| AI draws false connections | Medium | System prompt forbids correlation-as-causation |
| AI overconfident on incomplete data | High | System prompt requires acknowledgment of data limits |
| AI misunderstands user question | Low | Simple, direct prompts recommended |
| Prompt injection via calldata | Low | Calldata not passed to AI; only transfers included |

**Recommendation:** Treat Decyphra's output as a starting point for investigation, not a final verdict. Always verify against the primary blockchain evidence.

---

## System Prompt & Evidence-First Reasoning

### What Makes This Different

Most blockchain analysis tools either:
- **A)** Show raw data and expect users to decode it manually
- **B)** Use AI to analyze data, but don't distinguish fact from speculation

Decyphra does **C)**: Structure data intelligently, then reason over it with explicit evidence boundaries.

### The Reasoning Hierarchy

Every conclusion is classified:

- **FACT:** Directly from blockchain evidence (e.g., "This address received 15 transfers")
- **DERIVED:** Calculated from facts (e.g., "Total received: 50 ETH")
- **OBSERVATION:** Pattern visible in the data (e.g., "90% of transfers came from 3 addresses")
- **INTERPRETATION:** Reasonable explanation (e.g., "Suggests a concentrated relationship")
- **HYPOTHESIS:** Possible explanation needing more evidence (e.g., "Could indicate treasury distribution")
- **UNKNOWN:** Cannot be established from current data (e.g., "Reasons for the transfers")

**The AI never promotes a level without saying so explicitly.**

### Key Design Decisions

#### Principle 1: No Narrative-First Analysis

❌ **Bad approach:**
```
"This wallet is suspicious because:
1. Received a lot of money quickly
2. Sent it all out
3. Therefore it's probably a money launderer"
```

✅ **Good approach:**
```
OBSERVATION: Wallet received 50 ETH in 3 days, then sent 50 ETH out in 2 days.

INTERPRETATION: This is consistent with a treasury distribution, liquidity bootstrap,
or bridge activity.

HYPOTHESIS: Could also indicate rapid fund movement, which has multiple explanations.

UNCERTAINTY: The available data does not establish intent or purpose. Additional context
needed to distinguish between legitimate and suspicious patterns.
```

#### Principle 2: Respect Data Boundaries

If the blockchain API returns only 5 pages of history:
- ❌ AI should NOT claim "This wallet primarily does X"
- ✅ AI SHOULD say "During the observed period (500 most recent transfers), this wallet..."

If token data is missing:
- ❌ AI should NOT guess what FAKE_TOKEN is
- ✅ AI SHOULD say "Token transfer to unknown contract at 0xabc... (token metadata unavailable)"

#### Principle 3: Correlation ≠ Causation

Sending money to an exchange does NOT mean the user owns that exchange account.
Interacting with a suspicious contract does NOT mean the user was scammed.
Rapid transactions do NOT automatically prove bot activity.

### How to Read AI Output

When Decyphra investigates a wallet, look for:

1. **Explicit evidence references** – Is each claim backed by actual transaction data?
2. **Distinction between facts and interpretations** – Does the AI say "This wallet received X transfers" vs. "This wallet is likely used for X"?
3. **Uncertainty acknowledgment** – Does the AI admit what it doesn't know?
4. **Actionable next steps** – Does it suggest what additional data would improve the investigation?

If an output feels like speculation without evidence, it's a sign that the system prompt isn't working properly—report it.

---

## Current Limitations

### Honest Assessment of TRL 3 Status

Decyphra is an **experimental proof of concept**. It demonstrates the feasibility of the architecture but is not production-ready. These limitations are intentional.

### Blockchain Coverage

| Aspect | Status | Timeline |
|--------|--------|----------|
| Ethereum Mainnet | ✅ Supported | Now |
| L2s (Polygon, Arbitrum, Optimism) | ❌ Not supported | Phase 2  |
| Bitcoin, Solana | ❌ Not supported | Phase 3 |
| ERC20 tokens | ✅ Supported | Now |
| ERC721 (NFTs) | ⚠️ Partial | Limited metadata |
| ERC1155 (Multi-token) | ⚠️ Partial | Limited support |
| Contract interactions | ❌ Not supported | Phase 2  |
| Liquidity pool analysis | ❌ Not supported | Phase 3 |

### Data Limitations

| Limit | Value | Reason |
|-------|-------|--------|
| Transaction history | 5 pages × 500 transfers | API pagination limit; prevents analysis from overwhelming the AI |
| Time range | Last ~2 years | Older activity available but not retrieved by default |
| Balance queries | Not integrated | `get_balance()` exists but not called; WIP for Phase 2 |
| Token metadata | Partial | Only contract-provided data; no off-chain enrichment |
| Price history | Not supported | Cannot determine USD value at time of transfer |

### AI Reasoning Scope

Decyphra can:
- ✅ Summarize wallet activity patterns
- ✅ Identify repeated counterparties
- ✅ Detect unusual transaction frequency
- ✅ Distinguish transfers by asset type and direction
- ✅ Acknowledge uncertainty explicitly

Decyphra cannot:
- ❌ Identify the person controlling the wallet
- ❌ Prove criminal activity (requires law enforcement investigation)
- ❌ Evaluate intent (blockchain shows actions, not intent)
- ❌ Predict future behavior
- ❌ Provide legal or financial advice
- ❌ Replace specialized blockchain forensics tools

### Infrastructure Limitations

| Component | Limitation | Impact |
|-----------|-----------|--------|
| CLI only | No web UI | Limited user accessibility |
| Single-user | No authentication | Not suitable for shared use |
| Local memory | JSON file on disk | Not scalable; no cloud backup |
| Free-tier APIs | Rate limits apply | 300M compute units/month for Alchemy; 20 req/min for OpenRouter |
| No caching | Every query hits the API | Repeated investigations use quota |

### Known Issues

1. **Truncated history displays as complete**
   - FIXED: Data now includes `page_limit_reached` flag
   - AI is aware of truncation

2. **Token metadata inconsistencies**
   - Alchemy sometimes returns null decimals
   - MITIGATION: Defaults to 18 (ERC20 standard); AI warns when uncertain

3. **Address confusion**
   - Similar-looking addresses (different checksums) could confuse users
   - MITIGATION: Always show full address; highlight when multiple addresses appear similar

---

## Future Roadmap

For the full vision statement, see [README.md](README.md).

### Phase 1: Proof of Concept ✅ (Current)

### Phase 2: Investigation Intelligence 

**Goal:** Comprehensive investigation platform for a single user/research team.

### Phase 3: Advanced Intelligence

**Goal:** Production-grade platform for security teams and researchers.

### Phase 4: Product

**Goal:** Commercial product for enterprises and institutions.

### Current priorities:
- Multi-chain support (Solidity/ABI parsing)
- Token metadata enrichment
- Web API layer
- Test coverage (currently zero)

---

## Troubleshooting

### "API_KEY is missing from the environment"

**Problem:** `.env` file not found or `API_KEY` not set.

**Solution:**
```bash
# 1. Check .env exists
ls -la .env

# 2. If missing, copy from example
cp .env.example .env

# 3. Edit .env and add your Alchemy API key
nano .env  # or open in your editor

# 4. Make sure file is not empty
cat .env
```

### "OPENROUTER_API_KEY is missing"

**Problem:** OpenRouter API key not configured.

**Solution:**
```bash
# Edit .env and add:
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### "Error: Invalid wallet address"

**Problem:** Wallet address is not a valid Ethereum address.

**Solution:**
- Valid format: `0x` followed by 40 hexadecimal characters
- Examples: `0x1234567890123456789012345678901234567890`
- Copy directly from Etherscan; don't manually type

### "Rate limit exceeded / Too many requests"

**Problem:** Hit API rate limits.

**Solution:**
- Alchemy: 300M compute units/month
  - Check usage at https://dashboard.alchemy.com
  - Upgrade to Growth plan for higher limits
  - Wait 24 hours for daily quota reset

- OpenRouter: 20 requests/minute
  - Add a delay between investigations
  - Upgrade to paid tier for higher limits

### "No response from model"

**Problem:** OpenRouter API is unreachable or your API key is invalid.

**Solution:**
```bash
# 1. Test the API key
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{"model":"cohere/north-mini-code:free","messages":[{"role":"user","content":"test"}]}'

# 2. Check network connectivity
ping openrouter.ai

# 3. Verify API key is correct
cat .env | grep OPENROUTER
```

### "Transfer data is incomplete or truncated"

**Problem:** Wallet has more than 500 transfers; only recent ones shown.

**Expected behavior:** This is intentional. The system is designed to:
1. Show the 500 most recent transfers
2. Tell you about the truncation
3. Suggest that older activity is not analyzed

**Why:** Older activity is usually less relevant. Analyzing 10,000+ transfers would:
- Use too much API quota
- Overwhelm the AI reasoning layer
- Slow down investigation time

**Future improvement:** Phase 2 will add optional deep-dive mode for full history.

### "The AI seems to be hallucinating"

**Problem:** Output doesn't match blockchain evidence.

**Examples:**
- "This wallet sent 100 ETH to an exchange" (but you only see 10 ETH transfers)
- "Token is a well-known scam" (but there's no evidence of that in the data)

**Solution:**
1. **Always verify against primary source** – Check Etherscan directly
2. **Report the issue** with:
   - Wallet address
   - Exact output that was wrong
   - Screenshot of Etherscan evidence
3. **Cross-check the investigation data** – Run with `DEBUG=true` (if available) to see what evidence the AI received

**Root causes:**
- Truncated history makes recent activity look unusual
- Missing token metadata leads to wrong classification
- AI extrapolating beyond data boundaries (system prompt violation)

### "Can I use this for compliance/regulatory purposes?"

**Answer:** Not yet.

Decyphra is an experimental research tool. It is **not** suitable for:
- AML/KYC decisions
- Regulatory reporting
- Legal proceedings
- Financial decisions

Reasons:
- Data may be incomplete (Ethereum-only, 500 transfer limit)
- AI reasoning is not independently audited
- No guarantees about accuracy
- No liability framework

**Future:** Phase 4 will include compliance-grade investigation tools with audit trails and certification.

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

## Quick Reference: Environment Variables

```bash
# Blockchain Data API (Required)
API_KEY=your_alchemy_api_key_here

# AI Reasoning API (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional (defaults shown)
DEBUG=false
MAX_TRANSFER_PAGES=5
MAX_TRANSFERS_PER_PAGE=500
MAX_CONVERSATION_MESSAGES=15
MEMORY_FILE=memory/conversations.json
AI_MODEL=cohere/north-mini-code:free
AI_FALLBACK_MODEL=liquid/lfm-2.5-2.6b:free
```

---

## Support

- **Issues?** Open a GitHub issue with error logs and wallet address (you can redact it)
- **Feature requests?** Check the roadmap in [README.md](README.md) first
- **Security concerns?** Email privately (don't post publicly until fixed)

---

**Decyphra is an experimental tool. Use responsibly. Always verify findings against primary blockchain evidence.**
