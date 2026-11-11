# EDU IDO

This demo is run by the [Slack demo seeder](https://github.com/zacharwood-bryd/sf-slack-demo-seeder). Follow `AGENT.md` in that repository. The brief is [`demos/edu-ido.json`](demos/edu-ido.json), built with that repo's `scripts/plan.mjs`.

Northbridge University. The webinar is Slack for Education, backed by Education Cloud. The same three views fit a college: an applicant from offer to enrolment, a student already on a course, and a lecturer who sees both on one record.

Maya Chen's name comes from the seeder's education example. Leah Mensah and Helen Ward are the student and the lecturer this story adds. The tag on every record is `[demo-builder:edu-ido]`.

| View | Who | What you show | What the seeder creates |
| --- | --- | --- | --- |
| Applicant | Maya Chen | Her application moves on from offer and lands in Slack. She stays in the loop and is welcomed in. Slackbot answers the questions a lean admissions team would otherwise repeat. Admissions and Helen work the same case. | Maya's account, and the offer case |
| Student | Leah Mensah | Her course channel, Slackbot answers, a request she raises, and a society beyond the course. | Leah's account, and the course request case |
| Lecturer | Helen Ward | Maya's application and Leah's request on one record, the same record admissions has for Maya. When Maya is enrolled, that case is closed. | Helen's account. Maya's case moved to closed. |

The university account is created with Maya's.

The seeder creates a new Slack workspace named Northbridge University (`edu-ido`) and those Account and Case records. It does not create channels, post messages, or add a bot. Course channels, Slackbot, and societies are what you open in that workspace after you connect Salesforce for Slack yourself.

The walked staff view is Helen, the lecturer, because Leah's half of the demo is the course. Admissions is the other person on Maya's case, which is the moment the teams are on one record.

Record ids and the Slack workspace id go in `demos/edu-ido.links.json`, which is gitignored. `salesforceIds` in the spec stays empty.
