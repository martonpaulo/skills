# Domain Glossary Format

Use the repository's existing format when present. Otherwise keep `CONTEXT.md` compact:

```markdown
# Domain Context

## Vocabulary

### Order

A customer's confirmed request for one or more products.

Related to: Customer, Order Line

## Rules and relationships

- An Order belongs to one Customer.
- A cancelled Order cannot transition back to confirmed.
```

Include only terms, states, rules, and relationships that are specific and useful to the project. Define each term in one or two precise sentences. Record avoided synonyms only when they prevent a real ambiguity.

Use multiple glossary files or a context map only when the repository already has distinct domain contexts with different vocabulary or ownership.
