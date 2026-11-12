# Habitats – Cloudflare Scheduler Deployment

This guide explains how to deploy or redeploy the Cloudflare Worker responsible for triggering the hourly sensor collection workflow.

## 1. Architecture

The scheduler uses three components:

- **Cloudflare Cron Trigger:** Determines when the collection runs.
- **Cloudflare Worker:** Sends a request to GitHub to trigger the collection workflow.
- **GitHub Actions:** Executes `habitats/collect_readings.py`, which retrieves Aqara readings and stores them in Cloudflare D1.

Cloudflare does not execute the Python script directly.

## 2. Repository files

The relevant files are:

```text
database/
    schema.sql
    scheduler.js
    wrangler.toml

habitats/
    collect_readings.py

.github/
    workflows/
        collect-readings.yml
```

## 3. Prerequisites

- Node.js installed (includes `npx`).
- Access to the Cloudflare account.
- A GitHub fine-grained personal access token.

The GitHub token must have:
- Repository access: `habitats` only.
- Repository permissions: `Actions – Read and write`.

The token allows the Worker to trigger GitHub Actions.

## 4. Deploy the Worker

Open a terminal in the local repository root and run:

```bash
npx wrangler deploy --config database/wrangler.toml
```

If prompted:
- Install Wrangler if necessary.
- Authenticate with Cloudflare through the browser.

Wrangler reads the configuration and deploys the Worker named `habitats-scheduler`.

## 5. Configure the GitHub token

The Worker requires a secret named `GITHUB_TOKEN`.

1. Open Cloudflare Dashboard.
2. Navigate to Workers & Pages.
3. Select `habitats-scheduler`.
4. Open Settings → Variables and Secrets.
5. Add a secret:
   - Name: `GITHUB_TOKEN`
   - Value: Your GitHub personal access token.
6. Save.

Never commit the token to GitHub or put it in `scheduler.js`.

## 6. Configure the schedule

The schedule is defined in `database/wrangler.toml`:

```toml
[triggers]
crons = ["0 * * * *"]
```

This runs the Worker every hour, at minute 0 (UTC).

After changing the schedule, deploy again:

```bash
npx wrangler deploy --config database/wrangler.toml
```

## 7. Verify deployment

1. Open Cloudflare Dashboard → Workers & Pages → `habitats-scheduler`.
2. Check that the Worker is deployed and the Cron Trigger is configured.
3. Open [GitHub Actions](https://github.com/BenjaSanchez/habitats/actions).
4. Wait for the next scheduled execution.
5. Verify that `Collect sensor readings` starts and completes successfully.
6. Check that new readings appear in the D1 `readings` table.

## 8. Updating the GitHub token

If the GitHub token expires or is regenerated, update the existing Worker secret using either the Cloudflare dashboard or:

```bash
npx wrangler secret put GITHUB_TOKEN --config database/wrangler.toml
```

A new deployment is not normally required just to update a secret.

## Important notes

- The GitHub Actions workflow must retain its `workflow_dispatch` trigger.
- The Worker dispatches the workflow on the `main` branch.
- Cron schedules use UTC.
- Deploying the Worker does not manually execute the collection workflow.
- Existing Worker secrets are retained across normal code deployments.
