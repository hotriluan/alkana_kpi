Activate `ak:agent-browser` for browser automation. If the task needs low-level
Chrome DevTools Protocol access, use Chrome MCP through `ak:use-mcp`.

## Purpose
Run comprehensive UI tests on a website and generate a detailed report.

## Arguments
- $1: URL - The URL of the website to test
- $2: OPTIONS - Optional test configuration (e.g., --headless, --mobile, --auth)

## Testing Protected Routes (Authentication)

For testing protected routes that require authentication, follow this workflow:

### Step 1: User Manual Login
Instruct the user to:
1. Open the target site in their browser
2. Log in manually with their credentials
3. Open browser DevTools (F12) → Application tab → Cookies/Storage

### Step 2: Extract Auth Credentials
Ask the user to provide one of:
- **Cookies**: Copy cookie values (name, value, domain)
- **Access Token**: Copy JWT/Bearer token from localStorage or cookies
- **Session Storage**: Copy relevant session keys

### Step 3: Inject Authentication
Use project-native browser test fixtures when available. If the project has
Chrome MCP configured, use `ak:use-mcp` to set cookies, headers, or localStorage
before navigating protected routes.

Record which authentication state was injected so the report is reproducible.

### Step 4: Run Tests
After auth injection, the browser session persists. Run tests normally:

```bash
# Navigate and screenshot protected pages with ak:agent-browser or Chrome MCP
# through ak:use-mcp.
```

### Auth Script Options
- `--cookies '<json>'` - Inject cookies (JSON array)
- `--token '<token>'` - Inject Bearer token
- `--token-key '<key>'` - localStorage key for token (default: access_token)
- `--header '<name>'` - Set HTTP header with token (e.g., Authorization)
- `--local-storage '<json>'` - Inject localStorage items
- `--session-storage '<json>'` - Inject sessionStorage items
- `--reload true` - Reload page after injection
- `--clear true` - Clear saved auth session

## Workflow
- Use `planning` skill to organize the test plan & report in the current project directory.
- All the screenshots should be saved in the same report directory.
- Browse $URL with the specified $OPTIONS, discover all pages, components, and endpoints.
- Create a test plan based on the discovered structure
- Use multiple `tester` subagents or tool calls in parallel to test all pages, forms, navigation, user flows, accessibility, functionalities, usability, responsive layouts, cross-browser compatibility, performance, security, seo, etc.
- Use `ai-multimodal` to analyze all screenshots and visual elements.
- Generate a comprehensive report in Markdown format, embedding all screenshots directly in the report.
- Finally respond to the user with a concise summary of findings and recommendations.
- Use `ask_user capability` tool to ask if user wants to preview the report with `/preview` slash command.

## Output Requirements
How to write reports:
- Format: Use clear, structured Markdown with headers, lists, and code blocks where appropriate
- Include the test results summary, key findings, and screenshot references
- **IMPORTANT:** Ensure token efficiency while maintaining high quality.
- **IMPORTANT:** Sacrifice grammar for the sake of concision when writing reports.
- **IMPORTANT:** In reports, list any unresolved questions at the end, if any.

**IMPORTANT**: **Do not** start implementing the fixes.
**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
