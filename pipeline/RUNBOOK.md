# Daily run: Boris's 3 Instagram story accounts

Owner: Boris. He has given standing permission to post on these three accounts.
**Golden rule: the audience decides.** Every episode must follow the winning vote from the previous episode's comments. Never ignore, override or "improve on" a vote.

## 0. Setup (each run starts fresh)
1. Attach the repo: `add_repo` owner `vf6wgv2845-prog`, repo `media`, access `push`; clone to `/home/claude/media`.
2. Load Windsor tools with ToolSearch query `+Windsor`. Instagram connector id: `instagram`.
3. Install the free voice: `pip install --break-system-packages -q kokoro-onnx soundfile`, then download
   `https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx` -> `/tmp/tts/kokoro.onnx`
   and `.../voices-v1.0.bin` -> `/tmp/tts/voices.bin`.
4. Read `pipeline/state.json` (current day, stats, open vote, cast, rules for each series).

## 1. Check what's already posted today
`get_data` (connector `instagram`, fields `account_name, media_id, media_type, timestamp, media_caption`, date_preset `last_3dT`).
If a series already got its episode today (Boris did it live), skip that series' episode.

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

## 3b. Format lessons from @dalesglowup (studied Nov 19; copy the mechanics, never their jokes/characters)
Reference Reel: 1,338 comments, 1,356 reposts, 4,689 saves; previous ep 13.7K likes, 1.5K shares, 390 reposts. Why it works:
1. **Always-on HUD**: 3 big tiles top-left on every frame (DAYS LEFT / GLOW-UP % / AURA x/100). Viewers read progress instantly. For Theo: DAYS LEFT, GLOW-UP %, one engagement score.
2. **Engagement becomes the score, shown openly**: a "LAST EPISODE" board converts real shares/reposts/comments/likes into points (e.g. +1 per 1,000 shares, +1 per 100 reposts, +1 per 10K likes) -> total ticks up. Reposts are weighted highest, and that's what they get most of. Use real numbers from get_data only.
3. **Top commenter becomes a character**: the most-liked comment shown as a card (handle + like count), then that person appears in the episode ("Dr. Prince" the dentist). Do this for Theo: show the winning vote comment as a card and make its author a cameo (only with a public handle, nothing mean about them).
4. **One fix per day** stated as a rule: makes each vote matter and creates stakes.
5. **Absurd escalation + callback**: the fix goes wrong in funny ways (hammer, rubber bands, "industrial" braces), then a callback gag (magnetic braces -> stuck at a fridge store). Then the meter payoff badge (GLOW-UP +10%).
6. **Ending = sweet beat undercut by a gag** (crush smiles back -> he burps in her face). Leaves him short of the goal and feeds the next episode.
7. **Style**: word-by-word bold captions, low-centre, keywords coloured; tilted sticker/SFX labels for each beat (CLANK, BUURP); close-up inserts (mouth, etc.).
8. Caption opens with the recap of last episode's result ("Last episode gave Dale five more aura...").
Engine gaps (need make_episode.py work before they're possible): HUD overlay, word-by-word captions, sticker labels, comment-card scene. Until then: put the score in the stats scene, the top comment in the s3 notification card, and the rule + recap in s1.

## 4. Render and check
`KOKORO_MODEL=/tmp/tts/kokoro.onnx KOKORO_VOICES=/tmp/tts/voices.bin python3 -I pipeline/make_episode.py pipeline/episodes/X.json /tmp/X stills` -> look at `/tmp/X/contact.jpg` (text must not overflow the 1080px width; shorten lines if it does), then run again without `stills` for `final.mp4` + `cover.jpg`.

## 5. Publish
Copy outputs into the repo (`malik/s1dNN.mp4`, `rosie/dNN.mp4`, `theo/dayNN.mp4` + `_cover.jpg`), commit, `git -c push.negotiate=true push origin HEAD`.
Post with `execute_action` `create_video_post`: `video_url` = `https://raw.githubusercontent.com/vf6wgv2845-prog/media/main/<path>`, `cover_url`, `share_to_feed: true`, a caption with the hook, the vote options numbered, "Follow so you don't miss Day N+2", and hashtags per section 5b.
Also post one story per account (`create_story`, 1080x1920 JPEG made with PIL): an updated **Progress Tracker** card (same layout as `stories/2026-11-19_*_tracker.jpg`: character circle, title, Day N/30, stat bars, a short day-by-day log of what the votes decided, 'Vote on the newest Reel'). (No highlights: Boris decided not to use them.)

## 5b. Captions + hashtags (for engagement)
Instagram allows **max 5 hashtags per post** (since Dec 2025); posts over the limit may fail or get suppressed. Use exactly 5:
1. The series' branded tag from state.json (e.g. #TheosGlowUp) - always.
2-5. Four from that series' `hashtags.pool`, picked to fit THIS episode (e.g. a recipe day for Rosie -> #easyrecipes #dinnerideas; a game day for Malik -> #basketball #hoops). Never generic tags like #reels #explore #fyp #viral.
Caption structure (Instagram works like search now, so words matter more than tags):
- Line 1 = the hook in plain searchable words ("30-day glow up, Day 4: Theo finally fixes his skin").
- A question that invites comments (the vote) with numbered options.
- "Follow so you don't miss Day N+2."
- Hashtags last.
Debate/recipe extra posts: same 5-tag rule (e.g. #nbadebate #basketball #whoyougot + 2 topical; #easyrecipes #dinnerideas + dish tags).
Each run: check last week's posts' reach/views (get_data media_reach/media_views) and append to `hashtag_log` in state.json which tags were used and how the post did; favour the tags that keep showing up on the best posts.

## 5c. The Trash Horde (@thetrashhorde): a community game, not a vote
Different from the 3 story series: no vote options. Each run:
1. Read all comments on the posts in `series.horde.count_comments_on` + the latest daily post. Parse each haul: pieces and/or lbs and a city (e.g. "14 pieces, Boston", "3 lbs cleveland", "2 bags"). A "bag" with no weight = 3 lbs. Ignore our own comments and anything that isn't a haul. Each comment counts once (track comment ids in state).
2. Damage = pieces*1 + lbs*10. Apply the verification rule in state (big claims need photo proof first). Update totals, boss HP, city leaderboard, top cleaners.
3. Post a daily battle Reel with make_episode.py (image `trash_horde.jpg` or a newer boss image, `numbered: false`, custom `cta` like "Comment your haul + city"): s1 = today's damage + boss HP left, s2 = stats as % bars (Boss HP, Streets cleaned, etc.), s3 = notification-style event (e.g. "Boston just dealt 120 damage"), s4 = leaderboard/top cleaners shoutout, s5 = 5 'how to' rows (gloves, bag, bin it, comment haul+city, tag a friend). If zero hauls yet, make the horde advance and rally people to make the first hit.
4. Reply to every haul comment ("💥 140 damage! Boston leads.") and shout out top cleaners by @ in the caption.
5. Sunday: boss result Reel (beaten or the horde spreads), then introduce next week's boss (new zombie type, HP based on last week's total).
6. Report totals honestly as community-reported vs verified. Hashtags: #TrashHorde + 4 from #litterpicking #cleanup #environment #pickuplitter #plasticfree #cleanupchallenge.

## 6. Engage
Reply to up to 5 genuine new comments per account (`reply_to_comment`), short and in-character for the account. Never argue, never reply to spam/hate (hide it with `hide_comment` if it's abusive).

## 7. Save state + report
Update `state.json` (day, last_post_date, last_media_id, stats, open_vote, any new cast/threads) and commit.
Then message Boris: what posted on each account, the vote counts that decided each episode, current views/likes/comments per account, and anything that needs him (e.g. Theo visual upgrade, Windsor trial ending).

## Never
- Never post photos of real people (athletes etc.) or fake AI photos of real people.
- Never pretend AI food photos are real food someone cooked; note "AI image" in captions.
- Never post the same episode twice. If a post fails, retry once, then report.
