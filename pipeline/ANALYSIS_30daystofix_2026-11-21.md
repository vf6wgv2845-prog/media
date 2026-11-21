# What @30daystofix does (Boris's screen recordings + profile screenshots, Nov 21)

Their numbers: every Reel 1.9M-10.4M views (Day 1 "30 days to the reunion" 10.4M, Day 6 gym 9.1M). Day 16: 173K likes, 4,300 comments, 4,434 shares. Day 16 is **88 seconds** long. They also sell a "Glow Up Project Playbook" (pinned "8 million views, nobody drew it").

## Mechanics (copy these, never their character, names or jokes)
1. **"Previously" montage hook, 0-3.5 s.** DAY 1 -> DAY 5 -> DAY 7 -> DAY 9 -> DAY 11 -> DAY 14 -> NOW, ~0.5 s per flash, the character visibly changing each time, with the voice saying days left + the goal ("only fifteen days left until ... reunion"). A new viewer instantly gets the whole story and sees a transformation.
2. **A new visual every 1.5-2 s.** Status stickers that are jokes: "DIET: 58%", "CHEETOS: NOTIFIED", "40 BAGS", "HEADSET: GONE", "BELLY: INDOORS", "JAW: FIXED". Every voice line is a punchline, not narration.
3. **Big 2-word captions**, white with the keyword in yellow/red, lower-middle of the frame.
4. **A new scene/background every episode** (kitchen, gym, dentist, barber, airplane) and **the character changes visibly every day**. This is the thing we can't fake: it needs new character images (live session).
5. **Text-message scenes**: a phone with the ex's chat, the reply typed live ("good, i love hearing about your days"). Cheap, and pure drama.
6. **Top comment as a card inside the video** ("James takes a shower button ---> 138K").
7. **HUD** DAYS LEFT / GLOW-UP % on every frame, a "DAY 16" badge, a spoken countdown word on Day 1-3 ("TWENTY-NINE").
8. **Covers**: "DAY N" + a 2-line funny RESULT title with one word in yellow ("THE PIMPLES MOVED OUT", "HE FOUND HIS JAWLINE", "HIS HAIR WAS A WIG"), character in the middle, a bright background that changes each day, often a green joke label.
9. **Length**: 88 s works for them because of 1-2 s pacing. Our data: viewers leave at 9-17 s with ~3 s pacing. So: only go longer once pacing is at their level; measure avg watch time after each change.

## What we changed (template v4)
- New scene types in pipeline/scenes2.py: `sm` (PREVIOUSLY montage) and `sc` (live text chat). Template: pipeline/episodes/_template_v4.json.
- Covers: "DAY N" + funny result title (e.g. "THE BAR WON").
- More joke status stickers per episode.

## Caution
Their premise is "30 days to the high school reunion" with an ex who was prom queen. Our Danny page ("30 days to the reunion", @30daystothereunion) is too close to it: change Danny's premise before launch.

## Full Day 21 breakdown (~100 s, 12 clips, narration transcribed)
| Time | Beat | On screen |
|---|---|---|
| 0-3 s | "Only 10 days left until James' high school reunion." | PREVIOUSLY montage Day 1 -> 5 -> 11 -> 17 -> NOW |
| 3-7 s | "57,000 of you asked for better communication skills." | Top comment card "better communication skills button", sticker SOCIAL SKILLS: 0% |
| 7-12 s | "His idea of small talk is..." | Store scene, cashier, SMALL TALK sign |
| 12-30 s | "The coach wears sunglasses indoors. One look at James, and he puts on a second pair." Lesson 1 eye contact: stares at the guy next to him 0:05 -> 0:23 -> 0:48 -> 1:00, "he changed seats, then classes" | RIZZ CLASS whiteboard, PAIR #2, timer stickers, HE CHANGED CLASSES |
| 30-40 s | "Lesson 2 is compliments. Nobody will partner with James so he gets the mannequin. He tells her she has nice joints. Her arm falls off." | PARTNER: MANNEQUIN, speech bubble |
| 40-48 s | "Lesson 3 is the pickup line." "Are you a Wi-Fi signal..." "The coach takes off both pairs to stare at him." | speech bubble, BOTH PAIRS OFF (callback) |
| 48-62 s | "The final exam is a real person. In the laundry room, James asks the neighbor from 4B how she's doing, then actually listens. She talks for 40 minutes about her cat. She moves her laundry one machine closer." | FINAL EXAM: A REAL PERSON, 40 MINUTES, 1 MACHINE CLOSER |
| 62-75 s | "Sarah texts, how was your day? James sends, good, I love hearing about your days. Sarah sends three paragraphs. James reads every word twice." | phone chat typed live, 3 PARAGRAPHS |
| 75-80 s | (certificate) | RIZZ 101 - JAMES - ATTENDED stamp |
| 80-88 s | "Now it's on you. The top comment picks what James fixes next. And for the first time, he's actually listening." | NOW IT'S ON YOU, blank comment card ???, TOP COMMENT DECIDES |

Takeaways: a sitcom structure (ask -> 3 escalating fails with a callback -> real test -> payoff with the ex -> stamp gag -> hand it back), 2-3 s per line, each line a punchline, an emotional last line, and an OPEN top-comment vote that turns comments into pitches (4,300 comments on Day 16).
