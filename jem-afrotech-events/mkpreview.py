import sys
d = sys.argv[1]
p = lambda k: open(f'{d}/out/{k}.html').read()
wfcss = """body{margin:0;font-family:Arial,sans-serif;font-size:14px;line-height:20px;color:#333}
.w-form{margin:0 0 15px}.w-form-done{display:none;padding:20px;text-align:center;background:#ddd}.w-form-fail{display:none;margin-top:10px;padding:10px;background:#ffdede}
.w-input{display:block;width:100%;height:38px;padding:8px 12px;margin-bottom:10px;font-size:14px;color:#333;background:#fff;border:1px solid #ccc}
.w-button{display:inline-block;padding:9px 15px;background:#3898EC;color:#fff;border:0;border-radius:0}"""
form = f"""<div class="w-form"><form id="email-form" name="email-form" data-name="AfroTech 2026 List" method="get" onsubmit="event.preventDefault();this.style.display='none';var d=this.parentNode.querySelector('.w-form-done');d.style.display='block'">
<label class="at-lbl" for="Email">Email</label><input class="w-input" maxlength="256" name="Email" data-name="Email" placeholder="you@email.com" type="email" id="Email" required>
<div class="w-embed">{p('F_fields')}</div>
<input type="submit" data-wait="Unlocking..." class="w-button" value="Unlock the full list →"></form>
<div class="w-form-done" tabindex="-1" role="region"><div>You're in! The full list is unlocked below.</div></div>
<div class="w-form-fail" tabindex="-1" role="region"><div>Something went wrong. Try again, or email support@jem.social.</div></div></div>"""
body = f"""<div class="w-embed">{p('A_head')}</div>
<section data-afro="hero"><div data-afro="wrap"><div data-afro="grid">
<div class="w-embed">{p('H_copy')}</div>
<div data-afro="card" id="unlock"><div class="w-embed">{p('G_cardhead')}</div>{form}<div class="w-embed">{p('F_fine')}</div></div>
</div></div></section>
<div class="w-embed">{p('P_preview')}</div>
<div data-afro="lock">""" + ''.join(f'<div class="w-embed">{p(f"L{i}")}</div>' for i in range(1,5)) + f"""<div class="w-embed">{p('O_overlay')}</div></div>
<div class="w-embed">{p('C_tail')}</div>"""
open(f'{d}/preview.html','w').write(f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AfroTech 2026 Events</title><style>{wfcss}</style></head><body>{body}</body></html>")
