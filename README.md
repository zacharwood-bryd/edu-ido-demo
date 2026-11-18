# EDU IDO

This demo is run by the [Slack demo seeder](https://github.com/zacharwood-bryd/sf-slack-demo-seeder). Follow `AGENT.md` in that repository. The brief is [`demos/edu-ido.json`](demos/edu-ido.json).

Northbridge University. The webinar is Slack for Education, backed by Education Cloud. It runs in three parts: student services, the lecturer, and the student. A short trust-and-safety close finishes it.

The people are members of the Meridian Group Enterprise org. Slack user ids are in [`slack/cast.json`](slack/cast.json). The tag on every seeded record is `[demo-builder:edu-ido]`.

| Part | Who | What you show |
| --- | --- | --- |
| Student services | Alex, with Sam in finance and Riley in accommodation | Jordan's application channel, the staff handbook canvas, and Jamie's laptop enquiry |
| Lecturer | Casey | The history course and seminar, then Jamie's enrollment before the 1:1 |
| Student | Jordan, then Jamie | Jordan arrives and meets Jamie. Jamie asks for a loan laptop and hears back in Slack |
| Close | Presenter | Who can see student channels, where Slackbot is allowed to answer, and that students have no Salesforce licence |

Alex Fallon and Casey are the Salesforce users. Jordan, Jamie, Sam, and Riley use Slack only.

Record ids and the Slack workspace id go in `demos/edu-ido.links.json`, which is gitignored. `salesforceIds` in the spec stays empty.

## What you do live

Slackbot is not seeded. In the webinar, ask it yourself.

1. In `#app-jordan`, ask Slackbot: "Can Jordan defer the tuition deposit while a visa is pending?" The answer is in the Staff handbook canvas: 14 days, source Fees, Winter 2026.
2. As Casey, ask Slackbot what needs attention in `#course-channel` and `#seminar`.
3. In `#seminar`, open Jamie's program enrollment from the link in Casey's post, then show Casey's follow-up.
4. In `#course-channel`, ask Slackbot: "What happens if my laptop will not start?" The answer is in the Student FAQ canvas.
5. In `#student-services`, ask Slackbot to update Jamie's broken-laptop case, and approve it only after the preview. If Slackbot cannot write to Education Cloud, show the case Alex already owns and say the update would come back on this thread.
6. Close on trust and safety: student channels are only for the people in them, Slackbot answers from the canvases you opened, and Jordan and Jamie have no Salesforce user.

Open `#app-jordan` before you start and check that the Education Cloud links show a Salesforce preview. If they stay plain links, add Salesforce for Slack to that channel.
