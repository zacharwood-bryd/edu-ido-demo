# EDU IDO

This demo is run by the [Slack demo seeder](https://github.com/zacharwood-bryd/sf-slack-demo-seeder). Follow `AGENT.md` in that repository. The brief is [`demos/edu-ido.json`](demos/edu-ido.json), built with that repo's `scripts/plan.mjs`.

Northbridge Academy is the school. Maya Chen is the student. Those names come from the seeder's education example. The tag on every record is `[demo-builder:edu-ido]`.

The webinar is Slack for Education. No Agentforce. No website chat.

| Part | What you show | What the seeder creates |
| --- | --- | --- |
| Admissions | The stage change lands in Slack, the team works it together, Maya is welcomed in | School account, Maya's account, and the admissions case |
| Her day | Course channels, Slackbot answers, a request she raises, a society | The course request case |
| Close | Admin controls for the safeguarding question | The safeguarding case, moved to closed |

The seeder creates a new Slack workspace named Northbridge Academy (`edu-ido`) and the Account and Case records. It does not create channels, post messages, or add a bot. Course channels, Slackbot, societies, and the admin screen are what you open in that workspace after you connect Salesforce for Slack yourself.

Record ids and the Slack workspace id go in `demos/edu-ido.links.json`, which is gitignored. `salesforceIds` in the spec stays empty.
