# WorkMind Frontend

The React single-page application for WorkMind. It talks to the FastAPI
backend over REST and holds no business logic of its own.

For the project overview, architecture and deployment, see the
[root README](../README.md) and [docs/](../docs).

---

## Requirements

- Node.js 22+
- The backend running on `http://localhost:8000` (see the root README)

## Setup

```bash
npm install
cp .env.example .env
npm run dev
```

The dev server runs on `http://localhost:5173`.

## Configuration

One variable, read once at boot by `src/config/env.js`:

| Variable | Default | Purpose |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Base URL of the FastAPI backend |

Vite only exposes variables prefixed with `VITE_`. `.env` is gitignored;
`.env.example` is the tracked template.

## Scripts

| Script | Purpose |
|---|---|
| `npm run dev` | Dev server with hot module replacement |
| `npm run build` | Production build into `dist/` |
| `npm run preview` | Serve the production build locally |
| `npm run lint` | ESLint over the whole project |
| `npm run test` | Vitest in watch mode |
| `npm run test:run` | Vitest once — what CI runs |
| `npm run test:coverage` | Vitest with a v8 coverage report |

## Structure

```text
src/
├── api/            # One HTTP client + one module per resource
├── app/            # Route-level plumbing (ProtectedRoute)
├── components/
│   ├── chat/       # Message list, composer, conversation list and search
│   ├── layout/     # AppLayout, Sidebar, ProfileMenu, nav items
│   └── ui/         # Shared presentational pieces (Brand, Field, ...)
├── config/         # Environment and storage-key constants
├── context/        # AuthContext provider and its context object
├── hooks/          # useAuth
├── pages/          # One component per route
├── styles/         # theme.css plus per-area stylesheets
└── test/           # Vitest setup
```

### Conventions

- **All HTTP goes through `api/client.js`.** It attaches the bearer token,
  unwraps the backend's `detail` error field, and on a 401 clears the token
  and redirects to `/login`. Pages never call `fetch` directly.
- **Auth state lives in `AuthContext`.** The context object is declared in
  `context/auth-context.js`, separate from the provider component, so the
  provider file only exports a component and React Fast Refresh keeps working.
- **Routes are code-split.** `App.jsx` eagerly imports Login only; every other
  page is `lazy()`-loaded so signing in does not download the whole app.
- **Tests sit beside the code they cover** (`Login.jsx` / `Login.test.jsx`).

## Tests

```bash
npm run test:run
```

39 tests over the API client, route protection, and the Login, Chat,
ForgotPassword, ResetPassword and NotFound pages. They run in jsdom against
mocked `fetch` — no backend is required.
