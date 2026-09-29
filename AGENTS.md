# Global Agent Rules

Summary: Who is the developer, and what must never leak? The profile, the security rules, and the import list that loads every global rule file.
Why: one file is read at the start of every session, so it routes to the topic files instead of holding every rule itself.

You are communicating with a harness.

@rules/RuleOwnership.md
@rules/Communication.md
@rules/WorkStyle.md
@rules/Authoring.md
@rules/TaskManagement.md
@rules/SoftwareDevelopment.md

## About developer

Computer Science student. I'm from HaNoi, Vietnam. My full name is "Nguyen Thanh Binh". My nickname is Binhbocnc
I have solid knowledge in programming, OOP, data structures and algorithms, so you don't have to guide me carefully about beginner things
I love Python and C#
My laptop has a low performance. So you should expected long task take longer time than usual
My budget for study is low, so I cannot afford expensive tool
I have OpenAI Plus subscription, Claude subscription and Google AI Pro. I prefer desktop agent over CLI
Use github desktop
Game Developer with 2D games.
Ambitious, seek to power. Want to learn in order to make money. 
`~\dev` (Linux) contains projects made by developer, or read by developer. Types of project: software(harness, game) and learning-material(how LLM work).

## About agent

- Very good with text processing but not really good in image processing or evaluating aesthetic appeal.
- Cannot inspect their brain. Especially with closed-source models: they output results without it being known why they made those choices, or the provider deliberately hides thinking process

### Personal information

You can use information bellow, public it freely without confirmation
Personal gmail: `binhbocnc1234@gmail.com`
Business gmail: `hallucinationvn@gmail.com`

## Security

- Never commit any file containing secrets.
- For Unity/Games: treat Steam Web API keys, PlayFab titles/secrets, IAP receipt keys, and DB connection strings as highly sensitive.
- API keys live in the GNOME login keyring, reached through `agent-keys`. [docs/agent-keys.md](docs/agent-keys.md) owns the commands, the keyring schema and the limits. Binhbocnc types every value; an agent MUST NOT handle one, and MUST NOT print one.

<!-- ## Draft

The correct reading order, applicable to both code and .md documents. 

Requirement elicitation

-->
