# EDU IDO

This demo is run by the [Slack demo seeder](https://github.com/zacharwood-bryd/sf-slack-demo-seeder). Follow `AGENT.md` in that repository. The brief is [`demos/edu-ido.json`](demos/edu-ido.json), built with that repo's `scripts/plan.mjs`.

Northbridge University. The webinar is Slack for Education, backed by Education Cloud. The same three views fit a college: an applicant from offer to enrolment, a student already on a course, and a lecturer who sees both on one record.

The people are already members of the Meridian Group Enterprise org, the same org used for the frontline worker demo. Slack user ids and emails are in [`slack/cast.json`](slack/cast.json). The tag on every Salesforce record is `[demo-builder:edu-ido]`.

| View | Who | What you show | What the seeder creates |
| --- | --- | --- | --- |
| Applicant | Jordan | The application moves on from offer and lands in Slack. Jordan stays in the loop and is welcomed in. Slackbot answers the repeat questions. Alex and Casey work the same case. | Jordan's account, and the offer case |
| Student | Jamie | The course channel, Slackbot answers, a request Jamie raises, and a society beyond the course. | Jamie's account, and the course request case |
| Lecturer | Casey | Jordan's application and Jamie's request on one record, the same record Alex has for Jordan. When Jordan is enrolled, that case is closed. | Casey's account. Jordan's case moved to closed. |

The university account is created with Jordan's.

Demo seeder (`A0CHPUUMC00`) is already installed on the Meridian Group org. The new workspace is still Northbridge University (`edu-ido`). Invites go to the existing accounts in [`slack/cast.json`](slack/cast.json). Harry Kane and Morgan Rogers are deactivated and are not in the cast.

Record ids and the Slack workspace id go in `demos/edu-ido.links.json`, which is gitignored. `salesforceIds` in the spec stays empty.
