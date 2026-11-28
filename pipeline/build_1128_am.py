"""Builds the Nov 28 morning bonus configs (Jess T3 sitcom-length, Theo, Danny, Wes) from the Nov 27 morning configs."""
import json, os
E = os.path.join(os.path.dirname(os.path.abspath(__file__)), "episodes")
def load(n): return json.load(open(os.path.join(E, n + ".json")))
def save(n, c): json.dump(c, open(os.path.join(E, n + ".json"), "w"), indent=1, ensure_ascii=False); print(n)
YEL, RED, BLUE, DARK, GREEN, PINK, GREY = [255, 214, 102], [235, 80, 95], [90, 150, 240], [40, 40, 48], [102, 200, 92], [236, 110, 160], [190, 195, 205]
BLK, WHT = [15, 15, 15], [255, 255, 255]
def st(scene, line, text, bg, y, size, angle=-3, hold=1.6, delay=0.3, fg=None, **kw):
    d = {"scene": scene, "line": line, "text": text, "bg": bg, "y": y, "angle": angle, "size": size, "hold": hold, "delay": delay}
    if fg: d["fg"] = fg
    d.update(kw); return d
def card(scene, line, user, text, likes, y, hold=2.4, delay=0.15):
    return {"scene": scene, "line": line, "delay": delay, "user": user, "text": text, "likes": likes, "y": y, "hold": hold}

# ---------------- Jess: T3 = 35-40 s sitcom-length bonus (baseline otherwise: af_bella 1.18, no motion, captions y1500 s3, 1-or-2)
c = load("jess_bonus_1127")
c.update({
    "image": "jess_b1128_replyall.jpg", "pill": "DAY 6 / 30  •  BONUS",
    "hook": ["Grandma hit", "reply-all.", "Ryan's in the chat."], "hook_emoji": "💬",
    "name_line": "Saturday morning.", "sub_line": "Bonus  •  Day 7 drops tonight",
    "notif": {"from": "Mom", "msg": "glam or dance shoes. decide by tonight", "emoji": "", "color": [52, 199, 89]},
    "script": {
        "s1": [[0.1, "Grandma replied all in the wedding chat. Ryan is in the wedding chat."],
               [0.1, "Ten minutes earlier."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "Ryan texted. Chloe added me to the wedding chat. What color is your dress? For my tie."],
               [0.1, "She sent: ha. Tenth time."]],
        "s3": [[0.1, "Attempt one: she typed beige. Mom replied: it's blush, sweetie."],
               [0.1, "Attempt two: delete for everyone. She hit delete for me."],
               [0.1, "Attempt three: she left the chat. Chloe added her back. As maid of honor."],
               [0.1, "Then Grandma replied all. A photo from the fitting. The pliers."],
               [0.1, "Ryan: got the tie. Blush."],
               [0.1, "Then Walter texted. Also bought blush. Shall we match?"]],
        "sv": [[0.1, "Two dates in blush. Tonight: full glam, or dance lessons with Walter?"],
               [0.1, "Comment one or two."]]},
    "captions": {"scenes": ["s3"], "y": 1500, "keywords": ["beige", "blush", "sweetie", "delete", "everyone", "me", "maid", "honor", "grandma", "pliers", "tie", "walter", "match"]},
    "comments": [card("s1", 0, "kambri_133", "1", 0, 1450, hold=2.2), card("sv", 0, "kambri_133", "1", 0, 1650, hold=2.6, delay=0.3)],
    "stickers": [
        {"scene": "s1", "line": 0, "delay": 2.6, "kind": "calendar", "text": "25", "y": 1400, "hold": 2.0},
        st("s1", 1, "10 MIN EARLIER", DARK, 520, 74, fg=WHT, angle=-3, delay=0.1, hold=1.4),
        st("sc", 1, "HA #10", GREY, 1000, 100, fg=[20, 20, 20], angle=-4, hold=1.6, delay=0.2),
        st("s3", 0, "IT'S BLUSH.", PINK, 540, 84, angle=4, delay=1.6, hold=1.4),
        st("s3", 1, "DELETED FOR: ME", RED, 540, 76, angle=-4, delay=1.2, hold=1.4),
        st("s3", 2, "ADDED BACK", BLUE, 540, 84, angle=3, delay=0.9, hold=1.4),
        st("s3", 3, "THE PLIERS PHOTO", YEL, 540, 74, fg=BLK, angle=-4, delay=1.4, hold=1.6),
        st("s3", 5, "TWO TIES. ONE COLOR.", PINK, 540, 66, angle=4, delay=1.6, hold=1.6),
        st("sv", 0, "GLAM LEADS 1-0", YEL, 580, 70, fg=BLK, angle=-3, delay=0.3, hold=2.2)],
    "cover_title": ["BONUS", "GRANDMA REPLIED ALL"],
    "chat": {"name": "Ryan", "sub": "the ex · best man", "msgs": [["them", "chloe added me to the wedding chat"], ["them", "what color is ur dress"], ["them", "for my tie"], ["me", "ha"]]},
    "open_vote": {"title": "1 OR 2?", "hint": "1 = FULL GLAM   2 = DANCE W/ WALTER"},
    "beats": [{"scene": "sc", "line": 0, "image": "jess_b1128_ha.jpg"},
              {"scene": "s3", "line": 0, "image": "jess_b1128_beige.jpg"},
              {"scene": "s3", "line": 1, "image": "jess_b1128_delete.jpg"},
              {"scene": "s3", "line": 2, "image": "jess_b1128_added.jpg"},
              {"scene": "s3", "line": 3, "image": "jess_b1128_replyall.jpg"},
              {"scene": "s3", "line": 4, "image": "jess_b1128_walter.jpg"},
              {"scene": "sv", "line": 0, "image": "jess_b1128_walter.jpg"}],
    "cover_image": "jess_b1128_replyall.jpg"})
save("jess_bonus_1128", c)

# ---------------- Theo: 37 drafts (vote stays open: Tell Maya vs fix the brow)
c = load("theo_bonus_1127")
c.update({
    "image": "theo_b1128_drafts.jpg", "pill": "SEASON 1  •  SATURDAY MORNING",
    "hook": ["37 drafts", "to Maya.", "Sent: 0."], "hook_emoji": "📱",
    "notif": {"from": "Mom", "msg": "DID YOU TELL HER YET", "emoji": "", "color": [52, 199, 89]}, "notif_line": 3, "notif_y": 380,
    "script": {
        "s1": [[0.1, "Saturday. His ex Maya asked who the suit is for. He wrote thirty-seven drafts."],
               [0.1, "He sent zero."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "Maya: okay, so who is the suit for? You've been typing for twenty minutes."],
               [0.1, "He sent: dot dot dot."]],
        "s3": [[0.1, "Draft one: it's for you. Deleted. Too much."],
               [0.1, "Draft two: it's for a friend. Which friend? Deleted."],
               [0.1, "Draft three: a voice memo. His voice cracked on the word suit."],
               [0.1, "Then Mom yelled from downstairs: did you tell her yet?"],
               [0.1, "Maya: tell me what?"]],
        "sv": [[0.1, "Tell Maya who the suit is for, or fix the eyebrow for real? What should Theo do?"]]},
    "captions": {"scenes": ["s3"], "y": 1180, "keywords": ["draft", "one", "two", "three", "for", "you", "friend", "voice", "cracked", "suit", "mom", "tell", "what"]},
    "comments": [card("s1", 0, "ivannn_720", "Tell maya", 0, 1450, hold=2.2), card("sv", 0, "ivannn_720", "Tell maya", 0, 1650, hold=2.6, delay=0.3)],
    "stickers": [
        st("s1", 1, "SENT: 0", RED, 560, 110, angle=-5, delay=0.1, hold=1.4),
        st("sc", 1, "...", GREY, 1000, 120, fg=[20, 20, 20], angle=4, delay=0.6, hold=1.4),
        st("s3", 1, "WHICH FRIEND??", YEL, 560, 80, fg=BLK, angle=4, delay=1.0, hold=1.3),
        st("s3", 2, "-2,000 AURA", RED, 560, 90, angle=-4, delay=1.4, hold=1.4),
        st("s3", 0, "BROW: STILL SHARPIE", DARK, 560, 62, fg=YEL, angle=3, delay=1.4, hold=1.4),
        st("sv", 0, "TELL MAYA LEADS 1-0", YEL, 585, 62, fg=BLK, angle=-3, delay=0.4, hold=2.0),
        st("sv", 0, "SEND TO YOUR 37-DRAFT FRIEND", YEL, 1290, 46, fg=BLK, angle=-3, delay=2.6, hold=3.0)],
    "cover_title": ["BONUS", "37 DRAFTS. 0 SENT"],
    "chat": {"name": "Maya", "sub": "", "msgs": [["them", "ok so who is the suit for"], ["them", "u've been typing for 20 min"], ["me", "..."]]},
    "open_vote": {"title": "WHAT NOW?", "hint": "TELL MAYA  or  FIX THE BROW"},
    "beats": [{"scene": "sc", "line": 0, "image": "theo_b1128_base.jpg"},
              {"scene": "s3", "line": 0, "image": "theo_b1128_you.jpg"},
              {"scene": "s3", "line": 1, "image": "theo_b1128_friend.jpg"},
              {"scene": "s3", "line": 2, "image": "theo_b1128_memo.jpg"},
              {"scene": "s3", "line": 3, "image": "theo_b1128_mom.jpg"},
              {"scene": "s3", "line": 4, "image": "theo_b1128_what.jpg"},
              {"scene": "sv", "line": 0, "image": "theo_b1128_drafts.jpg"}],
    "cover_image": "theo_b1128_drafts.jpg"})
save("theo_bonus_1128", c)

# ---------------- Danny: push-up practice (vote stays open: real date vs side hustle)
c = load("danny_bonus_1127")
c.update({
    "image": "danny_b1128_hook.jpg", "pill": "DAY 6 / 30  •  BONUS",
    "hook": ["100 push-ups", "by tomorrow.", "He did 11."], "hook_emoji": "💪",
    "notif": {"from": "Mom", "msg": "why is the CEO on the floor", "emoji": "", "color": [52, 199, 89]}, "notif_line": 4, "notif_y": 380,
    "script": {
        "s1": [[0.1, "Tomorrow he owes his bully a hundred push-ups. If he loses, he pays the reunion bar tab twice."],
               [0.1, "Today he did eleven."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "Brock sent a video. His warm-up set. A hundred."],
               [0.1, "See you Sunday, CEO."]],
        "s3": [[0.1, "A commenter said he could do eighty-nine. New goal: eighty-nine."],
               [0.1, "Set one: eleven. His arms filed a complaint."],
               [0.1, "Set two: Tara FaceTimed on push-up three. He answered with his face."],
               [0.1, "Tara: are you doing push-ups at me?"],
               [0.1, "Total today: fourteen. The bar tab: still eleven hundred forty."]],
        "sv": [[0.1, "A real date with Tara, or a side hustle for the bar tab? What should Danny do?"]]},
    "captions": {"scenes": ["s3"], "y": 1200, "keywords": ["eighty-nine", "eleven", "arms", "complaint", "tara", "face", "push-ups", "fourteen", "tab"]},
    "comments": [card("s1", 0, "daniel_o0112", "Skip the date and continue to work on himself", 0, 1450, hold=2.6),
                 card("s3", 0, "h.nguy3n07", "he could do 89", 0, 1450, hold=2.2, delay=0.2),
                 card("sv", 0, "daniel_o0112", "Skip the date and continue to work on himself", 0, 1650, hold=2.6, delay=0.3)],
    "stickers": [
        st("s1", 1, "11 / 100", RED, 560, 110, angle=-4, delay=0.1, hold=1.4),
        st("sc", 1, "+0 AURA", GREY, 1000, 90, fg=[20, 20, 20], angle=4, delay=0.4, hold=1.3),
        st("s3", 1, "-4,000 AURA", RED, 560, 90, angle=5, delay=0.9, hold=1.3),
        st("s3", 2, "FACE ID: ACCEPTED", BLUE, 560, 68, angle=-4, delay=1.6, hold=1.4),
        st("s3", 3, "+300 AURA", GREEN, 560, 90, angle=-4, delay=0.8, hold=1.3),
        st("sv", 0, "SIDE HUSTLE LEADS 1-0", YEL, 585, 60, fg=BLK, angle=-3, delay=0.3, hold=2.0),
        st("sv", 0, "SEND TO YOUR 11 PUSH-UP FRIEND", YEL, 1290, 46, fg=BLK, angle=-3, delay=2.6, hold=3.0)],
    "cover_title": ["BONUS", "11 PUSH-UPS"],
    "chat": {"name": "Brock", "sub": "the bully", "msgs": [["them", "[video] warm-up set"], ["them", "100"], ["them", "see u sunday ceo"]]},
    "open_vote": {"title": "WHAT NOW?", "hint": "A REAL DATE  or  A SIDE HUSTLE"},
    "beats": [{"scene": "sc", "line": 0, "image": "danny_b1128_brock.jpg"},
              {"scene": "s3", "line": 0, "image": "danny_b1128_89.jpg"},
              {"scene": "s3", "line": 1, "image": "danny_b1128_floor.jpg"},
              {"scene": "s3", "line": 2, "image": "danny_b1128_tara.jpg"},
              {"scene": "s3", "line": 4, "image": "danny_b1128_total.jpg"},
              {"scene": "sv", "line": 0, "image": "danny_b1128_hook.jpg"}],
    "cover_image": "danny_b1128_floor.jpg"})
save("danny_bonus_1128", c)

# ---------------- Wes (Trash Horde story): the night before Brooke comes (vote stays open: let her help vs tell her no)
c = load("horde_story_bonus_1127")
c.update({
    "image": "wes_b1128_hook.jpg", "pill": "THE TRASH HORDE  •  BONUS",
    "hook": ["Brooke comes", "at 9 AM.", "Park: 4% clean."], "hook_emoji": "🍩",
    "notif": {"from": "Brooke", "msg": "omw!! bringing donuts", "emoji": "", "color": [236, 110, 160]}, "notif_line": 3, "notif_y": 380,
    "script": {
        "s1": [[0.1, "His ex Brooke is coming to help at nine A M. The park is four percent clean."],
               [0.1, "He had one night to fake it."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "Ranger Cole: Wes. She's bringing donuts."],
               [0.1, "Do not let her pick up anything."]],
        "s3": [[0.1, "Plan one: shove everything under the slide. The slide filled up."],
               [0.1, "Plan two: hide the bags behind a tree. The bags walked back."],
               [0.1, "Then the Butt Goblin moved in. Two thousand six hundred HP."],
               [0.1, "Eight fifty-nine. A car pulled in. Donuts on the dashboard."]],
        "sv": [[0.1, "Let Brooke help, or tell her no? What should Wes do?"],
               [0.1, "And real litter you pick up hits the Horde. Comment your haul and city."]]},
    "hud": {"tiles": [{"label": "DAYS LEFT", "value": "27", "color": YEL}, {"label": "PARK CLEAN", "value": "4%", "color": [120, 225, 120]},
                      {"label": "HORDE HP", "value": "2,600", "from": "2,500", "at": ["s3", 2], "color": RED}]},
    "captions": {"scenes": ["s3"], "y": 1200, "keywords": ["slide", "filled", "bags", "walked", "back", "butt", "goblin", "hp", "donuts", "dashboard"]},
    "comments": [],
    "stickers": [
        st("s1", 1, "ONE NIGHT", DARK, 560, 100, fg=YEL, angle=-4, delay=0.1, hold=1.4),
        st("sc", 1, "ALL CAPS COLE", GREY, 1000, 80, fg=[20, 20, 20], angle=4, delay=0.6, hold=1.3),
        st("s3", 1, "-2,000 AURA", RED, 560, 90, angle=4, delay=1.0, hold=1.3),
        st("s3", 2, "HORDE +100 (0 HITS YESTERDAY)", RED, 560, 50, angle=-3, delay=1.2, hold=1.6),
        st("s3", 3, "FOOD WRAPPERS = #1 BEACH TRASH (ICC)", YEL, 1420, 40, fg=BLK, angle=3, delay=0.6, hold=2.2),
        st("sv", 0, "VOTES SO FAR: 0", YEL, 585, 66, fg=BLK, angle=-3, delay=0.3, hold=2.0),
        st("sv", 1, "SEND TO YOUR MESSY FRIEND", YEL, 1290, 48, fg=BLK, angle=-3, delay=0.3, hold=3.0)],
    "cover_title": ["BONUS", "THE BAGS WALKED BACK"],
    "chat": {"name": "Ranger Cole", "sub": "his boss (her bf)", "msgs": [["them", "WES."], ["them", "SHE'S BRINGING DONUTS."], ["them", "DO NOT LET HER PICK UP ANYTHING"]]},
    "open_vote": {"title": "WHAT NOW?", "hint": "LET BROOKE HELP  or  TELL HER NO"},
    "beats": [{"scene": "sc", "line": 0, "image": "wes_b1128_cole.jpg"},
              {"scene": "s3", "line": 0, "image": "wes_b1128_slide.jpg"},
              {"scene": "s3", "line": 1, "image": "wes_b1128_bags.jpg"},
              {"scene": "s3", "line": 2, "image": "wes_b1128_goblin.jpg"},
              {"scene": "s3", "line": 3, "image": "wes_b1128_car.jpg"},
              {"scene": "sv", "line": 0, "image": "wes_b1128_car.jpg"}],
    "cover_image": "wes_b1128_bags.jpg"})
save("horde_story_bonus_1128", c)
