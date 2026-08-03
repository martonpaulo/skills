# Third-party notices

## mattpocock/skills (productivity/grilling)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/productivity/grilling`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. The 12-line original was rewritten; what remains is the method, not
the text.

### What was adapted

One question at a time with a wait for the answer, a recommended answer on every question,
resolving dependencies between decisions before the decisions they constrain, looking facts up
from the environment instead of asking, and treating decisions as the user's to make.

### What changed

**A skip condition.** Upstream always grills. This version states when not to: concrete, low-risk,
local, and reversible work.

**A materiality filter.** Questions are limited to decisions that affect behavior, scope,
architecture, data, security, compatibility, user experience, or irreversible cost. Reversible
preferences are settled from established project conventions instead of being put to the user.

**A stop condition.** Upstream is open-ended and relentless by design. This version stops once the
remaining uncertainty can be handled by reversible implementation choices, and explicitly forbids
continuing for exhaustiveness.

**A defined completion.** The session ends with a stated summary of understanding, assumptions,
constraints, decisions, and unresolved choices, so a caller skill can resume from it. Upstream
ended when the user said it had.

**Framing.** The adversarial register ("grill relentlessly") and the decision-tree metaphor were
dropped. This skill is delegated to by other skills in the collection and needed a neutral,
callable shape.
