# EDU IDO

This demo is run by the [Slack demo seeder](https://github.com/zacharwood-bryd/sf-slack-demo-seeder). Follow `AGENT.md` in that repository. The brief is [`demos/edu-ido.json`](demos/edu-ido.json).

Northbridge University. The webinar is Slack for Education, backed by Education Cloud. Presenter: Laurence. Webinar: 2 December 2026. It runs in three parts: student services, the lecturer, and the students. A short trust-and-safety close finishes it.

The people are members of the Meridian Group Enterprise org, in the Northbridge University workspace. Separate staff and student workspaces are talk track only. Slack user ids are in [`slack/cast.json`](slack/cast.json). The tag on every seeded record is `[demo-builder:edu-ido]`.

Only Alex is a Salesforce user. Sam, Riley, and Casey work from Slack. Jordan and Jamie have no Salesforce user.

| Part | Who | What you show |
| --- | --- | --- |
| Student services | Alex, Sam, Riley | Jordan Hale HIST, the record channel for Jordan's History application. The record is at the top. Jordan is not in the channel. |
| Lecturer | Casey | `#history-staff`, then a direct message to Jamie, then the week 7 reading pinned in `#his201-seminar-b`. |
| Students | Jordan, then Jamie | Alex's direct message and the welcome checklist. `#history-offer-holders`. Jamie's course, campus, and societies channels. |
| Help | Alex | `#student-help-triage`, then a case on Jamie. |

Record ids and the Slack workspace id go in `demos/edu-ido.links.json`, which is gitignored. `salesforceIds` in the spec stays empty.

## What you do live

Slackbot is not seeded. Ask it yourself. Run each prompt once before the webinar. The wording of the answer varies.

1. Open Jordan Hale HIST. Point at the record at the top, then open the threads on Sam's fee plan message and Riley's Harbour Hall message. The conversation is staff only. When you add the Education Cloud alert, it becomes the newest message in the channel. Post that alert from the automation, not as a person. Skip the stage reset until that automation is in place.
2. Ask Slackbot: "What's our policy if an offer holder misses the accommodation deposit deadline?" Open the Staff handbook canvas it cites. The answer is that Harbour Hall stays held and the date can be extended. The deposit is due Friday 4 December. Source: Fees, Winter 2026.
3. Paste this to Slackbot. Individual Application is not available through its query, so the prompt carries the four students.

```
Create a canvas titled "Who's drifting: History offer holders".

Use only the four students in this message. Do not search Slack. Do not query Salesforce. Do not add anyone else, and do not cite messages or records.

Count the days since last contact from today's date. Sort with the longest silence first. Anyone with no contact on record goes first.

Open with one line: how many History offer holders are quiet, and that Jordan's Harbour Hall deposit is due Friday 4 December.

Then one block per student. Show the name, BA History, the days since last contact as a bar of squares (one square per week, so the longest silence is the longest bar), what is still open, and a single next step.

Priya Shah. BA History. No staff contact on record. Still open: fee plan, and accommodation deposit. Next step: this is the first nudge. One message, both items.

Jordan Hale. BA History. Last contact 20 October 2026. Still open: the first payment on the fee plan, and the Harbour Hall deposit due Friday 4 December. Next step: message Jordan about the room. Leave the fee plan until they reply.

Maya Ellison. BA History. Last contact 28 October 2026. Still open: fee plan. Next step: a short note on the fee plan only.

Owen Blake. BA History. Last contact 1 November 2026. Still open: accommodation deposit. Next step: a short note on the deposit only.

Under the four blocks, close with this sentence: Jordan accepted the History offer and then went quiet. Maya, Owen and Priya are in the same gap.

If a canvas is not available, post this same layout in the reply.
```
4. Ask Slackbot to draft the Harbour Hall nudge, with the deposit due Friday, an offer to extend, and a link to the Welcome checklist. Edit a word, then send it to Jordan as a direct message.
5. Ask Slackbot to log today's deposit contact on Jordan's application and add a follow-up task for Thursday. Approve only after the preview.
6. As Casey, ask Slackbot to catch you up on History channels since Friday, then what Jamie has posted in HIS201. Open `#history-staff` and the thread where Alex tells Casey that Jamie missed 2 HIS201 seminars. Casey offers 15 minutes after Thursday's seminar. If you add an Education Cloud engagement alert, it lands on top of that conversation. Direct message Jamie, then show the pinned week 7 reading in `#his201-seminar-b`. Jamie's note that the chapter 4 PDF will not open, and the question about Thursday's room, are still unanswered.
7. As Jordan, open Alex's direct message, open the Welcome checklist, and tick the first two items. In `#history-offer-holders`, reply to Jamie: "Is Harbour Hall far from the History building?" Ask Slackbot when the accommodation deposit is due and whether more time is possible. The answer comes from the Student FAQ.
8. As Jamie, show the sidebar sections Course, Campus, and Societies, open `#his201-seminar-b` and Casey's direct message. Ask Slackbot about a broken laptop and an essay due Friday. Submit the Student help request: tick Laptop or IT and Coursework extension, choose HIS201, set the date to Friday 4 December 2026, and write that the laptop will not open files and the HIS201 essay needs an extension.
9. As Alex, open `#student-help-triage`, claim Jamie's request, ask Slackbot to create the laptop and HIS201 essay case, approve the preview, then resolve it with a note.
10. Close on trust and safety, with no clicks. Separate workspaces are the talk track. Also say: content filtering, Slackbot only answers from what that person can see, the institution controls AI access and retention, Sam, Riley, and Casey saw only what was shared, and Slack sits alongside Microsoft.

## Once, before the first rehearsal

- In Jamie's Slack sidebar, make three sections: Course (`#his201-seminar-b`, `#history-offer-holders`), Campus (`#campus`), Societies (`#film-society`). Sidebar sections cannot be set from here.
- Build the Student help request in Workflow Builder. Shortcut name: Student help request. Form fields: What do you need? (checkboxes: Laptop or IT, Coursework extension, Fees or funding, Accommodation, Wellbeing, Something else), Course (dropdown: HIS201, Not a specific course), Needed by (date), What happened (rich text). Post the answers to `#student-help-triage` with Claim and Resolve. Resolve asks for one rich-text Note. The channel is empty until Jamie submits the form.
- If you rehearse in the week of 2 December, the History channel posts need to be newer than the previous Friday or Casey's catch-up will look empty. Ask for those lines to be posted again that week.
