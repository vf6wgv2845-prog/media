# Daily run: Boris's Instagram story accounts (6)

**Nov 25 night (Boris, live): read 5l FIRST. Jess is the main focus, Theo second. What works on Jess is now the default format on every story page; 5l overrides 5i/5j where they differ. IntelliStudy videos: see 5g + 5l.4.**

Owner: Boris. He has given standing permission to post on all accounts in `state.json` `accounts`: Theo, Malik, Rosie, Trash Horde, and (once set up) the two new Theo-style glow-up pages Jess and Danny.
**Nov 25: read sections 5i, 5j and 5k first. It overrides older format/cadence notes for Jess, Theo, Malik, Rosie and the Trash Horde.**
**Golden rule: the audience decides.** Every episode must follow the winning vote from the previous episode's comments. Never ignore, override or "improve on" a vote.

## 0a. New glow-up pages (Jess, Danny): same format as Theo
Boris asked (Nov 20) for two more pages run exactly like Theo: 30-day countdown, one fix per day by vote, DAYS LEFT / GLOW-UP / AURA HUD, everything in 3b. Their series have `status: waiting_for_setup` until all of `setup_needed` is done.
- Each run: if a series is `waiting_for_setup`, check get_connectors for its account and pipeline/assets for its image. If anything is missing, skip it and list what's missing in the report. Never post a new page with someone else's image.
- When both exist: set `status: live`, fill `accounts.<key>`, and post Day 1 (hook = the deadline + the ex/bully, stats, first vote from `open_vote`) built from `_template_v2.json` (no scoreboard scene on Day 1: aura starts at 10). Day 1 Reel gets pinned by Boris.
- After that they follow every Theo rule (Day 7 boost episode, visual gap note, live sessions for new looks).

## 0. Setup (each run starts fresh)
1. Attach the repo: `add_repo` owner `vf6wgv2845-prog`, repo `media`, access `push`; clone to `/home/claude/media`.
2. Load Windsor tools with ToolSearch query `+Windsor`. Instagram connector id: `instagram`.
3. Install the free voice: `pip install --break-system-packages -q kokoro-onnx soundfile`, then download
   `https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx` -> `/tmp/tts/kokoro.onnx`
   and `.../voices-v1.0.bin` -> `/tmp/tts/voices.bin`.
4. Read `pipeline/state.json` (current day, stats, open vote, cast, rules for each series).

## 1. Check what's already posted today
`get_data` (connector `instagram`, fields `account_name, media_id, media_type, timestamp, media_caption`, date_preset `last_3dT`).
If a series already got its *episode* today (Boris did it live), skip that series' episode. Bonus/special posts listed in `bonus_posts` (or GTA/morning specials) do NOT count as the episode: still post the next Day.

## 2. Count the votes (for each series)
`get_data` fields `comment_text, comment_like_count, comment_timestamp, comment_username, media_id` (date range covering the last episode) and filter to the series' `last_media_id`.
- Each comment naming a number (or the option name) = 1 vote; each like on that comment = +1. One vote per user (use their latest comment). Ignore the account's own comments.
- Most votes wins. Tie -> earliest comment among the tied options. Zero votes -> pick the option that makes the best story and say "the crowd's choice" (it's still honest: nobody voted). Note the counts.
- Also read non-vote comments: if many viewers ask for something (a character, a twist), work it into the story. That is also "what the audience wants".

## 3. Write the next episode (Day N+1)
Check `state.json` `trends` for current trending topics (e.g. GTA 6) to weave in lightly.
Copy the shape of `pipeline/episodes/<series>_d01.json`. 5 scenes:
- s1 hook: "Day N+1: you voted ___" style, punchy, 3 short lines.
- s2 stats: apply the winning choice -> raise the matching stat(s) by 1-3 (realistic; confidence moves too). Show updated stats.
- s3 event: a notification card from a cast member + a twist line (rival, ex, best friend, boss...). Keep threads going, leave loose ends.
- s4 the result of the choice / the stakes.
- s5 new vote: 5 options for tomorrow, "Comment the number".
Every episode from Day 2 on opens s1 with a 1-line recap so a brand-new viewer gets it instantly (e.g. "17 days until he sees his ex. You've fixed his hair and skin."), and ends with "Start from Day 1, it's pinned on our profile."
**Theo Day 7 is the episode Boris will pay to boost**: make it the strongest so far: a cliffhanger (e.g. Maya notices his new photo / likes his post), a clear recap of Days 1-6, and the clearest vote yet.
Rules: wins AND losses for Malik; Rosie's chosen dish must come with a **real, accurate recipe** (also post a 3-4 slide recipe carousel like `cook/c001_*.jpg`, or put it in the caption). Theo in cloud runs: the image can't change without Leonardo, so show the fix through stats + narration ("Day 2: the hair. Full reveal soon") and flag in the report that Boris should do a live session for the visual upgrade.
Save the config as `pipeline/episodes/<series>_dNN.json` (image path relative to `pipeline/assets`, `voice` = the series' `voice_cloud`, pill e.g. "SEASON 1  •  DAY 2 / 30").

## 3b. Retention format (learned from @dalesglowup: 12 posts -> 58K followers, Reels at 2.5M / 1.2M / 706K views)
**Boris's standing rule: this format is REQUIRED for EVERYTHING posted on ALL accounts: every Reel, every story, every carousel/extra post. No exceptions, no "old style" posts.**
Per-series scoreboard (in `state.json` `series.<x>.format` / `aura`; `score.py <series>` prints the tiles):
- Theo: DAYS LEFT / GLOW-UP % / AURA x/100 (calendar = days to the party).
- Malik: DAY n/30 / OVR (stats avg x10) / HYPE x/100. Calendar = days to the next big game. Commenter cameos as coach, trainer, scout, rival's cousin...
- Rosie: DAYS LEFT / SKILL % / BUZZ x/100. Calendar = days to the cook-off. Commenter cameos as taste-tester, judge, sous-chef...
- Horde: BOSS HP / DAMAGE / CLEANERS (from real hauls only; no aura). Comment cards = real haul comments; top cleaners become characters ("Captain @handle"). Calendar = days until the boss deadline.
Copy the mechanics, never their jokes, names or characters. Start every episode (all story series) from `pipeline/episodes/_template_v3.json` (v2 only as a reference) (all features below already wired; see the docstring at the top of `pipeline/extras.py`).
1. **HUD on every frame** (`hud`): DAYS LEFT / GLOW-UP % / AURA x/100, top-left. GLOW-UP = average of the stats as %; tiles with `from` + `at` pop to the new value at that moment (GLOW-UP at `["s2",0]`, AURA at `["sb",-1]`).
2. **Aura = real engagement, shown openly** (`scoreboard` scene `sb`, auto-inserted after s2): run `python3 -I pipeline/score.py theo views=.. likes=.. comments=.. shares=.. saves=..` with the previous episode Reel's real numbers (get_data `media_views, media_like_count, media_comments_count, media_shares, media_saved`; reposts are not readable on this connection). It prints the `hud` AURA tile, the `scoreboard` block and the `sb` voice lines. After posting, run it again with `--save`. Never invent numbers. Say the rates out loud sometimes ("shares are worth 5") so viewers know sharing helps him.
3. **Open on the audience** (`comments`): first 2-3 seconds = the winning vote's real comment as a card (handle, text verbatim, real like count); stack 2-3 cards if several people asked for the same thing. Only public handles, nothing mean about them.
4. **Commenters become characters**: if a commenter offers ("can I be his barber?"), make them that role in the episode by handle ("Barber @handle") and tag them in the caption. Add to s5/caption: "Want to be in the next episode? Say what job you'd do." This is the #1 comment driver.
5. **Rules + countdown**: say "one fix per day" (sticker) and show the flip-calendar `{"kind":"calendar","text":"<days left>","x":800,"y":620}` early in s1 (after the comment card has gone, never overlapping it).
6. **The fix goes wrong first, then works**: 2-3 escalating absurd attempts (stickers as sound effects: CLANK, OW!, RIIIP; scene labels: LAST NIGHT, FLASHBACK), a callback gag, then a payoff badge ("GLOW-UP +6%").
7. **Maya is woven into the fixes** (she works where he goes for the fix, she sees him at the worst moment). Ending = a sweet beat undercut by a gag -> he stays short of the goal -> tomorrow's vote.
8. **Word-by-word captions** (`captions`): voice lines shown 2-3 words at a time, keywords coloured (put names, stats and numbers in `keywords`). Keep on-screen text panels short so they don't fight the captions.
9. **Designed cover** (`cover_title`: ["DAY N", "<the fix in 2-3 words>"]): grid tiles must read like episode titles.
10. **Caption line 1** = "<N> days left. You voted <fix>. <teaser of what went wrong>..." (cut off by "..." on purpose).
11. **Length**: aim 20-28 s (v3, Nov 20 analysis). Cut lines rather than speeding the voice; the hook must land in the first 2 seconds. Start from `pipeline/episodes/_template_v3.json` (order s1 -> s3 -> s5, no stats panel, no scoreboard scene; HUD + stickers carry the numbers). The vote screen must start by ~18 s.
12. Check the contact sheet (stills mode now shows extra frames at every sticker/comment) for overlaps before the full render.
**Visual gap (tell Boris, don't fake it)**: the reference draws a new scene every episode (bridal shop, wax room, surgery) and the character visibly changes. Cloud runs only have the images in `pipeline/assets`. Reuse the best matching one and lean on stickers/captions; when Boris does a live session, ask him for new scene images (same character, same style) and add them to assets with a clear name (e.g. `theo_barber.jpg`).


## 3c1. Nov 21 evening: why viewers leave at ~9-11 s, and the fixes (Boris: Jess, Theo and Danny are the priority)
**Priority (Boris, Nov 21):** Jess, Theo and Danny (the glow-up pages) get the most care and are written and checked first each run. Malik, Rosie, Horde and History still get full runs.
Data: Jess D1 14.7% skip / 9.5 s avg, Danny D1 30% / 8.7 s, Theo D5 42% / 7.1 s. People who get past 3 s stay on average ~11 s (estimate (avg - skip*1.5)/(1-skip)), then leave. Timings show what plays at 2-11 s in all three:
- **Bug (fixed in engine.py):** the 3 on-screen hook lines waited for voice lines 2 and 3, so the punchline ("sister's wedding.") wasn't on screen until ~3-4 s. They now all pop in within 0.8 s (`hook_slow: true` = old behaviour).
- **2-7 s was admin:** "The wedding is in thirty days." + "Stay to the end, you decide..." (4-5 s with no new info). Now: NO voice line for the countdown (the calendar sticker says it) and no "stay to the end" voice line (a "YOU DECIDE" sticker says it). Voice line 2 must be a NEW, funnier fact (e.g. "And she's still wearing his hoodie.").
- **7-11 s repeated the hook:** Jess s3 opened "Her sister texted: Ryan is best man"; Danny's chat opened "It started with one message. Brock asked..."; Theo "Day five of thirty. You voted gym." Never restate the hook or the vote; every line after the hook is a new escalation. The notification card must carry new info too.
- **One static picture for 30 s:** new `beats` key swaps the background image at any line: `"beats": [{"scene": "s3", "line": 1, "image": "jess_dress_nozip.jpg"}]`. For Jess/Danny render 2-4 toon.py looks per episode (expression, outfit, sweat, tired) so the picture changes every ~3 s. Theo: reuse his existing images (scruffy, gaming, clear skin) as beats until a live session adds more.
- **Put the strongest beat (the ex/rival text chat) at ~8-10 s**, exactly where people were leaving, not at 17 s; keep one open loop for the end ("He's typing again").
- `"conflict": null` turns off the s3 text panel; it fought the word-by-word captions (and repeated "30 days" a third time).
- Target 20-24 s. Example re-cut: `pipeline/episodes/_example_v5_jess_d01.json` (20.7 s, chat at 9 s, 3 picture changes). Check the contact sheet: hook fully visible by frame 1, stickers on the body (y ~1250), not over the face or the notification.

## 3c0. Nov 21: reference account @30daystofix (2-10M views/Reel) -> template v4
Read pipeline/ANALYSIS_30daystofix_2026-11-21.md. Start episodes from `_template_v4.json` (sm montage -> s1 -> s3 -> sc chat -> s5): PREVIOUSLY montage in the first 2-3 s, a joke status sticker every 1.5-2 s, a text-chat scene when the ex/rival is in the episode, covers titled with the funny RESULT ('DAY 5' / 'THE BAR WON'). Copy mechanics only, never their character, names or jokes. Go longer than ~30 s only when the pacing supports it, and check avg watch time.

**Script rules from the full @30daystofix Day 21 (see lessons + state.voting_rule_v2):** open with the audience ask + count ("N of you asked for..."), then 3 escalating attempts that each end in a punchline, one running callback gag, a real-world test, a payoff in a chat with the ex/rival, a small stamp/certificate gag, then the open vote (scene `sv`) + one heart line. Narration = short deadpan sentences, 2-3 s each; every line is a beat.

## 3c. What the Nov 20 analysis found (read before writing ANY episode) - full notes: pipeline/ANALYSIS_2026-11-20.md
- 46-72% of viewers leave in the first 3 seconds on every Reel. Hooks that opened with "Day N: you voted..." or a plain statement lost the most. Open on the most dramatic/absurd beat of the episode (the fail, the twist, the text), as a full sentence, in under 2 s, with motion (sticker/comment card) on frame 1.
- The viewers who stay leave after ~9-17 s, almost always DURING the stats panel (s2) or the aura scoreboard (sb). The vote screen started at 29-39 s, so almost nobody ever saw the vote options: that's why votes are near zero. => v3 structure, vote by ~18 s, say "stay to the end, you pick tomorrow" in s1.
- Best % watched: the short single-moment Theo bonus (33 s, 31% watched, first shares). Single clear moment > packed episode.
- Rosie: worst hooks (72% skip on Day 3) and 0 comments ever: her hooks must be the kitchen disaster first ("Her dumplings exploded in the pan").
- Two Reels got almost no distribution (Malik Day 2: 8 views; Rosie Day 4: 0 views after 1 h). If a Reel is still under 20 views after 3 h, note it in the report (possible processing/suppression) and don't repost it.
- Windsor gives skip rate (first 3 s) and average watch time only, no per-second retention curve; estimate the drop point from avg watch time vs scene timings (timing.json) and log it.

## 5e. Daily content plan (Boris + Claude, Nov 20)
Story series (Theo, Jess, Danny, Malik, Rosie): 1 main Day-N episode (5:45 PM run). Theo also gets (a) a morning bonus moment (new beat) and (b) a night "progress check" Reel ending on a cliffhanger, plus 2-3 stories; every ~4 days a "Days 1-N in 40 seconds" catch-up to pin. Follower ladder (shown in captions/HUD, never "like for X"): 50 followers = pro haircut reveal, 100 = Maya sees him in person, 250 = new outfit, 500 = ?, 1K = ? (audience picks the rewards).
Trash Horde: test 5 Reels/day for 5 days (Nov 21-25), each a different format (verified fact, 60-second challenge, boss update, "how long does it last" quiz, haul shout-outs). Keep 5 if per-post views hold, else drop to 3. Facts only from sources logged in state.json `facts` (verified by web search).
Extras scheduled task (created Nov 20) runs at 7:37 AM and 1:37 PM ET: Theo bonus (morning) + Horde Reels (both). The 5:45 PM run posts the episodes + stories and the Horde battle Reel (plus the Theo night progress check when it fits, 15+ min after Theo's episode). Horde total target during the test: morning 1, midday 2, evening 2. Never post two Reels on one account within 2 hours (Nov 21: a Reel posted 13 min before another got 3 views).

## 5f. Nov 22 night: Boris's posting plan (replaces the slot plan in 5d/5e where they differ)
Boris (Nov 22, ~6 PM ET): **every account posts at least 2 Reels a day, 1 story a day on every account, and the IntelliStudy promo account (@intellistuddy) posts 3 times a day.** He wants really good videos, especially IntelliStudy, Theo and Jess.
- 5:45 PM main run: every story series' Day episode + 1 story per account (story_card.py) + Horde battle Reel.
- 7:37 AM extras: second Reel for Theo, Jess and Danny (a "bonus moment": one absurd beat between episodes that keeps the open vote alive and never decides it) + a Horde Reel.
- 1:37 PM extras: second Reel for Malik, Rosie and History (Malik/Rosie: a single-moment bonus beat; History: a short 25-35 s true story, sources in caption) + a Horde Reel.
- Theo and Jess get the most care: write and check them first, render 2-4 toon looks for Jess per Reel, use every 3c1 rule, inspect every contact sheet frame.
- Never two Reels on one account within 2 hours (if a slot can't fit the spacing, post later in the same run rather than skip).
- @intellistuddy: see 5g.

## 5g. IntelliStudy (@intellistuddy, Windsor account 17841453485592778): 3 posts/day (8:13 AM, 3:13 PM, 8:13 PM ET task)
Boris's app: IntelliStudy (formerly StudyFlow), an AI study web app at intelli-study.com (old: quick-learn.base44.app). Goal: thousands of real users. He wants REAL-looking videos, not AI-looking.
- Make videos from REAL screen recordings of the live app (Playwright, 1080x1920 mobile viewport, record_video): paste real notes (e.g. a short IGCSE/biology/history paragraph), generate flashcards/quizzes, flip cards. Never fake app features: only show what the site actually does that day; if a feature errors, don't show it.
- Edit with ffmpeg/PIL: big hook text in the first 0.8 s, word captions, zoom-ins on the key moment, 15-30 s, Kokoro voice optional (a natural voice like af_heart; or text-only with a beat). Formats to rotate: before/after comparison ("making flashcards by hand: 45 min vs IntelliStudy: 10 s"), one-feature demo per post (different app section each time), "POV: exam tomorrow", study tip + the app, student-reaction style text posts.
- **Until the separate IntelliStudy scheduled task exists (it needs Boris's approval in a live chat; as of Nov 23 AM it does NOT exist), the 5:45 PM main run posts one IntelliStudy Reel per day following this section** (check get_data first so nothing is doubled).
- Caption: hook line, what it does, "link in bio" / intelli-study.com, 5 hashtags (#studytok #studyhacks #igcse #revision #studentlife or fitting ones). Honest claims only (no fake user counts, reviews or testimonials).
- 1 story/day (the day's best clip or a story_card-style card with the link). Reply to every genuine comment. Log every post + its numbers in state.json `intellistudy.log` and lessons; keep files in `intellistudy/`.

## 5h. Nov 23: Jess is the model account (Boris: "it's doing great")
Data Nov 23 PM: every Jess Reel 1,400-1,700 views (D1 1,683, D2 1,425, Mon bonus 1,481 in 6 h / 19 likes = most-liked post on any account). Theo/Danny normal Reels 85-250. Jess has 3 of the top 4 posts.
- **Don't change what works on Jess**: same premise, same toon style, 3-4 toon looks per Reel, 3c1 pacing, single-moment bonus in the morning.
- **Only fix comments on Jess** (2 and 0 comments on her last two despite 1,400+ views): end on a 2-choice question that's answerable in one tap ("1 or 2?"), say it in the voice AND show it as the cover-style sticker; put the leading real comment card on screen by ~10 s, not only on the vote screen; pin-able caption line 1 ends with the question. Keep the full option list in the caption for the episode.
- **Copy Jess's mechanics to Danny and Theo** (never her story): a premise a stranger gets in one line in the first 2 s, 3-4 picture changes per Reel (Danny: new toon.py looks every Reel; Theo: rotate existing images as beats until a live session adds new ones), and the same 2-choice comment ask.
- Track each run in learning_log: Jess views vs comments, and whether the 2-choice ask lifts comments; if comments stay under 3 for 2 more days, try the commenter-cameo ask in the voice line instead.

## 5i. Nov 25: niche research + "the 800-view gate" (Boris, live: "Jess is doing good, rank it up but don't make a change that makes it go down; change the others a good amount")
**What our own data says (59 Reels, Nov 19-24, Windsor skip rate + avg watch):** every Reel with **skip <= 40% AND avg watch >= 10 s** reached 800-1,800 views. Everything else was stuck at ~100-250 (47 Reels, avg 50% skip / 6.8 s). Instagram shows each Reel to a small test pool and only pushes it further if people stay. Jess passes this gate on every post (avg 37% / 12.0 s, 1,473-1,820 views). Theo, Malik, Rosie, Horde and History almost never do (45-53% skip, 5.5-8.2 s). Danny's Wed bonus (receipt + 1-star review props) is the first non-Jess Reel at 32.8% / 14.8 s.
**What the niche + platform reward (web, Nov 25; sources in state.trends.niche_nov25):**
- Instagram Reels ranking (late 2026, per SocialPilot and Dataslayer write-ups): watch time / completion first, then **sends (DM shares) per reach**, then likes per reach. Original content only, no watermarks. Keyword-rich caption text beats hashtags. Trial Reels need 1,000+ followers (we can't use them yet).
- @30daystofix (2-10M per Reel): ex/reunion stakes, visible change every day, a new picture or joke every 1.5-2 s, top comment as a card, sitcom structure (see 3c0).
- Fruit Love Island (AI reality-TV parody, Mar 2026: 3M followers in 9 days, 300M+ views, ~10M per episode, per Wikipedia): a familiar format (dating show), audience votes decide what happens, daily serialized episodes, absurd characters. It also drew heavy "AI slop" backlash and TikTok removals. So: stay hand-drawn-looking with real comments and real recipes/facts, never generic AI-looking footage.
**Gate rules for every account except Jess (apply from the next Reel):** the hook sentence is fully on screen by 1 s; a new picture or prop every 2-3 s (3-4 looks + drawn props, never one static image); the strongest beat (chat with the ex/rival) by 7-9 s; 20-26 s total; one visible prop that IS the joke in the frame (receipt, sign, card, glued place card); a relationship stake a stranger gets in one line. On the vote screen add a send sticker ("SEND THIS TO YOUR <brother/sister/teammate/chef friend>") and put the same ask in caption line 2.

### Jess: protect the baseline, test one lever at a time
**Never change** the premise, toon style, voice (af_bella 1.18), length (22-26 s), order (s1 -> chat by ~7 s -> s3 -> 1-or-2 vote), 3-4 looks per Reel, the leading real comment card, the morning single-moment bonus, or posting times (~7:50 AM bonus, ~5:50 PM episode).
**Baseline** (her last 6 Reels): 1,473-1,820 views, skip 33-41%, avg watch 10.6-13.4 s, 0-3 shares.
**Tests (the order is now in 5j)** go on the **morning bonus first** (never the Day episode), **one at a time**, with results logged in `state.series.jess.experiments`. At ~24 h: **keep** it only if views >= 1,400 AND skip <= 38% AND avg watch >= 11 s (then also use it on episodes); otherwise revert the next day and note why. Order:
- **T1 (Nov 26 AM bonus): send prompt.** No voice change. Vote screen gets a sticker "SEND THIS TO YOUR SISTER" (or the beat's best fit) and caption line 2 = a send ask ("Send this to the friend who'd glue the place card"). Measures shares/reach.
- **T2: loop ending.** The last frame returns to the hook image, and the last voice line sets up the first one so rewatches flow (watch time).
- **T3: a third Jess Reel per day** (a 12-16 s chat-only "night text" beat, ~9:30 PM ET). Only after T1/T2 hold, and stop if the other Jess Reels drop below the baseline.
- **T4:** the cameo ask in the voice line ("want to be her date? comment the job").

### Theo (stays 3D, Boris Nov 25)
Every Reel gets 1-2 drawn props/frames composited with PIL over his existing images (like the Nov 25 Thanksgiving card: frames, signs, stickers on the photo, a phone screen), 4+ beats, chat by ~7 s. Keep asking Boris for new 3D images in live sessions.

### Malik + Rosie: redrawn as toons (Boris approved Nov 25)
From their next Reel use `toon.py` who `malik` (scene `gym`) / who `rosie` (scene `kitchen`); base looks are `pipeline/assets/malik_toon_*.jpg` / `rosie_toon_*.jpg`. Render 3-4 looks per Reel with props (`extra` SVG: ball, scout email on a phone, burnt pan, thermometer). The first toon Reel's caption says once "(new look, same story)"; no other fuss. The stories continue. Sharpen the stakes so a stranger gets them in one line:
- Malik: "His ex is in the stands at the tourney and the scout wants his left hand" (Jada + scout Dec 4 + Tyler/Dez).
- Rosie: next episode twist: **Julian (the favorite) is her ex from culinary school**. Hook lines lead with Julian or Chef Marco, never with the dish. The recipe stays real and stays in the caption.

### Trash Horde = a story now (Boris approved Nov 25)
Lead **Wes** (toon `who: wes`, scene `street`): he threw one cup out his car window, it hit park ranger **Cole** (his ex **Brooke**'s new boyfriend), and the judge gave him 30 days of litter duty in the park. At night the trash comes alive (the Horde). He must get the park spotless by Day 30 or start over. Same vote mechanics as Jess (top comment decides), worded as a natural question per 5j (no "comment 1 or 2"). HUD: DAYS LEFT / PARK CLEAN % / HORDE HP. **HORDE HP moves only from real hauls** (5c counting + verification rules unchanged); real cleaners appear as comment cards and become "reinforcements" by @handle. Litter facts only as one sticker inside an episode, with the source in the caption. No more standalone fact/quiz/challenge Reels. Cadence: AM bonus beat, midday short beat (<= 20 s: a chat or a real-haul shout-out), evening Day N.

## 5j. Nov 25 (Boris live: "get to 10K, then 100K+ fast"): deep research -> production + distribution rules
Full notes + sources: `pipeline/RESEARCH_2026-11-25.md`. Short version:
- **Where we stand:** Jess (1,400-1,800) is at the Instagram median for accounts under 2K followers (Metricool 2026: ~1,484 views per Reel). Getting to 10K+ needs non-follower distribution, which runs on watch time, then **sends per reach** (Mosseri: "sends are slightly more important for unconnected content"), then likes per reach. Posting more mainly raises the odds of an outlier (Buffer: the 90th-percentile post rises with frequency, the median doesn't).
- **Vote-bait risk:** Instagram says it may not recommend content "asking people to comment with a specific word, number, or emoji". Facebook demotes "vote baiting". "Comment 1 or 2" is exactly that pattern. **Boris (Nov 25): rephrase on every page except Jess now; Jess tests it first (her test queue below).** New wording: voice "Dress, or a date? What should she do?" Vote-screen title "WHAT SHOULD SHE DO?" with hint "THE DRESS  or  A DATE". Caption: a natural question ("Dress or a date: what should Jess do?"), never "comment 1 or 2" or "comment the number". Keep counting votes from any comment that names an option (or says 1/2).
- **Motion (all pages except Jess until her test): set cfg `"motion": true`.** engine.py adds a punch-in + tiny shake on every picture change and scene start, plus a stronger slow push. Aim for a visual event (picture change, sticker, punch) every 1.5-2 s.
- **Safe zones (Instagram UI covers the bottom ~35% and a ~230 px right rail over the bottom 40%):** on non-Jess pages put word captions at y ~1150-1250 (not 1500), comment cards at y <= 1450, and no stickers at x > 850 below y 1150. HUD stays below y ~270 (already true). Cover title stays inside the 3:4 grid crop (y 240-1680; already true).
- **Length test (non-Jess Day episodes only):** 35-50 s with the full sitcom shape (3c0: the ask -> 3 escalating attempts with a callback -> real test -> chat payoff -> vote). The hook still lands by 1 s and the chat by 8 s. Bonuses stay 20-26 s. Socialinsider 2026: 45-60 s Reels have 2.2x the median views of 1-30 s Reels (a correlation). Judge by avg watch time AND views at 24 h vs the page's last 3 Day episodes, and log the result.
- **Voice:** non-Jess Day episodes try speed 1.10 (from 1.18) with more full stops before reveals. "Unnatural voice" is the #2 reason viewers say a video feels AI.
- **Sends:** every non-Jess Reel ends with a send sticker + caption line 2 send ask (5i).
- **Jess test queue (one lever per morning bonus, keep rule from 5i):** T1 send prompt (Nov 26) -> T2 vote wording without "1 or 2" (Nov 27) -> T3 `motion: true` (Nov 28) -> T4 captions at y ~1200 (safe zone) -> T5 loop ending -> T6 third daily Reel. If a test drops her below the bar, revert and move to the next.
- **Series linking:** Instagram's "link reels into a series" (next-episode button) has no API. It's on Boris's in-app list in the daily report: link each page's Reels in order, Jess first.
- **YouTube Shorts (Boris approved Nov 25):** see 5k once the channel is connected in Windsor (get_connectors shows a youtube account).
- **Don't:** post the same video on two of our Instagram accounts (originality penalty), use other apps' watermarks, use coordinated likes or comments between our own accounts, or use like/follow CTAs.

## 5k. YouTube Shorts cross-post (Boris approved Nov 25; active once `get_connectors` lists a youtube account)
- Each main run, after Jess's episode is live on Instagram: `execute_action` youtube `upload_video` with the same `jess/dNN.mp4` (clean file, no watermark), title "<hook line> | 30 Days to the Wedding, Day N #shorts" (<= 100 chars), a description with the premise + "New episode every day" + 3 hashtags (#shorts #storytime #glowup), privacy public. Add it to a playlist "Season 1: 30 Days to the Wedding" (`add_video_to_playlist`) if one exists. Morning bonuses go up too, titled "Bonus: ...".
- On YouTube the vote line becomes "Comment what she should do" (no numbers). Reply to genuine YouTube comments with `reply_to_comment`.
- Log every upload in `state.youtube.log` (date, video id, source file). Check views after 24-48 h and compare with Instagram. If Shorts beat 1,000 views/video for a week, propose adding Danny next.
- Never upload another page's video to Jess's channel.

## 5l. Nov 25 night (Boris live): "Jess is the main focus, Theo second. Put what's working on Jess onto every other account. Make the IntelliStudy videos more niche and different from each other."
Why: Jess D5 (18103405238426994, 25.7 s) had 1,406 views, 25 likes, **27.4% skip** (best on any account ever) and 12.6 s avg watch after ~1 h 40 min. Every earlier Jess Reel stalled at 1,500-1,850; D5 passed that in under 2 h. The other pages sit at 100-470.

### 5l.1 Priority (every run)
1. **Jess**: written, rendered and checked first, with the most care. Her baseline rules in 5i still apply (one test lever at a time, on the morning bonus only).
2. **Theo**: second, same care. Then Danny, Malik, Rosie, Horde, History.

### 5l.2 The Jess formula = the default for EVERY story page (Theo, Danny, Malik, Rosie, Horde/Wes)
1. **A premise a stranger gets in one line**, built on a relationship stake: the ex + an event with a date (wedding / party / reunion / tourney / cook-off / court order). It's in hook line 1 or the chat. Never open on "Day N".
2. **Length 22-26 s, four scenes: s1 -> sc -> s3 -> sv.** s1 = the fail in 3 short hook lines (each line <= ~19 characters, a concrete number or object: "Mom brought pliers."). sc = the chat with the ex/rival, starting by ~6 s. s3 = escalation -> payoff + one new twist. sv = the vote by ~20 s.
   - **The 35-50 s length test (5j) ends.** Exception: if, at 24 h, a page's Nov 25 test episode (Theo D9 17916808875502650, Danny D5 18090873785322193, Malik D9 18111738383182141, Rosie D9 17883758289550779) beats that page's last 3 Day episodes on BOTH views and avg watch, that page may run one more test cut. Otherwise go back to 22-26 s. Log the result.
3. **3-4 new pictures per Reel, and a drawn prop that IS the joke** (pliers, the "SENT TO: RYAN" tag, Grandma's sewing kit, glued place cards). Toon pages: new toon.py looks every Reel. Theo: PIL props + small cloud face edits that show the fix (e.g. theo_d09_smile.jpg). Props go inside x 230-850, y 1000-1450 so the camera push doesn't crop them.
4. **A real comment card in the first second** (the winning vote, verbatim, with its real like count), and again at ~9 s. Zero votes? Use a "VOTES SO FAR: 0" sticker, never a fake card.
5. **A running callback gag** that pays off every episode (Jess's "ha" count, now #6). Each page gets one: Theo = Maya's "who is the suit for?", Danny = the 1-star review / "CEO", Malik = "that's one... that's two" (Coach Reyes), Rosie = "How does Julian know?", Wes = Cole's ALL CAPS texts.
6. **Family side characters with one line each** (Mom, Grandma, sister, Aunt Linda), plus the ex's new partner as a friendly threat.
7. **Cover = the fail, not the fix** ("IT WON'T ZIP", "INTO THE TRASH"). Build it from the hook image (the engine's automatic cover uses the LAST beat image; rebuild it when they differ).
8. **Morning single-moment bonus** on every page: one absurd beat that keeps the vote open.
9. Platform rules from 5j stay on every page (they're about Instagram, not format): natural-question vote wording on non-Jess pages, the IG safe zones, a send sticker + a caption line-2 send ask. On non-Jess pages, `motion` stays until the 24 h comparison above. If the test cuts lose, try the Jess setup exactly (no motion, voice speed 1.15-1.18).

### 5l.3 The 24 h Jess review (due Nov 26 ~6 PM ET, then for every Jess Day episode)
At ~24 h, pull Jess D5's numbers: views, reach, skip, avg watch, likes, comments, shares, saves, and views at 2 h / 24 h. Compare with her last 6 Reels and write "what could have gone better" in `state.series.jess.experiments.results` + lessons:
- Shares (D5 had 0 at 2 h; sends drive reach to non-followers).
- Comments (0 at 2 h: was the 1-or-2 ask answerable? was there a comment card?).
- Where viewers left: avg watch vs scene timings (s1 0-5.6 s, sc 5.6-13.4 s, s3 13.4-21.4 s, sv 21.4-25.7 s).
- Cover/title, posting time, hook wording.
Then turn each finding into ONE change for the next test slot (5i: on the morning bonus, one lever at a time). Copy anything that clearly worked to Theo, then to the other pages.

### 5l.4 IntelliStudy videos (@intellistuddy): niche, and no two alike
Data: r001-r003 got 95-100% skip and 1-2 s avg watch. They were three versions of the same video (generic notes -> 3 flashcards, same layout, same hook style).
- **One niche per video, written for that exact student** (first words on screen = the niche): e.g. "Nursing students: pharm exam tomorrow", "AP US History: 40 terms by Friday", "IGCSE Biology Paper 2", "GCSE Chemistry: moles", "Med school anatomy: brachial plexus", "Spanish vocab: 50 words", "SAT vocab", "Law school: case names". Never the same subject twice in 7 days.
- **Rotate formats; never the same format two posts in a row**:
  (a) POV panic, then the payoff;
  (b) race: writing cards by hand vs the app, with a real timer;
  (c) quiz the viewer: show 3 real generated cards as questions, answers in the comments;
  (d) "I turned [a public-domain text, e.g. the Gettysburg Address] into flashcards";
  (e) one feature per video, a different section of the app each time (quiz mode, spaced repetition, PDF/photo upload) and only if it really works that day;
  (f) a 12-15 s study-with-me timelapse with a single text hook.
- **Every first frame looks different** (colour, layout, zoom). Open on the payoff (finished cards, zoomed in), never a static landing page.
- Real screen recordings, real numbers, honest claims only (5g). Log `niche` + `format` for each post in `state.intellistudy.log` and check the last 7 entries before choosing.

## 5m. Nov 25 night (Boris live): per-account changes for every page except Jess ("you decide; soft shifts, never a restart")
Jess doesn't change. Each shift below continues the running story: no "new series", no Day 1 again, same handle, same HUD.

### Theo (no niche change)
- The premise works and he has the only loyal commenters (5sta.r.angel, ivannn_720). The blocker is the pictures: one 3D face reused for 9 days. **Ask Boris for a live session: 10-12 new 3D images, same Theo** (fixed brows, real smile, suit, at the gym, at school, plus Maya and Jake as characters).
- Like Jess: put the ex IN the scenes, not only in texts (Maya seeing him at the worst moment = s3 every episode). His regulars become characters by handle (5sta.r.angel = Maya's best friend, ivannn_720 = his barber) after asking them in a reply.

### Danny (soft shift: three lies -> one rom-com rivalry)
- "Make 3 lies true" is too much for a stranger to take in at 2 s. From Day 6, the one-line stake is "**His high school bully's sister is into him, and the reunion is in N days.**" Tara = the romance (Jess-style chats), Brock = the rival. The lies stay as the comedy engine (HUD LIES TRUE stays), not the hook.

### Malik (soft shift: training show -> high-school drama, basketball as the backdrop)
- 0 comments ever on a pure "road to the NBA" training story; the drama beats (Jada, aisle 4) got his best skip rates. From Day 10, every episode leads with the people (Jada, Tyler, Mom, Coach Reyes, chem class), and the basketball skill is the fix. The tourney (Dec 4) stays the deadline. This also gives IntelliStudy a natural home (grades = eligibility).

### Rosie (soft shift: recipe show -> rom-com rivalry in a kitchen)
- 0 comments ever; recipe viewers and story viewers are different people. From Day 10 the story is Rosie vs Julian (her ex, the favorite) with Marco and Dee. The dish is the battlefield; the hook is always Julian/Marco. Keep the real recipe in the caption plus one 2-second "THE TRICK" sticker in the Reel (save bait).

### Trash Horde (the Wes story is the show; the real game moves to the background)
- 0 real hauls in 7 days with 0 followers: the game can't headline yet. Wes's sitcom (community service, his ex's boyfriend as his boss, trash monsters at night) is the show. HORDE HP + "comment your haul + city" stays as one sticker + one caption line. Stop announcing nightly regen in hooks. Real hauls are still counted and credited exactly (5c), and the first real haul becomes a big episode beat.

### History (recurring host: Gus, the museum night guard)
- Faceless art slideshows = 52-60% skip, 0 followers. From the next episode (Story #6, not a restart), every story is told by **Gus** (toon `who: gus`, base `pipeline/assets/gus_toon_base.jpg`, navy guard shirt, grey beard), a museum night guard who tells one true story per night after closing, standing next to the "exhibit" (the public-domain archival image, shown as a framed beat). Same voice every time: Kokoro `bm_george`, speed 1.08 (engine.py now uses lang en-gb for b* voices automatically). Ready-made looks: `gus_toon_base/point/shock/phone.jpg` in the new toon scene `museum` (the frame on the wall is decoration; show the real archival image as its own full-screen beat right after Gus points at it).
- Running gag: the museum director texting "GUS. STOP TALKING TO THE EXHIBITS." Format = the Jess formula (hook = the most absurd true fact, 25-35 s, a chat beat at ~6 s, vote "which story tonight?"). Fact-checking and sources in the caption don't change. First Gus caption: "(new host, same true stories)".

### IntelliStudy (@intellistuddy): Boris's idea, adopted: a long-running student story
- **Kai, 15** (toon `who: kai`, base `pipeline/assets/kai_toon_base.jpg`). Season 1 = the months to his IGCSE exams in the May/June exam season (verify the dates with a web search before showing a countdown). Season 2 = the IB Diploma (2 years). One episode a day, Jess formula: a deadline + a relationship stake (e.g. his older sister got straight 9s and their parents compare them; the friend who says studying is for nerds), one study fix per day voted in the comments, HUD DAYS TO EXAMS / PREDICTED GRADE / FOCUS.
- Every episode contains a **real IntelliStudy screen recording** of the thing Kai does that day (made from the live site per 5g: real notes for his subject, real generated cards/quiz), shown as his phone screen. Only real features, as they work that day.
- **Honesty:** Kai is an animated character (say "animated story" in captions). His grades are story, never a claim about the app ("X% better grades", reviews and user counts stay banned). Study tips must be real techniques (active recall, spaced repetition, past papers).
- Daily mix on @intellistuddy: 2 Kai episodes/bonuses + 1 niche demo from 5l.4. Kai's subjects rotate through the IGCSE subjects the niche demos cover, so both formats feed each other.
- Note: the @intellistuddy scheduled task wasn't visible from the main run's session (Nov 25). If it doesn't read this runbook, Boris has to add this to its prompt.

## 5n. Nov 26 (Boris shared Jess's in-app Insights + a growth checklist): the bottleneck is shares, comments and follows, not the hook
**Jess's Insights (from Boris, in-app; Windsor can't read these):** skip 31.9-35.6% (winning), avg watch 11-12 s on 25 s (~45-48% complete, a steady drop after 3 s), share rate 0.1-0.3%, comment rate 0-0.4%, **65 profile visits -> 0 follows**, 99.4% non-followers, ~72% aged 13-24. Instagram ranks skip rate first and share rate second, and our share rate is close to zero. So the 1.5K cap comes from sends, rewatches and follows.

### 5n.1 Every page except Jess, from the next Reel (Jess gets these one at a time via 5n.2)
1. **One "send this to..." gag per Reel**: a painfully specific, relatable moment for 13-24 year olds that someone sends to their group chat as "literally you" (the zipper, the hostage smile, 4 push-ups). Put it in s3 and match the send sticker to it ("SEND THIS TO THE FRIEND WHO...").
2. **Aura-swing gag stickers**: absurd in-story aura hits as comedy stickers ("-5,000 AURA" when the zipper breaks, "+300 AURA" for the comeback), plus a caption question that starts a debate ("How much aura did he lose at the brow bar?"). They're clearly jokes. The HUD AURA tile stays REAL engagement (3b.2) and is never inflated.
3. **One hidden detail per Reel**: a small background gag or a 0.5 s text flash in a corner (a sign, a phone lock screen, a name on a cup) that rewards a rewatch and gets "did anyone see...?" comments. Keep it out of the IG UI zones (5j).
4. **A seamless loop**: the last frame and line lead back into the first (the last image = the hook image; the last voice line sets up the hook line).
5. **An open loop at the end**: stop right before a reveal ("He's typing..." / "Then the door opened.") and say what's next ("Tomorrow: Thanksgiving, next to Ryan").
6. **Every episode works alone**: a stranger seeing Day 14 first still gets a full mini-story (problem -> 3 attempts -> payoff) inside the bigger goal.
7. **Bigger stakes every 5 days**: Days 10, 15, 20, 25 and 30 are major twist or "boss" episodes (plan them in state: Jess D10, Theo D10, Danny D10, Malik D10 = tourney week, Rosie D10).
8. **Length test, morning bonus only**: cut the bonus to 12-15 s (one gag, one punchline, the loop). If its avg watch / length beats the page's last 3 bonuses, keep it short. Day episodes stay 22-26 s (5l).
9. **Keywords**: say the niche words in the voice, show them on screen, and put them in caption line 1 ("glow up", "ex", "wedding", "basketball", "cook-off", "true story"), plus niche hashtags (5b).
10. **Reply to every comment within the run** and end replies with a question. (The API can't comment on other accounts or post video replies; don't try.)

### 5n.2 Jess test queue (replaces the 5i/5j order; one lever per morning bonus, keep rule from 5i)
- **T1 (Nov 26 AM bonus): send gag + send prompt.** One group-chat-relatable beat, the sticker "SEND THIS TO THE FRIEND WHO..." matching it, and the same ask in caption line 2. Measures shares/reach.
- **T2 (Fri Nov 27): RSVP guest list + follower milestones (5o).** Measures comments + follows.
- **T3 (Nov 28): aura-swing stickers + an aura-debate caption question.** Measures comments.
- **T3b (Nov 29): a 12-15 s bonus** (one gag + punchline + loop ending). Measures completion and rewatches.
- **T4: seamless loop ending** (if T3 didn't already prove it).
- **T5: vote wording without "1 or 2"**, then T6 `motion`, T7 captions at y ~1200, T8 a third daily Reel.
Day episodes stay on the baseline until a test passes the 5i keep rule; then it moves onto the episodes.

### 5n.3 Profile -> follow (Boris does these in the app; the API can't edit profiles or pin posts)
Every Jess cover says "DAY N" huge (bonus covers: "DAY N.5" or "BONUS"). Bio proposal for Jess: "Her ex is the best man at her sister's wedding 💍 / Can she hit 100% glow-up in 30 days? / You pick the fix 👇 Day 1 pinned". Pin Day 1 + the best episode (D5) + the newest milestone. Same pattern for Theo. Check follows per profile visit in Boris's Insights when he shares them.

## 5o. Jess: the wedding guest list + follower milestones (Boris approved, Nov 26)
**RSVP guest list (from Fri Nov 27 AM bonus, then every episode):** Mom hands Jess the wedding guest list. Line (an open question, NOT "comment RSVP": Instagram names "comment a specific word" as engagement bait): "Want a seat at the wedding? Who are you bringing?" Everyone whose comment asks for a seat / says they're coming / names a plus-one (the word RSVP also counts) goes into `state.series.jess.guest_list` (handle, date, comment id), and gets a reply: "You're on the list 💌 Table TBD". Only handles that opted in by asking for a seat ever go on screen; never invent guests. Every 3-4 days a quick seating-chart gag puts real RSVP handles on place cards (callback to the glued place card), and the comments pick tables ("next to Ryan?", "kids' table?"). "Tag who you're bringing" goes in caption line 2 (tags = shares/comments). Day 30 finale: the real place cards with every RSVP handle.
**Follower milestones = story rewards (bonus content only; they never override a vote):** shown as a fact, never as "follow for X": a small vote-screen sticker "GUESTS 11/25" + caption line "At 25 guests: Jess's maid-of-honor speech draft." Use the real `followers_count` from Windsor each run.
- 25: Jess's maid-of-honor speech draft (a disaster bonus Reel)
- 50: the full dress + glam reveal Reel
- 100: viewers pick what goes wrong for Ryan at the rehearsal dinner (a comment vote)
- 250: Grandma gets her own episode
- 500: a seating-chart episode with every RSVP handle so far
- 1K: commenters write Jess's wedding toast (top comment lines used, credited by handle)
When a milestone is hit, post the reward as that day's extra Reel (keep the 2-hour spacing) and say so in the caption ("You hit 50. As promised:"). This launches on Jess as the T2 test slot (Fri Nov 27); if it lifts comments without dropping her below the 5i bar, it moves onto her Day episodes and the pattern gets copied to Theo (his `follower_ladder` already exists) and then the other pages.

## 5p. Nov 26 deep research (report: reports/Growing animated Reels story series.md; notes: research_notes/Growing animated Reels story series/)
Bottom line: Jess isn't penalized; ~1,500 views is the normal ceiling for <2K-follower accounts (median ~1,484). Her hook beats the averages (skip 32-36% vs ~65% for small accounts; 11-12 s watch vs ~8.5 s). To break out she needs **sends per reach (target 0.5-1%, now ~0.1-0.3%)** and **profile follows**. The other pages (100-470 views) first need to clear the retention gate (5i) before sends matter.
1. **Vote wording on every page incl. Jess's bonus tests:** Instagram's own example of engagement bait is "comment a specific word, number, or emoji". Move Jess's "1 or 2" test (5n.2 T5) up to the **Sun Nov 29** bonus; non-Jess pages already use open questions. The next episode still opens on real viewer comments (the proven Fruit Love Island loop). Optional for Boris: a daily Story poll sticker by hand (the API can't add stickers).
2. **A send trigger in every Reel** (5n.1.1): one person-specific, high-arousal beat (petty win, jaw-drop reveal, "the friend who..."). Never end on sadness (sad content gets shared less).
3. **Cold-viewer legibility:** the series name + day number readable in the first second (HUD/pill), then the most charged frame.
4. **Caption line 1 = a searchable headline:** series name + Day + genre words ("30 Days to the Wedding, Day 6: animated glow-up revenge story..."), with the same words in on-screen text/subtitles; 5 hashtags max (they're labels, not reach).
5. **Length:** Buffer (Nov 2026, 2.7M Reels): 90-179 s +7.4% reach vs baseline, 15-29 s -0.9%, 3 min+ -49%. Small effect; the test stays one lever at a time: Jess T9 = a 45-60 s bonus (after the queue above), non-Jess = the 5l comparison.
6. **AI label (Sept 2026 rule):** accounts whose persona is an AI-generated person must turn on the profile "AI creator / AI-generated" label (unlabeled ones can lose recommendations). That's **Theo** (Leonardo 3D). The cartoon pages (Jess, Danny, Malik, Rosie, Wes, Gus, Kai) are "made with AI tools", no profile label needed. Never pass Theo off as a real person.
7. **No boosting yet** (visits don't convert to follows until the profile fix). **Trial Reels** via `trial_params` once a page has 1,000+ followers.
8. **Cross-posting own clean files is allowed** (the crackdowns target reposting others' content and visible watermarks). Small accounts average more views on TikTok (~2,429) than Reels (~1,484): **Boris (Nov 26): he can't post by hand, so cross-posting happens ONLY automatically:** YouTube Shorts via Windsor `execute_action` youtube `upload_video` (Windsor has it; active once get_connectors lists a youtube account, see 5k), TikTok via the Buffer connector if it shows up in this session's tools (check ToolSearch "buffer"). If neither is connected, Instagram only; never ask Boris to upload by hand.
9. **Theo look (Nov 26):** new default images `theo_teeth_drawnbrow.jpg` (current continuity: eyeliner brow) and `theo_teeth_clean.jpg` (both brows, use once the story says the brow grew back): a real smile with visible teeth, made by `pipeline/theo_teeth_edit.py` (OpenCV warp + teeth). Use them from Theo's next Reel; real new 3D scenes still need Boris's Leonardo images.

## 5q. Buffer cross-posting (Boris, Nov 26: "use Buffer for this"; he can't post by hand)
**Done by its own scheduled task "Cross-post Jess to TikTok + YouTube (Buffer)" (trig_013qYYXnMSEeVQQ5pAjMEkZK, 8:41 AM + 6:41 PM ET, Buffer attached). The main and extras runs do NOT cross-post (avoids duplicates); they just keep making the Jess files under jess/.**
Buffer is connected (org "My Organization", id 648a4579a7af12840277c415, free plan: 3 channels, 10 scheduled posts). Connected Nov 26: **TikTok `jessweddingglowup` (Jess, channel 6b0792328541f09ecba7f803)** and **YouTube 6b07924c8541f09ecba7f889 (= JESS's channel; Boris is renaming it from 'Youdecidewhatsnext'; post only Jess there)**. One free slot left (Theo TikTok or a Jess YouTube channel). **Catch-up:** both channels are new mid-series, so each run posts the next 2 backlog episodes in order (Jess TikTok: D1 posted Nov 26 01:59 UTC, then D2, D3...; Jess YouTube: from Day 1) plus that day's new episode, until caught up. TikTok/YouTube comments can't be read here, so their captions never ask for votes; votes come from Instagram only. Each run: ToolSearch "buffer" -> `mcp__Buffer__list_channels` (org above). For every connected channel, right after the matching Instagram Reel is live:
- `mcp__Buffer__create_post` with `channelId` (exact id from list_channels), `schedulingType: "automatic"`, `mode: "shareNow"`, `assets: [{"video": {"url": "https://raw.githubusercontent.com/vf6wgv2845-prog/media/main/<path>.mp4"}}]`, and a caption WITHOUT Instagram-only lines (no "link in bio" promises, no IG handles). TikTok: `metadata.tiktok = {"title": "<hook>", "isAiGenerated": true}`. YouTube: `metadata.youtube = {"type": "short", "title": "<hook> | 30 Days to the Wedding, Day N #shorts" (<=100 chars), "categoryId": "24", "madeForKids": false, "isAiGenerated": true, "privacy": "public"}`.
- `isAiGenerated: true` on everything (AI voice/visuals; unlabeled AI got Fruit Love Island's episodes removed).
- Episodes only (+ morning bonuses for Jess if the channel takes them); same clean file, no watermark. Log each post in `state.youtube.log` / `state.tiktok_log` (date, channel, Buffer post id, source file).
- If a Buffer call fails, retry once, then report it; never ask Boris to upload by hand. If list_channels is empty, skip silently and note "Buffer: no channels yet" in the report.

## 5r. Running without Boris (Nov 26 audit: "imagine I never text again")
Every run must keep going with zero input from Boris. Rules for the situations that would otherwise stall:
1. **Day 30 finales -> Season 2, same page, no gap.** Finales land around Dec 16-24 (Theo/Malik/Rosie ~Dec 16, Jess/Danny ~Dec 21, Wes ~Dec 24). On Day 27 the vote includes the Season 2 goal (2 options a stranger gets in one line, e.g. Jess: "the honeymoon he wasn't invited to" vs "her own wedding in 30 days"). Day 30 = the payoff + the Season 2 hook; the next day = S2 Day 1 with a new countdown, same character, same HUD style. Malik follows his season_plan. Never stop posting because a season ended.
2. **Windsor trial ends ~Dec 17 (plan: TRIAL, unpaid).** From Dec 10, put "Windsor trial ends ~Dec 17: pay or Instagram posting stops" at the TOP of every daily report and push. If a Windsor call fails with a plan/trial/auth error: (a) keep building the videos and committing them; (b) if Buffer has an Instagram channel (list_channels), post the Jess episode through Buffer (`metadata.instagram = {"type": "reel", "shouldShareToFeed": true}`) as the fallback; (c) notify Boris once per day with the exact error. Don't retry Windsor in loops.
3. **Repo size** (~600 MB after 8 days, ~+70 MB/day). Clone with `git clone --depth 1` when starting fresh (pushing still works). If the repo passes ~3 GB, tell Boris in the report (GitHub warns at large sizes); never delete published files that a post may still be fetching.
4. **Git conflicts** (several tasks push the same repo): always `git pull --rebase` right before pushing; on a state.json conflict take the newest file and re-apply only your own changes, never drop another run's entries.
5. **Report cleanup:** Boris does NOT upload anything by hand anymore. Skip the "TikTok caption + YouTube title for Theo" item; cross-posting is the Buffer task's job (5q). Only list things only he can do (payments, logins, in-app profile/pin/series steps, new Leonardo images).
6. **IntelliStudy (@intellistuddy):** Boris approved (Nov 26: "keep posting on every account, even the IntelliStudy"). Its own task now exists: "IntelliStudy: Kai's IGCSE story + niche demos" (trig_01AgSkiuGQnH7WbTogHmebtn, 8:13 AM / 3:13 PM / 8:13 PM ET). The main and extras runs still don't post there; the main report includes one line on @intellistuddy's numbers.
8. **Weekly improvement loop (Boris, Nov 26: "keep improving, look at the results and improve on them"):** every **Sunday main run**, before writing episodes, also do the weekly review: pull the last 7 days of every account (Instagram via Windsor; Jess TikTok/YouTube via Buffer metrics), compute per account the median views, best/worst post, sends per reach, comments per 1,000 views and follower change, find what separates winners from losers, and write at most 2 changes per account for next week into a new dated section "5w-<date> Weekly review" (Jess: one test lever at a time). Add a short weekly summary block at the top of that day's report (median views this week vs last, followers, best post + why, the changes made). Real numbers only.
7. **Comments to watch for:** if a commenter asks to be removed from the guest list or from an episode, remove their handle from all future episodes and reply politely. Hide abusive comments (hide_comment); never argue.

## 4. Render and check
`KOKORO_MODEL=/tmp/tts/kokoro.onnx KOKORO_VOICES=/tmp/tts/voices.bin python3 -I pipeline/make_episode.py pipeline/episodes/X.json /tmp/X stills` -> look at `/tmp/X/contact.jpg` (text must not overflow the 1080px width; shorten lines if it does), then run again without `stills` for `final.mp4` + `cover.jpg`.

## 5. Publish
Copy outputs into the repo (`malik/s1dNN.mp4`, `rosie/dNN.mp4`, `theo/dayNN.mp4` + `_cover.jpg`), commit, `git -c push.negotiate=true push origin HEAD`.
Post with `execute_action` `create_video_post`: `video_url` = `https://raw.githubusercontent.com/vf6wgv2845-prog/media/main/<path>`, `cover_url`, `share_to_feed: true`, a caption with the hook (3b.10), the vote options numbered, the cameo ask (3b.4), "Follow so you don't miss Day N+2", and hashtags per section 5b. Tag any commenter who appears in the episode.
After posting: `python3 -I pipeline/score.py <series> ... --save` so the next episode's AURA starts from the right number.
Also post one story per account (`create_story`), AND post the full episode video itself as a story too (create_story video_url, Reels under 60 s) so followers see the whole episode (Boris, Nov 21). **Every story is made with `python3 -I pipeline/story_card.py spec.json`** (see its docstring): HUD tiles identical to that day's Reel, a sticker headline, and then either (a) tracker: stat bars + day log, or (b) teaser: flip-calendar + one REAL comment card + the vote question; always a CTA sticker ("VOTE ON THE NEWEST REEL"). Extra/midday stories use the same tool. **Highlights (Boris, Nov 21: wanted again):** after each episode, also make that day's highlight card with `pipeline/highlight_card.py` (character photo up front, DAY N + title, 3 rows You voted / The fix / The twist, days-left calendar; Boris wants the character visible, never icons), save it as highlights/<series>/dayNN.jpg, post it as a story, and remind Boris in the report to make a NEW highlight for that day (Boris, Nov 21: one highlight per day per account, named "DAY N"): the day card + that day's bonus/special Reels + the episode Reel, all posted as stories in that order (Reels under 60 s can be posted as story videos via create_story video_url). Also make the round cover with `highlight_card.py` (spec key "cover": {out: highlights/<acc>/cover_dayNN.jpg, image, cx, cy, side, ring, num: "D6"}) and attach it to the report. Same for each new Horde fact (highlights/horde/factNN.jpg -> FACTS). Boris adds stories to highlights himself (the API can't).

## 5b. Captions + hashtags (for engagement)
Instagram allows **max 5 hashtags per post** (since Dec 2025); posts over the limit may fail or get suppressed. Use exactly 5:
1. The series' branded tag from state.json (e.g. #TheosGlowUp) - always.
2-5. Four from that series' `hashtags.pool`, picked to fit THIS episode (e.g. a recipe day for Rosie -> #easyrecipes #dinnerideas; a game day for Malik -> #basketball #hoops). Never generic tags like #reels #explore #fyp #viral.
Caption structure (Instagram works like search now, so words matter more than tags):
- Line 1 = the hook in plain searchable words ("30-day glow up, Day 4: Theo finally fixes his skin").
- A question that invites comments (the vote) with numbered options.
- "Follow so you don't miss Day N+2."
- Hashtags last.
Carousels and extra posts (recipes, debates, recaps): slide 1 is a `story_card.py` image (HUD + sticker headline, e.g. "DAY 4 RECIPE" / "BIRRIA TACOS"; it's 9:16, so for 4:5 feed slides crop it to 1080x1350 keeping the top) and the caption follows 3b.10. Debate posts end with a comment question + the cameo ask.
Debate/recipe extra posts: same 5-tag rule (e.g. #nbadebate #basketball #whoyougot + 2 topical; #easyrecipes #dinnerideas + dish tags).
Each run: check last week's posts' reach/views (get_data media_reach/media_views) and append to `hashtag_log` in state.json which tags were used and how the post did; favour the tags that keep showing up on the best posts.

## 5c. The Trash Horde (@thetrashhorde): a community game, not a vote
Different from the 3 story series: no vote options. Each run:
1. Read all comments on the posts in `series.horde.count_comments_on` + the latest daily post. Parse each haul: pieces and/or lbs and a city (e.g. "14 pieces, Boston", "3 lbs cleveland", "2 bags"). A "bag" with no weight = 3 lbs. Ignore our own comments and anything that isn't a haul. Each comment counts once (track comment ids in state).
2. Damage = pieces*1 + lbs*10. Apply the verification rule in state (big claims need photo proof first). Update totals, boss HP, city leaderboard, top cleaners.
3. Post a daily battle Reel with make_episode.py in the 3b format (HUD from `score.py horde`, real haul comment cards, calendar to the boss deadline, stickers like "-140 HP", designed cover) (image `trash_horde.jpg` or a newer boss image, `numbered: false`, custom `cta` like "Comment your haul + city"): s1 = today's damage + boss HP left, s2 = stats as % bars (Boss HP, Streets cleaned, etc.), s3 = notification-style event (e.g. "Boston just dealt 120 damage"), s4 = leaderboard/top cleaners shoutout, s5 = 5 'how to' rows (gloves, bag, bin it, comment haul+city, tag a friend). If zero hauls yet, make the horde advance and rally people to make the first hit.
4. Reply to every haul comment ("💥 140 damage! Boston leads.") and shout out top cleaners by @ in the caption.
5. Sunday: boss result Reel (beaten or the horde spreads), then introduce next week's boss (new zombie type, HP based on last week's total).
6. Report totals honestly as community-reported vs verified. Hashtags: #TrashHorde + 4 from #litterpicking #cleanup #environment #pickuplitter #plasticfree #cleanupchallenge.


## 5d. Posting plan (Boris, Nov 20: Claude decides when/what to post, driven by the data; Windsor trial ends ~Dec 17)
Data on Nov 20: Theo 21 followers, every other account 0. Stories and feed images only reach followers, and carousels have shown 0 reach every time, so with 0 followers growth comes from **Reels reaching non-followers**. Extra posts must be extra Reels, each with a NEW story beat (never a repost or recap-only).
Proof it works: Theo Day 4 (new format) = best skip rate yet 45.6%, 9.4 s avg watch, 7 likes + 3 comments in the first hour; Theo's 6 AM bonus Reel = 10.3 s avg watch + the first 2 shares.
Daily slots (ET):
- **7:37 AM extras run**: Theo morning bonus Reel (a small real-life moment between episodes: alarm, gym, school hallway, a text from Maya); Trash Horde morning Reel.
- **1:37 PM extras run**: Trash Horde midday Reel.
- **5:45 PM main run**: every series' episode + one story per account (stories stay: they cost nothing and keep the few followers hooked).
Trash Horde gets the most volume (3 Reels/day) because it's the game account and needs players. Formats to rotate in the extra slots (all 3b format, real numbers only):
 a) "60-second challenge": what you can pick up in 60 s (tips, safety, comment your haul + city);
 b) one verified litter fact (web-search it first, cite the source in the caption, e.g. how long a can/cigarette butt lasts);
 c) "the horde advances": map/boss HP update, a countdown to Sunday, rally the first hit;
 d) as soon as real hauls arrive: every haul becomes its own shout-out Reel/story ("Captain @handle hit for 40").
 Never fake a cleanup, a haul, a photo or a city. Stories and carousels for the Horde come back once it has followers (re-check followers_count each run).
Each extras run: check the last 48 h of skip rate / avg watch / likes / comments / shares per account and pick the format and hook style that's winning (log the choice in `lessons`). If an extra slot's Reels keep underperforming the evening ones for 3 days, drop or move that slot and say so in the report.

## 6. Engage
Reply to up to 5 genuine new comments per account (`reply_to_comment`), short and in-character for the account. Never argue, never reply to spam/hate (hide it with `hide_comment` if it's abusive).


## 6b. Learning loop (Boris, Nov 20: more accounts is fine as long as every one gets full attention, and lessons from every account improve all of them)
Each run, before writing episodes, pull every Reel from the last 7 days on ALL accounts (views, reach, likes, comments, shares, saves; plus skip rate/avg watch time if the connector gives them) and add one line per post to `state.json` `learning_log`: account, day, hook line 1, cover title, length, and the numbers at ~24h.
Then write 1-3 short `lessons` (state.json) comparing posts across accounts: which hooks, covers, lengths, vote options, cameo asks and posting times did better, and what flopped. Apply the current lessons to EVERY account's next episode, and say in the report which lesson you applied. Never copy another account's story, only what worked mechanically.

## 7. Save state + report
Update `state.json` (day, last_post_date, last_media_id, stats, open_vote, any new cast/threads) and commit.
Then message Boris: what posted on each account, the vote counts that decided each episode, current views/likes/comments per account, and anything that needs him (e.g. Theo visual upgrade, Windsor trial ending).

## Never
- Never post photos of real people (athletes etc.) or fake AI photos of real people.
- Never pretend AI food photos are real food someone cooked; note "AI image" in captions.
- Never post the same episode twice. If a post fails, retry once, then report.
