# EDU IDO

This demo is run by the [Slack demo seeder](https://github.com/zacharwood-bryd/sf-slack-demo-seeder). Follow `AGENT.md` in that repository. The brief is [`demos/edu-ido.json`](demos/edu-ido.json).

Northbridge University. The webinar is Slack for Education, backed by Education Cloud. It runs in three parts: student services, the lecturer, and the student. A short trust-and-safety close finishes it.

The people are members of the Meridian Group Enterprise org. Slack user ids are in [`slack/cast.json`](slack/cast.json). The tag on every seeded record is `[demo-builder:edu-ido]`.

| Part | Who | What you show |
| --- | --- | --- |
| Student services | Alex, Sam, Riley | The record channel for Jordan's application. Jordan is not in it. |
| Nudge | Alex and Jordan | A direct message. No Salesforce record in that conversation. Alex brings Jordan's reply back to the record channel. |
| Lecturer | Casey | Reads Jamie's enrollment, then writes the follow-up in `#seminar` without the record. |
| Student | Jordan, Jamie | The course channel and `#student-services`. Jamie hears the outcome in Slack. The case stays with Alex. |

Alex Fallon and Casey are the Salesforce users. Jordan, Jamie, Sam, and Riley use Slack only.

Record ids and the Slack workspace id go in `demos/edu-ido.links.json`, which is gitignored. `salesforceIds` in the spec stays empty.

## What you do live

Slackbot is not seeded. In the webinar, ask it yourself.

1. In the record channel, ask Slackbot: "Can Jordan defer the tuition deposit while a visa is pending?" The answer is in the Staff handbook canvas: 14 days, source Fees, Winter 2026. Jordan is not in this channel.
2. Show Alex's direct message to Jordan, then Alex's note back on the record channel that Jordan still wants the place.
3. Open Jamie's program enrollment in Education Cloud. Then show Casey's follow-up in `#seminar`. That post does not contain the record.
4. In `#course-channel`, ask Slackbot: "What happens if my laptop will not start?" The answer is in the Student FAQ canvas.
5. In `#student-services`, ask Slackbot to update Jamie's broken-laptop case, and approve it only after the preview. Jamie's thread stays in ordinary language. The case stays on Alex's side.
6. Close on trust and safety: the record channel is staff only, Slackbot answers from the canvases you opened, and Jordan and Jamie have no Salesforce user.

Jordan's record channel is the Individual Application channel. Its name comes from Friendly Name on the application: the student name and subject code, for example Jordan Hale HIST. Friendly Name is the first field on the Admissions compact layout, which Slack uses for the record. The applicant conversation stays the direct message and the course channel.
