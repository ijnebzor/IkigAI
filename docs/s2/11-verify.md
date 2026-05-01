# S2 — 11 — Verify

> The "you're done with S2 when X" criteria.
> Run these checks. If everything passes, S2 is shipped and you can move to S3.

## Health-check matrix

Run each. ✓ = passing. ✗ = problem to fix before declaring S2 done.

### 1. NUC reachable on Tailscale

```bash
# From your laptop
tailscale status | grep nuc
ping -c 3 <nuc-tailscale-name>
ssh <nuc-tailscale-name> 'whoami'
```
- ✓ NUC visible in tailnet
- ✓ Pings succeed
- ✓ SSH works without password

### 2. Ollama responding

```bash
# On NUC or anywhere on tailnet
curl http://<nuc-ip>:11434/api/tags
```
- ✓ Returns JSON listing `llama3.2` and `nomic-embed-text`

### 3. Docker stack healthy

```bash
ssh <nuc> 'cd ~/IkigAI/docs/s2 && docker compose ps'
```
- ✓ All daemons `running` (or `healthy` if they have healthchecks)
- ✓ No `restarting` or `exited`

If anything's restarting, check its logs:
```bash
docker compose logs <daemon-name> --tail 50
```

### 4. Vault structure correct

```bash
ssh <nuc> 'ls ~/ikigAI-me/'
```
- ✓ `CLAUDE.md`, `ikigai.md`, `lexicon.md`, `config.yml` present
- ✓ `inbox/` with subfolders web, voice, email, chat, tabs, ideas, unsorted
- ✓ `wiki/` with subfolders sources, concepts, entities, projects, ideas, outputs
- ✓ `log.md` exists

### 5. Index initialised

```bash
ssh <nuc> 'ls ~/ikigai-state/index/'
```
- ✓ `chroma/` directory non-empty
- ✓ `graph.json` present

### 6. THE WATCHER processes new files

```bash
ssh <nuc>
echo "# Smoke test\n\nThis is a test capture for verifying S2." > ~/ikigAI-me/inbox/unsorted/smoke-test.md
sleep 60
ls ~/ikigAI-me/wiki/sources/ | grep -i smoke
```
- ✓ A canonicalised page appears within 60 seconds
- ✓ `~/ikigAI-me/inbox/unsorted/.processed/smoke-test.md` shows the input was moved

### 7. THE SCOUT produces queue entries

After at least 5 pages exist:
```bash
docker exec ikigai-the-scout python /daemons/the-scout.py
ls ~/ikigai-state/index/scout_queue.jsonl
tail ~/ikigai-state/index/scout_queue.jsonl
```
- ✓ Queue file exists
- ✓ Entries with `type: linkage` (or admission of no linkages)

### 8. THE KEEPER produces lint report

```bash
docker exec ikigai-the-keeper python /daemons/the-keeper.py
ls ~/ikigAI-me/state/lint-*.md
```
- ✓ Today's lint report exists
- ✓ Sections for schema_violations, orphans, dead_links, etc

### 9. THE HERALD produces a brief

```bash
docker exec ikigai-the-herald python /daemons/the-herald.py
ls ~/ikigAI-me/wiki/outputs/brief-*.md
cat ~/ikigAI-me/wiki/outputs/brief-$(date +%Y-%m-%d).md
```
- ✓ Today's brief exists
- ✓ Has "Where you've been compounding" section
- ✓ Has voice signoff matching `me/config.yml`

### 10. MCP server reachable

```bash
# From your laptop, test the SSH bridge
ssh <nuc> '/home/<nuc-user>/bin/ikigai-mcp-bridge' < /dev/null
```
- ✓ Outputs MCP server banner to stderr (or, on stdin EOF, exits cleanly)
- ✓ No "container not found" or permission errors

### 11. Claude Desktop sees IkigAI tools

In Claude Desktop:
1. Restart the app
2. Click the MCP indicator (bottom-right of input)
3. Confirm `ikigai` is listed with 7 tools

In a new chat:
> Use ikigai_brief_today and tell me what's in today's brief.

- ✓ Returns the brief content (not "no_brief_today")

### 12. Real retrieval works

After Phase 0 (or after at least 10 pages exist):

> Use ikigai_retrieve with query "compounding visibility" gear=2

- ✓ Returns a `trail` with at least 1-3 page entries
- ✓ Page IDs match real files in `wiki/sources/`

### 13. Calendar daemon (if Google OAuth done)

```bash
docker compose logs the-scribe --tail 20
ls ~/ikigAI-me/wiki/calendar/
```
- ✓ Logs show successful pull
- ✓ At least one calendar event file written

### 14. Gmail daemon (if Google OAuth done)

```bash
docker compose logs the-gatekeeper --tail 20
```
- ✓ Logs show "0 unread on label" or successful processing
- ✓ No auth errors

Send yourself a test email matching your IkigAI label filter, wait ~90s, then:

```bash
ls ~/ikigAI-me/inbox/email/
```
- ✓ Email body present as markdown

### 15. Phase 0 corpus exists

```bash
ssh <nuc> 'ls ~/ikigAI-me/wiki/sources/ | wc -l'
```
- ✓ ≥50 sources (Phase 0 floor)

## The end-to-end test

The ultimate smoke test. Do this from your phone (Claude Desktop iOS):

1. **Capture a thought:**
   > Use ikigai_capture with type=thought: "The framework overlay only earns its keep if compounding visibility produces an action I wouldn't have taken otherwise."

2. **Wait 60 seconds.**

3. **Retrieve:**
   > Use ikigai_retrieve with gear 2: "what have I said about whether IkigAI works"

4. **The thought you captured should appear in the trail.**

If steps 1-4 all succeed: **S2 is shipped.**

## Troubleshooting cheat sheet

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Daemons restart loop | Missing volume mount | Check `04-docker-compose.yml` paths |
| `understand` fails JSON parse | llama3.2 not in JSON mode | Check Ollama version supports `format: json` |
| Empty Chroma after captures | Embeddings failing | `docker exec ikigai-the-watcher python -c "import ollama; print(ollama.Client().embeddings(...))"` |
| Brief is empty | No projects with `project_status: active` | Add at least one project page |
| MCP tools missing in Claude Desktop | Config JSON invalid | `cat ~/Library/.../claude_desktop_config.json | jq` |
| Gmail "label not found" | Label name mismatch | Exact case-sensitive match required |
| Calendar pull empty | Wrong calendar | THE SCRIBE uses `primary` — adjust if your default isn't your work calendar |

## When NOT to declare S2 done

- If THE WATCHER is processing >30 seconds per file consistently — Ollama is too slow on your hardware. Either upgrade RAM or use a smaller model (mistral 7b, gemma 2 2b).
- If lint shows >100 schema violations after Phase 0 — your CLAUDE.md or ikigai.md probably has a parsing bug feeding bad context to /understand. Fix and re-run.
- If MCP retrieval returns empty for queries you know have matching content — vector index is desynced. Force reindex with `docker compose restart the-watcher` and re-process inbox.
- If a daemon is healthy but "not doing anything" — check `docker compose logs <daemon>` for errors swallowed by exception handlers.

## After S2

You go to S3 (Coach Experience). Documented in `roadmap-reference.html#s3`. Roughly:
- Three retrieval gears with real classifier
- Web viewer at `http://<nuc>/`
- Brusselbach diagram interactive with live region fill
- Daily 07:30 brief lands consistently (THE HERALD already runs; S3 is about polish + voice + idea-flow)
- /phase-an-idea reads idea + vault + projects + calendar, offers slot

S3 is a different kind of work: less infra, more product polish. Single sustained Saturday.
