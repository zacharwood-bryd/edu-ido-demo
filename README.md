# EDU IDO

This demo is run by the [Slack demo seeder](https://github.com/zacharwood-bryd/sf-slack-demo-seeder). Follow `AGENT.md` in that repository. The brief is [`demos/edu-ido.json`](demos/edu-ido.json), built with that repo's `scripts/plan.mjs`.

Northbridge University is the institution. Maya Chen is the student. Maya's name comes from the seeder's education example. The tag on every record is `[demo-builder:edu-ido]`.

The webinar is Slack for Education, backed by Education Cloud. It is a university story, and the same motion fits a college: one view of the student, teams working the application together, and the student staying in the loop from offer to enrolment.

| Part | What you show | What the seeder creates |
| --- | --- | --- |
| Offer | The application moves on from offer, lands in Slack, the teams work it together, Maya is welcomed in | The university account, Maya's account, and the offer case |
| Her day | Course channels, Slackbot answers, a request she raises, a society | The course request case |
| Enrolment | The same record is the one view of her once she is enrolled | That case, moved to closed |

The seeder creates a new Slack workspace named Northbridge University (`edu-ido`) and the Account and Case records. It does not create channels, post messages, or add a bot. Course channels, Slackbot, and societies are what you open in that workspace after you connect Salesforce for Slack yourself.

Record ids and the Slack workspace id go in `demos/edu-ido.links.json`, which is gitignored. `salesforceIds` in the spec stays empty.
