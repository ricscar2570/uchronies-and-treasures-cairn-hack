# Information Hierarchy - Step 18

The A5 publication system now distinguishes four reader-facing content types without adding a new gameplay subsystem.

## RULE

Binding mechanical or procedural text. RULE labels use the primary red accent and a stable code such as `CORE-18` or `SET-04`. Each code has exactly one canonical source in the registry.

## PRINCIPLE

Adjudication guidance. PRINCIPLE labels use the blue accent. They explain how to preserve agency, causality, and transparency but do not replace the underlying procedure.

## EXAMPLE

Worked application. EXAMPLE labels use neutral grey. An example may clarify a sequence but cannot override a RULE.

## WARNING

Critical limits, irreversible thresholds, or easy-to-miss exceptions. WARNING labels use the warning accent.

## Source format

Markdown keeps a non-rendering marker immediately after the authoritative heading:

```html
<!-- UTRULE: CORE-18 | RULE | Damage sequence -->
```

The A5 builder converts it into a compact visual label. Web/plain Markdown remains readable, and the canonical registry can validate the source independently from PDF layout.

## Why codes are stable

Cross-references should use the procedure code before relying on a page number. Page numbers can change between A5, digital, operational, and future translated editions; `CONT-05` continues to mean the contamination-check procedure in every profile.
