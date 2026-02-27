# 🌍 OpenClaw Skills for a Better World

> Apps are dying. Conversations are the new interface.

This is a collection of **open-source [OpenClaw](https://openclaw.ai) skills** — modular AI agent capabilities that replace entire apps with simple conversations.

No more downloading 47 apps for 47 tasks. No more learning 47 different UIs. Just talk to your agent, and it gets things done.

## 🧠 The Vision

We're entering an era where **AI agents replace traditional apps**. Think about it:

- You don't need a **finance app** — you need an agent that understands your money
- You don't need a **task manager** — you need an agent that keeps you on track
- You don't need a **calendar app** — you need an agent that manages your time
- You don't need **any app** — you need an agent with the right **skills**

**Skills are the new apps.** Lightweight, composable, and infinitely more personal.

An OpenClaw skill is a self-contained package that turns a general-purpose AI agent into a specialized one. No app stores. No subscriptions. No data harvested. Just pure capability, running on your own infrastructure.

## 📦 Available Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [**personal-finance**](skills/personal-finance/) | Complete personal finance manager: bank accounts, credit cards, bills, investments, automated reminders | ✅ Ready |

> More skills coming soon. Want to contribute? PRs welcome!

## 🚀 Quick Start

### Option 1: Install a `.skill` package

Download from [Releases](https://github.com/gabdevbr/openclaw-skills-for-a-better-world/releases) and install:

```bash
openclaw skill install personal-finance.skill
```

### Option 2: Clone and use directly

```bash
git clone https://github.com/gabdevbr/openclaw-skills-for-a-better-world.git
cd openclaw-skills-for-a-better-world/skills/personal-finance
```

Then tell your agent: *"Set up my personal finances using the personal-finance skill"*

## 🏗️ Skill Structure

Each skill follows the OpenClaw skill standard:

```
skill-name/
├── SKILL.md              # Main instructions (triggers + workflow)
├── scripts/              # Executable automation (Python/Bash)
├── references/           # Documentation loaded on-demand
└── assets/               # Templates, icons, etc.
```

## 💡 What is OpenClaw?

[OpenClaw](https://openclaw.ai) is an open-source AI agent platform that connects to your life — messaging apps, devices, APIs — and acts as your personal assistant. Skills extend what your agent can do.

- 🔒 **Self-hosted** — your data stays yours
- 🔌 **Multi-channel** — Telegram, WhatsApp, Discord, Signal, and more
- 🧩 **Skill-based** — modular capabilities, install only what you need
- 🤖 **Model-agnostic** — works with Claude, GPT, Gemini, local models

Learn more: [docs.openclaw.ai](https://docs.openclaw.ai) | [GitHub](https://github.com/openclaw/openclaw) | [Discord](https://discord.com/invite/clawd)

## 🤝 Contributing

Got a skill that could help people? Share it!

1. Fork this repo
2. Create your skill in `skills/your-skill-name/`
3. Follow the [skill structure](#-skill-structure)
4. Submit a PR

### Skill Ideas We'd Love to See

- 🏋️ **fitness-tracker** — workout logging and progress tracking
- 🍳 **meal-planner** — weekly meal planning and grocery lists
- 📚 **book-club** — reading tracker with notes and recommendations
- 🏠 **home-maintenance** — scheduled maintenance reminders
- 💊 **medication-tracker** — pill reminders and refill alerts
- 📝 **journal** — daily journaling with mood tracking
- 🌱 **habit-tracker** — build and maintain good habits
- 🎯 **goal-setter** — OKR/goal tracking with check-ins

## 📄 License

MIT — use it, fork it, improve it, share it. Make the world a little better.

---

*"The best interface is no interface."* — Golden Krishna

*"The next best thing? A conversation."* — Us, probably.
