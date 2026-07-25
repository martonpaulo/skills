---
name: grey-market
description: Find digital products (accounts, licenses, subscriptions, gift cards, templates, courses) sold far below the official price in regional markets — China, India, Brazil, Russia, Southeast Asia, Eastern Europe — by searching discussion communities, forums, messaging groups, and regional marketplaces instead of ordinary search engines. Use when the user asks for cheap keys or licenses, shared accounts, regional offers, loot deals, Brazilian PIX-friendly sellers, Turkish or Argentine gift cards, subscription splitting, or names a grey-market source such as Plati, 52pojie, DesiDime, GGMAX, or Desapego Games. Do not use for ordinary shopping research, for pirated software, or for anything that requires making a purchase.
metadata:
  upstream: https://github.com/felinto-dev/felinto-skills/tree/main/.agents/skills/grey-market
  upstream-author: felinto-dev
---

# grey-market

Digital grey-market researcher. Aggregates community intelligence to locate offers and
trustworthy sellers across Mandarin, Hindi, Portuguese, Russian, and English forums and groups.

This is a personal skill, not a project skill. It **locates discussions and sellers only** — it
never executes a transaction, enters payment details, or creates an account.

## Interview phase

Before any search, run a short interview to reach a shared understanding of the exact need.
Resolve one branch of the decision tree at a time. Stop as soon as further questions would not
change the search.

1. **Research before asking.** If the web can answer it — current global price, common product
   variants, which regions are cheapest right now, payment methods per region, known scams for
   this product — search first. Use the findings to skip questions and to frame sharper ones.
2. **One branch at a time.** Ask the next question only after the previous is resolved. Use
   `AskUserQuestion` for multiple-choice; put the recommended option first, labelled
   `(Recommended)`. Batch up to four questions only when they are independent.
3. **Always recommend an answer.** Never ask cold — lead with your best guess and a one-line
   reason.
4. **Scale to the request.** "Windows 11 Pro OEM key, China, crypto, $15" may need one
   confirmation; "cheap Netflix" needs several. Never re-ask what the user already stated.
5. **Detect refusals early.** If the interview reveals a request for cracks, keygens, pirated
   ISOs, or stolen accounts, stop and apply *When not to help*.

### Decision tree

- **Product and edition** — exact product, version, edition (Windows 11 Pro vs Home; Office 365
  vs 2021; Netflix Premium vs Standard).
- **Format** — digital key, shared account, top-up on the user's own account, gift card, ISO,
  template, course enrolment. Drives region and source.
- **Region** — any, or fixed? Tied to format (a Steam TR gift card implies Turkey).
- **Budget** — official global reference price versus an acceptable grey price.
- **Payment** — crypto, PayPal, AliPay via an agent, PIX, card, UPI (residents of India only).
  Rules out regions and sources.
- **Risk tolerance** — is peer-to-peer acceptable (Plati, 52pojie, Carousell), or is marketplace
  escrow required? Are shared accounts or grey keys acceptable, given revocation risk?
- **Delivery** — instant or willing to wait; by email or by account login.

The interview produces a spec. Hand it to the request workflow.

## Request workflow

The spec drives every step: product, edition, format, region, budget, payment, risk, delivery.

1. **Read the full market reference.** Read `references/markets.md` end to end every time. Do
   not skim by target region — global reputation checks, payment notes, dead-source warnings,
   and adjacent-region sources often change the best route.
2. **Build search terms.** Start in English, then adapt per region using the glossaries in
   `references/markets.md`.
3. **Optionally split the sweep.** For a broad request across several regions, splitting the
   work across parallel subagents is faster: shard by region and source family (global and
   commercial marketplaces; China and Mandarin sources; India and Russia/CIS; Southeast Asia,
   Brazil, and other local-payment sources). This is an optimization, not a requirement — a
   single-threaded sweep must reach the same result. If you do split, give each lane the full
   spec, the stack rules below, and the instruction to read all of `references/markets.md`; then
   deduplicate, prefer inspected pages over snippets and recent reputation evidence over stale
   mentions, and say which lane failed if one did.
4. **Run the sweep.** Two layers:
   - *Targeted* — for each relevant source, execute a real query.
     `scripts/dork-generator.sh` only **prints** `site:<domain> "<query>"` strings; it does not
     search. Execute each one through the search stack. For Telegram, use `tgstat.com` or the
     index bots listed in the reference.
   - *Broad* — run the raw product query without a `site:` operator, per region and language.
     This surfaces sellers, forums, and aggregators that are in no reference file; include them
     when relevant. When a marketplace blocks direct fetching, query around it — for example
     `"<domain>" <product> account price` — so third-party discussions of its pricing surface.
   - *Coverage check (hard rule).* Before writing the answer, confirm each source in the spec
     actually received an executed query. Generating a dork or listing a domain is not coverage.
     A source counts as covered only once a real query has run against it.
5. **Inspect candidate pages** through the site inspection stack before ranking. Extract direct
   offer links, seller name, level, feedback percentage, sales count, stock, delivery time,
   buyer protection, recent reviews, price, currency, and product caveats. Use this evidence to
   improve the recommendation, not just to bypass a blocked page.
6. **Evaluate reputation.** Prefer sellers with repeated mentions and positive feedback.
   Combine on-page seller data with payment method and buyer protection. For commercial
   marketplaces, cross-check with the reputation lookup tools in `references/markets.md`
   (`tested.gg`, per-domain Trustpilot pages, Krebs on Security for account-hijacking exposés).
   For community sources, use karma, likes, account age, and vouch channels.
7. **Convert the price.** Run `bash scripts/currency-converter.sh <CURRENCY> <amount>` for a BRL
   estimate. **Do not list any option priced at or above the official global price** — a grey
   option that costs as much as the official one is useless. If a region's cheapest option still
   exceeds official pricing, skip that region.
8. **Format the answer** as specified below.

## Search and inspection stacks

Both stacks are ordered by preference. Every layer below the first is a legitimate fallback —
use it and say so. None of these tools is a prerequisite for the skill.

### Web search

1. **SearXNG via Docker**, when Docker is available. Best for targeted dorks and broad sweeps.
   Always `docker run --rm`; stop the container after the query.
   ```bash
   cid=$(docker run --rm -d -p 127.0.0.1:18080:8080 searxng/searxng)
   curl -fsS -G "http://127.0.0.1:18080/search" --data-urlencode "q=site:g2g.com ChatGPT Plus account"
   docker stop "$cid"
   ```
   If `format=json` returns 403, fetch the HTML results page and parse titles and links.
2. **AnySearch**, only when `ANYSEARCH_API_KEY` is set in a `.env` file or the environment.
   ```bash
   python3 scripts/anysearch.py "windows 11 pro key cheap" --max_results 10 --tag general.general
   python3 scripts/anysearch.py "netflix account sharing" --language zh-CN --zone cn
   ```
   Useful tags: `general.general`, `social_media.social_media`, `business.company`. If the key
   is absent, skip this layer silently — do not ask the user to configure it unless they want it.
3. **Native web search** — the fallback that always exists.

If a query fails or returns nothing useful at one layer, retry it at the next before declaring
the source uncovered. Record which layer covered each source.

### Site inspection

1. **Lightpanda via Docker**, when Docker is available. Preferred for marketplace, category,
   search, offer, and seller pages, which routinely bot-block plain fetching.
   ```bash
   docker run --rm lightpanda/browser:nightly lightpanda fetch \
     --wait-until networkidle --wait-ms 15000 --terminate-ms 25000 \
     --dump markdown --strip-mode js,css,ui,invisible "https://example.com/offer"
   ```
2. **Native page fetch** — when Docker is unavailable, or Lightpanda fails, times out, or
   renders incomplete content.

Use search-result snippets only when both layers fail, and say which failed.

## Quick search terms

Use these rather than literal translation:

- **China** — `正版` genuine · `激活码` activation code · `白嫖` get free · `账号分享` shared
  account · `便宜` cheap · `拼车` group buy
- **India** — `loot deal` · `cheap key` · `Udemy free` · `regional pricing`
- **Russia/CIS** — `дешевый ключ` cheap key · `ключ активации` activation key · `аккаунт`
  account · `раздача` giveaway
- **Southeast Asia** — `digital key` plus country (MY/TH/ID) · `top up murah` (Indonesian)
- **Brazil** — `conta` · `chave` · `licença digital` · `gift card` · `recarga` · `PIX` ·
  `é confiável` · `Reclame Aqui`
- **Global** — `grey market` · `reseller` · `regional key` · `account sharing`

Full glossaries are in `references/markets.md`.

## Output format

```markdown
## <product> — <target region>

| # | Product/Seller | Local price | BRL | Source | Trust | Payment |
|---|---|---|---|---|---|---|
| 1 | Windows 11 Pro OEM | ¥12 | R$ 8.40 | [52pojie](url) | Medium | AliPay |

Notes:
1. Seller appears in 3+ threads; marketplace payment protects the buyer...

Best bet: #X — reason.
```

Rules for the table: always include the exact discussion link; only include options cheaper than
the official global price; flag any source not in `references/markets.md` with
`(new — not in references)` and lean harder on the reputation lookup tools before recommending
it. If every option found costs at least as much as the official price, say so and recommend the
official source instead of padding the table. After the notes, list high-value new sources
discovered this run and suggest adding them to `references/markets.md` — do not edit reference
files mid-search.

If no viable source is found, say so. Never invent links.

Close with one line: *this skill locates discussions; it does not process payment. Verify seller
reputation before sending any funds.*

## When not to help

Do not locate cracks, keygens, pirated ISOs, stolen accounts, carded purchases, malware, or
exploits. Those are not grey-market goods; they are theft and fraud. Decline in a sentence,
without lecturing, and offer a legal low-cost alternative — regional OEM pricing, household
account sharing, an education discount, or an extended trial.

Never enter payment details, never create an account, and never complete a purchase. Hand the
user the link and let them decide.

## Maintenance

`scripts/exchange-rates.json` holds spot rates against BRL and goes stale. Check the rates
before quoting a converted price and refresh the file when they look wrong.
`scripts/currency-converter.sh` requires `jq`.

## Attribution

Adapted from [felinto-dev/felinto-skills](https://github.com/felinto-dev/felinto-skills/tree/main/.agents/skills/grey-market).
See `THIRD_PARTY_NOTICES.md`.
