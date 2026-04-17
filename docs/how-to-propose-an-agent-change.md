# How to Propose an Agent Change

Agents in this repo are versioned markdown files. They get better the same way any other code gets better: someone notices a defect, opens a pull request, and a human reviews the change before it lands. Agents do **not** edit each other. Agents do **not** edit themselves. Improvements are a deliberate human act.

## When to Propose a Change

Open a PR against an agent file when you observe, across one or more runs:

- The agent consistently misses something it should catch (missed counter-arguments, unsupported claims, weak rhetoric)
- The agent produces boilerplate language you have to strip out by hand
- The agent hedges when the prompt explicitly tells it not to
- The agent's output overlaps too much with another agent's output
- The agent's output is too shallow, too long, or structurally wrong
- A new class of evidence is worth pulling in (new data source, new case study, new metric)

Do **not** open a PR to fix a one-off bad output. Re-run first. If the defect shows up twice in different runs, that's a signal the file needs editing.

## The Workflow

1. **Create a branch** named `agent/<agent-name>/<short-description>`. Example: `agent/contrarian/stronger-political-economy-argument`.

2. **Edit the relevant file in `.claude/agents/`.** Keep the YAML frontmatter intact. Edit the system prompt.

3. **Write the commit message in terms of behavior, not text.** Bad: "Updated contrarian prompt." Good: "Contrarian: require at least one case where ops-intel investment failed to deliver, to force Strategist to concede real ground."

4. **Open a PR with:**
   - A link to the run or runs that motivated the change
   - A quoted snippet from a bad output that illustrates the problem
   - The specific behavior change you expect after the edit
   - Any second-order effects to watch for (e.g., "this may make the Contrarian brief longer; may need to trim elsewhere")

5. **Review.** Another human — ideally someone who read the run output — reviews the PR. The review question is always: *will this make the next run's output better, or just different?*

6. **Merge and re-run.** The next run uses the updated agent file. Log the change in the relevant run's retrospective.

## What Not to Change

- **Do not change the agent's tools list** unless you have a specific reason. Tools are chosen to constrain the agent's surface area.
- **Do not add inter-agent dependencies.** The Economist does not read the Operations brief. Keeping the research agents independent is a feature.
- **Do not expand the agent's scope indefinitely.** If you find yourself wanting to add a seventh section to the Strategist brief, you probably want a new agent, not a longer prompt.
- **Do not soften any agent's tone.** The Contrarian should argue hard. The Red Team should be rude. The Editor should cut aggressively. Don't sand the edges off.

## Adding a New Agent

Adding an agent is a bigger decision than editing one. The test: if you cannot explain what the new agent sees that no current agent sees, you do not need a new agent. You need to edit an existing one.

When adding:
1. Create the file in `.claude/agents/`
2. Update `docs/how-to-run.md` to include the new agent in the run sequence
3. Update the orchestration prompt in `claude-code-setup.md`
4. Run once and include the output in the PR so reviewers can see the agent's real behavior before approving

## What Not to Do

- Never let an agent edit another agent's file during a run
- Never let an agent propose changes to its own file during a run
- Never skip human review to merge "obvious" improvements
- Never rewrite an agent file in response to a single run — wait for the pattern
