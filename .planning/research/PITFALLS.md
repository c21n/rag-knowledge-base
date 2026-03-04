# Domain Pitfalls

**Domain:** RAG Knowledge Base System
**Researched:** 2026-03-04

## Critical Pitfalls

Mistakes that cause major rewrites or significant issues.

### Pitfall 1: Poor Text Chunking Strategy
**What goes wrong:** Answers miss context because chunks cut mid-sentence or lose semantic boundaries
**Why it happens:** Default chunk sizes don't match content structure
**Consequences:** Low-quality retrieval, incomplete answers
**Prevention:** 
- Use semantic boundaries (paragraphs, sections)
- Include overlap between chunks (50-100 chars)
- Test with real documents
- Monitor retrieval quality

**Detection:** Users report "answer doesn't match document" or missing context

### Pitfall 2: Wrong Embedding Model
**What goes wrong:** Semantic search returns irrelevant documents
**Why it happens:** Using general embeddings for domain-specific content
**Consequences:** Poor retrieval, useless answers
**Prevention:**
- Use text-embedding-ada-002 or better for general content
- Consider fine-tuning for specialized domains
- Test retrieval with real queries
- Measure hit rate on expected documents

**Detection:** Top-K results consistently irrelevant to query

### Pitfall 3: Prompt Injection Vulnerabilities
**What goes wrong:** Users manipulate system through crafted prompts
**Why it happens:** No input validation, direct LLM exposure
**Consequences:** Security issues, data exposure
**Prevention:**
- Validate and sanitize user input
- Use system prompts carefully
- Implement rate limiting
- Never expose raw LLM to untrusted input

**Detection:** Unusual system behavior, attempts to override instructions

## Moderate Pitfalls

### Pitfall 1: Ignoring Token Limits
**What goes wrong:** Context too long for LLM, truncated or rejected
**Why it happens:** Not calculating tokens before sending
**Consequences:** Failed requests, missing context
**Prevention:**
- Calculate context size before LLM call
- Implement smart truncation strategies
- Set max chunk limits
- Monitor token usage

### Pitfall 2: No Error Handling for LLM Failures
**What goes wrong:** App crashes or hangs when OpenAI is down/rate-limited
**Why it happens:** Assuming API always works
**Consequences:** Poor UX, unhandled exceptions
**Prevention:**
- Implement retries with exponential backoff
- Handle rate limits gracefully
- Provide fallback messages
- Log all failures

### Pitfall 3: Synchronous LLM Calls
**What goes wrong:** UI freezes during LLM generation (can take 10-30s)
**Why it happens:** Blocking HTTP requests
**Consequences:** Terrible UX, timeout errors
**Prevention:**
- Use async/await throughout
- Implement streaming responses
- Show progress indicators
- Set appropriate timeouts

### Pitfall 4: Storing API Keys in Code
**What goes wrong:** Keys committed to git, security breach
**Why it happens:** Convenience during development
**Consequences:** API abuse, cost, revocation needed
**Prevention:**
- Use environment variables exclusively
- Add .env to .gitignore
- Never log API keys
- Rotate keys regularly

## Minor Pitfalls

### Pitfall 1: No Conversation Persistence
**What goes wrong:** History lost on page refresh
**Why it happens:** State only in memory/React state
**Consequences:** Frustrated users
**Prevention:** Persist conversations to database from start

### Pitfall 2: Missing Source Attribution
**What goes wrong:** Users can't verify answers
**Why it happens:** Not including metadata in response
**Consequences:** Low trust in system
**Prevention:** Always return sources with answers

### Pitfall 3: File Upload Without Validation
**What goes wrong:** Crashes on corrupted files, security issues
**Why it happens:** Trusting user uploads
**Consequences:** App crashes, potential exploits
**Prevention:**
- Validate file types
- Check file sizes
- Handle parse errors gracefully
- Scan for malware (if public)

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Document Processing | Parser failures on complex PDFs | Use multiple parsers, graceful degradation |
| Vector Store Setup | Wrong distance metric | Use cosine similarity for embeddings |
| RAG Chain | Context window overflow | Monitor token count, implement truncation |
| Frontend Integration | CORS issues | Configure FastAPI CORS properly |
| Deployment | Environment variables not set | Create .env.example, validate on startup |
| Performance | Slow vector search | Index optimization, batch processing |

## Testing Recommendations

### Retrieval Quality Testing
```python
# Test that queries return expected documents
test_cases = [
    ("how to reset password", ["user_manual.pdf"]),
    ("vacation policy", ["hr_handbook.docx"]),
]
```

### Load Testing
- Simulate multiple concurrent users
- Test with large documents (100+ pages)
- Monitor response times

### Error Scenario Testing
- OpenAI API down
- Malformed documents
- Very large queries
- Special characters in documents

## Sources

- RAG system failure analysis
- LLM production best practices
- OpenAI API guidelines
- Document processing edge cases
