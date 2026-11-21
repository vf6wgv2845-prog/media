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
