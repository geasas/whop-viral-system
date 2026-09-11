# Update and Deliver — How to Package Knowledge Updates

> **Purpose**: After research is done, the knowledge must be packaged and delivered to the user in a way they can verify, integrate, and use. This is the protocol for that final step.

---

## The Premise

Bad delivery destroys good research. If the user can't understand what was learned, can't trust the new file, or can't verify the sources, the research was wasted effort.

This protocol ensures:
1. The user can verify what was researched
2. The user can integrate the new file into the system
3. The user can re-trigger research if the file is stale
4. The system stays auditable — every claim can be traced to a source

---

## Step 1: File Creation

After synthesis (per `00_META/research_protocol.md` Stage 5), the file is saved to the appropriate layer.

### Naming convention

- Lowercase, snake_case
- Domain-specific prefix where useful (e.g., `egypt_*` for Egypt-specific files, `electrical_*` for electrical-specific)
- Descriptive name, not clever name

Examples:
- `egypt_electrical_market.md` (good)
- `egypt_litigation_basics.md` (good)
- `stuff_about_contracts.md` (bad)
- `TheUltimateGuide.md` (bad)

### File header

Every file begins with this header:

```markdown
# [File Title]

> **Layer**: [00-16]
> **Sublayer**: [if applicable, e.g., contracting/, spiritual/]
> **Created**: [YYYY-MM-DD]
> **Last reviewed**: [YYYY-MM-DD]
> **Next review**: [YYYY-MM-DD + 6 months]
> **Origin**: [User question on YYYY-MM-DD that triggered this file, OR "Foundational file"]
> **Confidence**: [low/medium/high]
> **Source tiers used**: [e.g., Tier 1, Tier 3 — see 00_META/book_selection_criteria.md]
```

This header is mandatory. It allows the user to see at a glance:
- What this file is
- Where it lives in the architecture
- When it was created and needs review
- Why it exists
- How confident the system is in its contents
- What types of sources it draws from

---

## Step 2: Update the Index

After creating a file, update `/home/z/my-project/STRATEGIC_MIND/manifest.md`:

### If the file is in an existing layer:

Append to the layer's table:
```
| new_file_name.md | Brief description | word_count |
```

### If the file is in a new sublayer:

Add a new subsection in the layer's documentation:
```
### new_sublayer_name/ (N files)
- file_1.md
- file_2.md
```

### If the file creates a new layer:

This should NOT happen — layer architecture is fixed at 16. If a file doesn't fit any layer, the user and I need to redesign.

---

## Step 3: Deliver to the User

The delivery message has this structure:

```
## Knowledge Update — [Topic]

**New file**: /path/to/file.md
**Updated files**: [list, if any]
**Time spent**: [hours]
**Sources consulted**: [number] (Tier 1: X, Tier 2: Y, Tier 3: Z, Tier 4: W)

### The core principle (1 paragraph)

[Distilled synthesis.]

### The 3 most surprising things I learned

1. [Surprise 1]
2. [Surprise 2]
3. [Surprise 3]

### Where experts disagreed

[If applicable, the key tension in the field.]

### What I still don't know

1. [Gap 1]
2. [Gap 2]

### Confidence: [low/medium/high]

[Explanation of why this confidence level.]

### Recommended next questions

[2-3 follow-up questions the user might want to ask now.]

### Source list

[Full citations with tier annotations.]
```

This delivery is NOT just a file dump. It's a **briefing** — the user gets the value of the research without having to read the file unless they want depth.

---

## Step 4: Versioning

Files change over time as knowledge evolves. Versioning rules:

### Minor update (small clarification, typo, example)
- Update the file
- Bump `Last reviewed` date
- No need to inform user unless the change affects a decision they've already made

### Substantive update (new sources, new principle, new application)
- Update the file
- Bump `Last reviewed` date AND `Next review` date (push by 6 months from update)
- Inform user with a brief "Update to [file]" message
- Add a changelog entry at the bottom of the file:
  ```
  ## Changelog
  - [YYYY-MM-DD]: Added source [X] and revised principle [Y]. Confidence raised from low to medium.
  - [YYYY-MM-DD]: Initial creation.
  ```

### Major revision (file is largely rewritten)
- Treat as a new version (v2, v3, etc.)
- Save old version as `file_v1.md` for reference (in an `_archive/` subfolder)
- Inform user with full briefing

---

## Step 5: Review Queue

Every file has a "Next review" date. The system maintains a review queue.

When the user asks a question and a relevant file is past its review date, the system should:
1. Note that the file is overdue for review
2. Offer: "This file was last reviewed [date]. Want me to refresh it before answering?"

This prevents knowledge rot. Files that aren't reviewed become stale, and stale knowledge is more dangerous than no knowledge.

### What "review" means:
- Check if the cited sources are still current
- Check if new sources have appeared that contradict or extend the file
- Check if the user's situation has changed (e.g., moved from 1 project to 5 projects, scaling rules need updating)
- Check if recent events (economic, regulatory) have changed the application

---

## Step 6: Re-delivery (after review)

After a file is reviewed and updated, deliver a brief update:

```
## Knowledge Refresh — [Topic]

The file [path] has been reviewed and updated.

### What changed
- [Change 1]
- [Change 2]

### What's new in the field since last review
- [New source 1]
- [New development 2]

### Impact on previous advice I gave you
- [If any past advice is now outdated, flag it]
```

This is important: if past advice is now outdated, the user needs to know. A confident answer 6 months ago may have been right then but wrong now. Honesty about this is critical.

---

## The Integrity Test

Before delivering any file, the system asks itself:

1. **Can the user verify every claim?** (Are sources cited?)
2. **Can the user see my reasoning?** (Did I show the mechanism, not just the conclusion?)
3. **Does the user know my confidence level?** (Is it stated?)
4. **Does the user know what I don't know?** (Are gaps explicit?)
5. **Can the user push back?** (Did I invite critique?)

If any answer is no, the delivery is incomplete. Revise before sending.

---

## Anti-Patterns

### Anti-Pattern 1: The silent update
Updating a file without telling the user. The user has no idea what changed. They may have made decisions based on the old version.

### Anti-Pattern 2: The unsourced file
A file with no source citations. The user can't verify, and the file degrades to "trust me bro."

### Anti-Pattern 3: The over-confident delivery
Delivering an answer with "high confidence" when the file is actually low-confidence. Misleads the user.

### Anti-Pattern 4: The never-reviewed file
A file created in 2026, never reviewed. By 2028 it's stale but still being cited. Knowledge rot.

### Anti-Pattern 5: The comprehensive dump
Delivering the entire file content to the user. The user doesn't have time. Deliver the synthesis; the file is for reference.

---

## The Final Rule

**Knowledge delivery is a service, not a download.** The user is not a recipient of a file; they are a partner in the knowledge. The system's job is to make sure they can use the knowledge well — not to dump it on them and move on.

---

## File History

- Created: 2026-09-09
- Version: 1.0
- Review: 2027-03-09
