# Skill Domain Routing

When a user's task involves a specific domain, use these decision trees to pick the RIGHT skill based on user intent.

## Frontend / UI

```
User wants to...
├── Replicate a mockup, screenshot, or video    → /ak:frontend-design
├── Build React/TS components with best practices → /ak:frontend-development
├── Style with Tailwind CSS + shadcn/ui          → /ak:ui-styling
├── Choose colors, fonts, layout, design system  → /ak:ui-ux-pro-max
├── Audit existing UI for accessibility/UX       → /ak:web-design-guidelines
├── Apply React performance patterns             → /ak:react-best-practices
├── Build with Stitch (AI design generation)     → /ak:stitch
├── Create 3D / WebGL / Three.js experience      → /ak:threejs
├── Write GLSL shaders / procedural graphics     → /ak:shader
└── Build programmatic video with Remotion       → /ak:remotion
```

## Codebase Understanding

```
User wants to...
├── Quick file search, locate specific code     → /ak:scout
├── Onboard a new repo / dump codebase for LLM  → /ak:repomix
├── Semantic go-to-definition, find-usages      → /ak:gkg
└── Build a queryable knowledge graph from code → /ak:graphify
```

## Backend / API

```
User wants to...
├── Build REST/GraphQL API (NestJS, FastAPI, Django) → /ak:backend-development
├── Add authentication (OAuth, JWT, passkeys)        → /ak:better-auth
└── Integrate payments (Stripe, Polar, SePay)        → /ak:payment-integration
```

## Database

```
User wants to...
├── Design schemas, write SQL/NoSQL queries     → /ak:databases
├── Optimize indexes, migrations, replication   → /ak:databases
└── Add auth with database-backed sessions      → /ak:better-auth
```

## Infrastructure / Deployment

```
User wants to...
├── Deploy to Vercel, Netlify, Railway, Fly.io   → /ak:deploy
└── Docker, Kubernetes, CI/CD pipelines, GitOps   → /ak:devops
```

## Security

```
User wants to...
├── STRIDE/OWASP security audit with auto-fix    → /ak:security
├── Scan for secrets, vulnerabilities, OWASP patterns → /ak:security-scan
└── OSINT / CTI / threat-intel investigation     → /ak:cti-expert
```

## AI / LLM

```
User wants to...
├── Optimize context, agent architecture, memory → /ak:context-engineering
├── Generate llms.txt, LLM-friendly docs         → /ak:llms
├── Build AI agents with Google ADK              → /ak:google-adk-python
├── Generate/analyze images, audio, video with AI → /ak:ai-multimodal
└── Learn the autoresearch pattern / find the right family member → /ak:autoresearch
```

## MCP (Model Context Protocol)

```
User wants to...
├── Build a new MCP server                       → /ak:mcp-builder
├── Convert existing code into CLI/MCP server    → /ak:agentize
└── Discover and execute MCP tools               → /ak:use-mcp
```

## Testing / Browser

```
User wants to...
├── Run test suites, coverage reports, TDD          → /ak:test
├── Test strategy + Playwright/Vitest/k6 runner     → /ak:web-testing
└── Drive a live browser                            → /ak:agent-browser
```

## Media

```
User wants to...
├── Process video/audio (FFmpeg), images (ImageMagick) → /ak:media-processing
└── Generate AI images (Imagen, Nano Banana)           → /ak:ai-artist
```

## Documentation

```
User wants to...
├── Update project docs (codebase-summary, PDR)   → /ak:docs
├── Search library/framework docs (context7)      → /ak:docs-seeker
├── Discover skills by capability / "is there a skill" → /ak:find-skills
├── Build docs site with Mintlify                 → /ak:mintlify
├── Inline doc diagrams (Mermaid v11)             → /ak:mermaidjs-v11
├── Publish-grade SVG/PNG diagrams (architecture) → /ak:tech-graph
├── Read long-form docs / RFCs / specs in browser → /ak:markdown-novel-viewer
├── Generate session hand-off / EOD summary       → /ak:watzup
└── Sprint retrospective from git history         → /ak:retro
```

## Documents / Office Files

```
User wants to...
├── Create / edit / extract from .docx (Word)         → /ak:docx
├── Create / edit / extract from .pdf (forms, tables) → /ak:pdf
├── Create / edit / extract from .pptx (PowerPoint)   → /ak:pptx
└── Create / edit / extract from .xlsx (spreadsheets) → /ak:xlsx
```

## Content / Copy

```
User wants to...
├── Write landing page, email, headline copy     → /ak:copywriting
├── Brand identity, logos, banners               → /ak:design
└── Create Excalidraw diagrams                   → /ak:excalidraw
```

## Frameworks

```
User wants to...
├── Next.js App Router, RSC, Turborepo           → /ak:web-frameworks
├── TanStack Start/Form/AI                       → /ak:tanstack
├── React Native, Flutter, SwiftUI               → /ak:mobile-development
└── Shopify apps, Polaris, Liquid templates       → /ak:shopify
```

## Usage Notes

- Pick ONE skill per distinct user intent
- If a task spans two domains (e.g. "build + deploy"), suggest the primary skill and mention the secondary
- Domain skills combine with core workflow: `/ak:plan` → domain skill → `/ak:cook`
- Skills not listed here are either core workflow skills (see `skill-workflow-routing.md`) or utility skills activated on demand (e.g. `/ak:ask`, `/ak:preview`, `/ak:sequential-thinking`)
