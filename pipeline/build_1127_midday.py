"""Builds the Nov 27 midday episode configs from the proven Nov 26 midday configs (same engine keys)."""
import json, copy, os
E = os.path.join(os.path.dirname(os.path.abspath(__file__)), "episodes")
def load(n): return json.load(open(os.path.join(E, n + ".json")))
def save(n, c): json.dump(c, open(os.path.join(E, n + ".json"), "w"), indent=1, ensure_ascii=False); print(n)
YEL, RED, BLUE, DARK, GREEN = [255, 214, 102], [235, 80, 95], [90, 150, 240], [40, 40, 48], [120, 225, 120]
def st(scene, line, text, bg, y, size, angle=-3, hold=1.6, delay=0.3, fg=None, **kw):
    d = {"scene": scene, "line": line, "text": text, "bg": bg, "y": y, "angle": angle, "size": size, "hold": hold, "delay": delay}
    if fg: d["fg"] = fg
    d.update(kw); return d
BLK = [15, 15, 15]; WHT = [255, 255, 255]

# ---------------- Malik: Black Friday sneaker standoff (vote stays open: Jada Sunday vs Dez's film)
c = load("malik_bonus_1126")
c.update({
    "image": "malik_b1127_hook.jpg", "pill": "SEASON 1  •  BONUS",
    "hook": ["Black Friday.", "Last size 11s.", "Dez has the left."], "hook_emoji": "👟",
    "name_line": "Black Friday.", "sub_line": "Bonus  •  Day 11 drops tonight",
    "notif": {"from": "Dez", "msg": "my film's up. if u scared", "emoji": "", "color": [235, 80, 95]}, "notif_line": 3, "notif_y": 380,
    "script": {
        "s1": [[0.1, "Black Friday. One pair of size elevens left. His rival Dez grabbed the left shoe."],
               [0.1, "Malik got the right one. He still can't go left."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "Then his ex texted. Are you and Dez fighting over one shoe?"],
               [0.1, "I'm literally behind you."]],
        "s3": [[0.1, "Tug of war. Round one. The shoe stretched."],
               [0.1, "Round two. The lace snapped. Dez said: that's one."],
               [0.1, "The manager split the pair. One shoe each. Full price."],
               [0.1, "Then two texts. Jada: Sunday? Dez: my film is up, if you're scared."]],
        "sv": [[0.1, "Study with Jada on Sunday, or scout Dez's film? What should Malik do?"]]},
    "hud": {"tiles": [{"label": "DAY", "value": "10/30", "color": YEL}, {"label": "OVR", "value": "76", "color": [255, 150, 60]},
                      {"label": "HYPE", "value": "36/100", "color": [236, 110, 180]}]},
    "captions": {"scenes": ["s1", "s3"], "y": 1200, "keywords": ["black", "friday", "dez", "left", "right", "jada", "lace", "snapped", "one", "full", "price", "sunday", "film", "scared", "elevens"]},
    "comments": [],
    "stickers": [
        {"scene": "s1", "line": 0, "delay": 2.6, "kind": "calendar", "text": "7", "label": "TOURNEY IN", "x": 230, "y": 1480, "hold": 2.0},
        st("s1", 1, "STILL CAN'T GO LEFT", RED, 600, 72, angle=4, delay=0.4),
        st("sc", 1, "SHE'S RIGHT BEHIND HIM", YEL, 640, 60, fg=BLK, angle=-4, hold=1.8),
        st("s3", 0, "*STRRREEETCH*", BLUE, 600, 84, angle=-5, delay=0.2),
        st("s3", 1, "-800 AURA", RED, 600, 100, angle=5, delay=0.2),
        st("s3", 1, "THAT'S ONE...", DARK, 780, 64, fg=WHT, angle=-3, delay=1.4),
        st("s3", 2, "$0 SAVED", YEL, 640, 96, fg=BLK, angle=3, delay=0.6),
        st("sv", 0, "VOTES SO FAR: 0", DARK, 1110, 56, fg=WHT, angle=-2, hold=3.0, delay=0.2),
        st("sv", 0, "SEND THIS TO YOUR BLACK FRIDAY BUDDY", YEL, 1290, 46, fg=BLK, angle=-3, hold=3.0, delay=1.2)],
    "cover_title": ["BONUS", "ONE SHOE EACH"],
    "chat": {"name": "Jada", "sub": "his ex", "msgs": [["them", "are u and dez fighting over ONE shoe"], ["them", "i'm literally behind u"]]},
    "open_vote": {"title": "WHAT NOW?", "hint": "STUDY W/ JADA  or  DEZ'S FILM"},
    "beats": [{"scene": "sc", "line": 0, "image": "malik_b1127_phone.jpg"}, {"scene": "s3", "line": 0, "image": "malik_b1127_tug.jpg"},
              {"scene": "s3", "line": 1, "image": "malik_b1127_lace.jpg"}, {"scene": "s3", "line": 3, "image": "malik_b1127_two.jpg"},
              {"scene": "sv", "line": 0, "image": "malik_b1127_hook.jpg"}],
    "cover_image": "malik_b1127_hook.jpg", "motion": True})
save("malik_bonus_1127", c)

# ---------------- Rosie: the ketchup trap (vote stays open: IntelliStudy vs confront the dishwasher)
c = load("rosie_bonus_1126")
c.update({
    "image": "rosie_b1127_hook.jpg", "pill": "SEASON 1  •  BONUS",
    "hook": ["She set a trap.", "Secret: ketchup.", "Julian knew. 4 min."], "hook_emoji": "🍅",
    "name_line": "Black Friday.", "sub_line": "Bonus  •  Day 11 drops tonight",
    "notif": {"from": "Julian", "msg": "2 hours max. then the fridge.", "emoji": "", "color": [90, 150, 240]}, "notif_line": 1, "notif_y": 380,
    "script": {
        "s1": [[0.1, "She set a trap. Her fake secret ingredient: ketchup. Said it loud. Next to the dish pit."],
               [0.1, "Four minutes later, her phone buzzed."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "Julian. Ketchup? In a cook-off? Rosie. No."]],
        "s3": [[0.1, "Trap two. She told the dish pit the leftover turkey stays out all day."],
               [0.1, "Julian: two hours, max. Then the fridge. He's right. That's the rule."],
               [0.1, "Chef Marco read it over her shoulder. How does Julian know about my turkey?"],
               [0.1, "In the dish pit, a phone lit up. Rosie took off her apron."]],
        "sv": [[0.1, "Study food science on IntelliStudy, or confront the dishwasher? What should Rosie do?"]]},
    "hud": {"tiles": [{"label": "DAYS LEFT", "value": "20", "color": YEL}, {"label": "SKILL", "value": "78%", "color": GREEN},
                      {"label": "BUZZ", "value": "35/100", "color": [236, 110, 180]}]},
    "captions": {"scenes": ["s1", "s3"], "y": 1200, "keywords": ["ketchup", "trap", "julian", "dish", "pit", "four", "two", "hours", "fridge", "turkey", "marco", "apron"]},
    "comments": [],
    "stickers": [
        {"scene": "s1", "line": 0, "delay": 3.0, "kind": "calendar", "text": "20", "label": "COOK-OFF IN", "x": 230, "y": 1480, "hold": 2.0},
        st("s1", 1, "*BZZT*", RED, 600, 110, angle=-5, delay=0.3),
        st("sc", 0, "SHE NEVER TOLD HIM", YEL, 640, 64, fg=BLK, angle=-4, hold=1.8, delay=1.0),
        st("s3", 0, "TRAP #2", DARK, 600, 90, fg=WHT, angle=4, delay=0.2),
        st("s3", 1, "THE TRICK: FRIDGE WITHIN 2 HOURS", YEL, 760, 54, fg=BLK, angle=-3, hold=2.2, delay=0.8),
        st("s3", 2, "HOW DOES JULIAN KNOW? (x3)", BLUE, 600, 62, angle=4, delay=1.6),
        st("s3", 3, "-1,000 AURA (FOR THE DISHWASHER)", RED, 780, 50, angle=-3, delay=0.8),
        st("sv", 0, "VOTES SO FAR: 0", DARK, 1110, 56, fg=WHT, angle=-2, hold=3.0, delay=0.2),
        st("sv", 0, "SEND THIS TO THE FRIEND WHO CAN'T KEEP A SECRET", YEL, 1290, 40, fg=BLK, angle=-3, hold=3.0, delay=1.2)],
    "cover_title": ["BONUS", "THE KETCHUP TRAP"],
    "chat": {"name": "Julian", "sub": "her ex", "msgs": [["them", "ketchup??"], ["them", "in a cook-off??"], ["them", "rosie. no."]]},
    "open_vote": {"title": "WHAT SHOULD SHE DO?", "hint": "INTELLISTUDY  or  CONFRONT HIM"},
    "beats": [{"scene": "sc", "line": 0, "image": "rosie_b1127_phone.jpg"}, {"scene": "s3", "line": 0, "image": "rosie_b1127_turkey.jpg"},
              {"scene": "s3", "line": 2, "image": "rosie_b1127_marco.jpg"}, {"scene": "s3", "line": 3, "image": "rosie_b1127_apron.jpg"},
              {"scene": "sv", "line": 0, "image": "rosie_b1127_hook.jpg"}],
    "cover_image": "rosie_b1127_hook.jpg", "motion": True})
save("rosie_bonus_1127", c)

# ---------------- Wes midday short beat (<= 20 s): rehearsing "no" to a trash can (vote stays open)
c = load("horde_story_bonus_1127")
c.update({
    "image": "wes_b1127m_rehearse.jpg", "pill": "THE TRASH HORDE  •  BONUS",
    "hook": ["He practiced", "saying no.", "The trash can: no."], "hook_emoji": "🗑️",
    "script": {
        "s1": [[0.1, "Wes practiced telling his ex no. To a trash can."],
               [0.1, "The trash can said: let her come."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "Ranger Cole: Who are you talking to? Is that the trash can?"]],
        "s3": [[0.1, "Then Brooke texted. Bringing snacks for the crew."],
               [0.1, "The crew is him. And a trash can."]],
        "sv": [[0.1, "Let Brooke help, or tell her no? What should Wes do?"]]},
    "hud": {"tiles": [{"label": "DAYS LEFT", "value": "27", "color": YEL}, {"label": "PARK CLEAN", "value": "4%", "color": GREEN},
                      {"label": "HORDE HP", "value": "2,500", "color": RED}]},
    "captions": {"scenes": ["s1", "s3"], "y": 1200, "keywords": ["brooke", "no", "trash", "can", "cole", "snacks", "crew", "him"]},
    "chat": {"name": "Ranger Cole", "sub": "his boss (her bf)", "msgs": [["them", "WHO ARE YOU TALKING TO."], ["them", "IS THAT THE TRASH CAN."]]},
    "open_vote": {"title": "WHAT NOW?", "hint": "LET BROOKE HELP  or  TELL HER NO"},
    "stickers": [
        st("s1", 1, "HORDE: 1  WES: 0", RED, 600, 84, angle=4, delay=0.4),
        st("sc", 0, "ALL CAPS AGAIN", YEL, 640, 64, fg=BLK, angle=-4, hold=1.6, delay=1.2),
        st("s3", 1, "-3,000 AURA", RED, 600, 96, angle=-4, delay=0.3),
        st("s3", 1, "US ROADSIDE LITTER: DOWN 54% SINCE 2009 (KAB 2020)", YEL, 1420, 34, fg=BLK, angle=3, hold=2.2, delay=0.6),
        st("sv", 0, "VOTES SO FAR: 0", YEL, 585, 66, fg=BLK, angle=-3, hold=2.0),
        st("sv", 0, "SEND TO THE FRIEND WHO REHEARSES TEXTS OUT LOUD", YEL, 1250, 34, fg=BLK, angle=-3, hold=2.6, delay=0.6)],
    "cover_title": ["BONUS", "THE TRASH CAN SAID YES"],
    "beats": [{"scene": "s1", "line": 1, "image": "wes_b1127m_can.jpg"}, {"scene": "sc", "line": 0, "image": "wes_b1127m_phone.jpg"},
              {"scene": "s3", "line": 0, "image": "wes_b1127m_brooke.jpg"}, {"scene": "sv", "line": 0, "image": "wes_b1127m_rehearse.jpg"}],
    "cover_image": "wes_b1127m_can.jpg", "comments": [],
    "notif": {"from": "Brooke", "msg": "bringing snacks for the crew :)", "emoji": "", "color": [236, 110, 160]}, "notif_line": 0, "notif_y": 380})
c["script"]["sv"] = [[0.1, "Let Brooke help, or tell her no? What should Wes do? And real litter you pick up hits the Horde."]]
save("horde_story_midday_1127", c)

# ---------------- History #7 (Gus): who named Black Friday
c = load("history_e06")
c.update({
    "image": "gus_e07_point_police.jpg", "pill": "THAT REALLY HAPPENED  •  STORY #7",
    "hook": ["Black Friday", "was named by", "angry cops."], "hook_emoji": "🚓",
    "script": {
        "s1": [[0.1, "Black Friday wasn't named by stores. It was named by angry cops."],
               [0.1, "Philadelphia. The day after Thanksgiving. Shoppers flooded downtown."]],
        "s2": [[0.1, "x"]], "s4": [[0.1, "x"]], "s5": [[0.1, "x"]],
        "sc": [[0.1, "The director texted. Gus. Stop talking to the exhibits."]],
        "s3": [[0.1, "Then the tourists came for Saturday's Army Navy football game."],
               [0.1, "Traffic jams. Shoplifters. And no police officer could take the day off. They called it Black Friday."],
               [0.1, "By 1961, stores tried to rename it Big Friday. Nobody said Big Friday."],
               [0.1, "Decades later, stores told the in the black profit story. Historians say that's not where it started."]],
        "sv": [[0.1, "That really happened. Which true story should I tell tomorrow night?"]]},
    "hud": {"tiles": [{"label": "YEAR", "value": "1961", "color": YEL}, {"label": "DAYS OFF", "value": "0", "color": RED}]},
    "captions": {"scenes": ["s1", "s3"], "y": 1200, "keywords": ["black", "friday", "cops", "police", "philadelphia", "army", "navy", "football", "shoplifters", "1961", "big", "profit", "historians", "thanksgiving"]},
    "comments": [],
    "stickers": [
        st("s1", 1, "PHILADELPHIA, 1950s-60s", DARK, 560, 70, fg=WHT, angle=-3, delay=0.4),
        st("s3", 0, "ARMY vs NAVY, SATURDAY", BLUE, 560, 70, angle=4, delay=0.4),
        st("s3", 1, "DAYS OFF: 0", RED, 560, 96, angle=-4, delay=1.4),
        st("s3", 2, "REBRAND: FAILED", RED, 760, 84, angle=3, delay=1.4),
        st("s3", 3, "'IN THE BLACK' = A LATER STORY", YEL, 760, 56, fg=BLK, angle=-3, hold=2.0, delay=0.6),
        st("sv", 0, "SEND THIS TO YOUR BLACK FRIDAY SHOPPER", YEL, 1250, 46, fg=BLK, angle=-3, hold=3.0, delay=1.0)],
    "cover_title": ["1961", "NAMED BY ANGRY COPS"],
    "chat": {"name": "Museum Director", "sub": "boss", "msgs": [["them", "GUS."], ["them", "STOP TALKING TO THE EXHIBITS."], ["me", "it's black friday"], ["them", "IT'S 2 AM. GO HOME."]]},
    "open_vote": {"title": "NEXT TRUE STORY?", "hint": "NAME A STORY YOU WANT"},
    "beats": [{"scene": "s1", "line": 1, "image": "gus_e07_ex_street.jpg"}, {"scene": "sc", "line": 0, "image": "gus_e07_phone.jpg"},
              {"scene": "s3", "line": 0, "image": "gus_e07_ex_football.jpg"}, {"scene": "s3", "line": 1, "image": "gus_e07_ex_police.jpg"},
              {"scene": "s3", "line": 2, "image": "gus_e07_bigfriday.jpg"}, {"scene": "s3", "line": 3, "image": "gus_e07_shock_police.jpg"},
              {"scene": "sv", "line": 0, "image": "gus_e07_point_police.jpg"}],
    "cover_image": "gus_e07_point_police.jpg", "motion": True,
    "notif": {"from": "Museum Director", "msg": "GUS. IT'S BLACK FRIDAY. GO SHOPPING.", "emoji": "", "color": [236, 110, 180]}, "notif_line": 3, "notif_y": 380})
save("history_e07", c)
