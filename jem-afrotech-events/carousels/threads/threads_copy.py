import json
U = 'https://www.jem.social/afrotech-2026-events?utm_source=threads&utm_medium=social&utm_campaign=afrotech26&utm_content='
posts = {
 'creators': ("""afrotech is next week and there are 101 events on the calendar 😮‍💨

we went through every single one so you don't have to 🫡

swipe for the 6 rooms creators should be in 👀📸

come find us too 🫶
🌿 the green room · sun
💻 sapphic hour · thu

all 101 are linked in the replies 👇

which one are you pulling up to? tag your plus one 🎟️

#afrotech""",
 f"""here's all 101 afrotech events in one place, sorted by type 🔥

{U}creators

pop your email in to unlock the full list and we'll send a copy to your inbox too 📩"""),
 'brands': ("""brands 👀 heading to afrotech? consider this your field trip 🚌

swipe for the 6 activations worth seeing irl
(aka the ones your cmo is gonna ask about 😭)

wanna meet creators? 🌿
pull up to the green room on sunday. we're a sponsor, come say hi 🫶

all 101 events are linked in the replies 👇

📲 send this to your marketing team chat rn

#afrotech""",
 f"""every afrotech event in one place, sorted by type 🔥

{U}brands

unlock it with your email and we'll send a copy to your inbox 📩

and if you need creators for an activation, that's literally what jem social does 😉"""),
 'founders': ("""founders, it's officially afrotech week 🚀

your calendar is about to be chaos. we went through all 101 events so you don't have to 🫡

swipe for the 6 worth blocking off time for ➡️

come find us thursday at sapphic hour 💻💖

the full list of 101 is linked in the replies 👇

📲 send this to the founder in your group chat who's "just networking" this week 😭

#afrotech""",
 f"""the full afrotech list, all 101 events sorted by type 🔥

{U}founders

drop your email to unlock it and we'll send a copy to your inbox 📩 go get it this week 🚀"""),
}
out = {}
for k, (cap, rep) in posts.items():
    print(k, 'caption', len(cap), 'reply', len(rep), 'tags', cap.count('#'))
    assert len(cap) <= 500 and len(rep) <= 500 and cap == cap.lower()
    out[k] = {'caption': cap, 'reply': rep}
json.dump(out, open('threads_copy.json', 'w'), ensure_ascii=False, indent=1)
