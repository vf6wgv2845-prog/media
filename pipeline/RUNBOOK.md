# Daily run: Boris's Instagram story accounts (6)

Owner: Boris. He has given standing permission to post on all accounts in `state.json` `accounts`: Theo, Malik, Rosie, Trash Horde, and (once set up) the two new Theo-style glow-up pages Jess and Danny.
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
Until the extra time slots exist as scheduled tasks, the 5:45 PM run posts: Horde queue item first (from state.json `post_queue`), then all episodes + stories, then the Horde battle Reel last (natural ~20-30 min spacing). Never post two Reels on one account within 15 minutes.

## 4. Render and check
`KOKORO_MODEL=/tmp/tts/kokoro.onnx KOKORO_VOICES=/tmp/tts/voices.bin python3 -I pipeline/make_episode.py pipeline/episodes/X.json /tmp/X stills` -> look at `/tmp/X/contact.jpg` (text must not overflow the 1080px width; shorten lines if it does), then run again without `stills` for `final.mp4` + `cover.jpg`.

## 5. Publish
Copy outputs into the repo (`malik/s1dNN.mp4`, `rosie/dNN.mp4`, `theo/dayNN.mp4` + `_cover.jpg`), commit, `git -c push.negotiate=true push origin HEAD`.
Post with `execute_action` `create_video_post`: `video_url` = `https://raw.githubusercontent.com/vf6wgv2845-prog/media/main/<path>`, `cover_url`, `share_to_feed: true`, a caption with the hook (3b.10), the vote options numbered, the cameo ask (3b.4), "Follow so you don't miss Day N+2", and hashtags per section 5b. Tag any commenter who appears in the episode.
After posting: `python3 -I pipeline/score.py <series> ... --save` so the next episode's AURA starts from the right number.
Also post one story per account (`create_story`). **Every story is made with `python3 -I pipeline/story_card.py spec.json`** (see its docstring): HUD tiles identical to that day's Reel, a sticker headline, and then either (a) tracker: stat bars + day log, or (b) teaser: flip-calendar + one REAL comment card + the vote question; always a CTA sticker ("VOTE ON THE NEWEST REEL"). Extra/midday stories use the same tool. (No highlights: Boris decided not to use them.)

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
