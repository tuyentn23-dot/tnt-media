import os, sys, math, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from PIL import Image, ImageEnhance
from ops import voice_synth as VS
from ops import voice_master as VM
from ops.gacha_viral_pack import VIDEOS
FFMPEG = os.path.abspath(os.path.join("tools", "ffmpeg.exe"))
BW, BH = 720, 1280
FONT = "tools/font_black.ttf"

def fit(im, w, h):
 iw, ih = im.size
 s = max(w / iw, h / ih)
 nw, nh = int(iw * s), int(ih * s)
 im2 = im.resize((nw, nh), Image.LANCZOS)
 x0 = (nw - w) // 2
 y0 = (nh - h) // 2
 return im2.crop((x0, y0, x0 + w, y0 + h))

def build(vid):
 cfg = VIDEOS[vid]
 parts = cfg["parts"]
 music_file = cfg["music"]
 pack_dir = "output/gacha_pack_" + vid
 out = os.path.abspath("output/Mialinhcute_gacha_" + vid + ".mp4")
 print("=== building", vid)
 vo = os.path.abspath("output/gacha_vo_" + vid + ".mp3")
 VS.synth_parts(parts, vo, voice="female_north", preset="cute", gap=0.3)
 VO_DUR = VM.duration(vo)
 print("voice dur:", VO_DUR)
 DUR = min(VO_DUR + 0.5, 19.5)
 print("total dur:", DUR)
 total_chars = sum(len(p) for p in parts)
 segs = []
 acc = 0.0
 for p in parts:
  d = VO_DUR * (len(p) / total_chars)
  segs.append((acc, acc + d))
  acc += d
 imgs = [pack_dir + "/pose" + str(i) + ".jpg" for i in range(6)]
 missing = [p for p in imgs if not os.path.exists(p)]
 if missing:
  print("MISSING:", missing)
  return None
 fps = 8
 n = int((DUR + 0.5) * fps)
 n_img = len(imgs)
 seg = DUR / n_img
 covers = [fit(Image.open(p).convert("RGB"), BW, BH) for p in imgs]
 tmp = "output/viral" + vid + "_frames"
 os.makedirs(tmp, exist_ok=True)
 for i in range(n):
  t = i / fps
  idx = min(n_img - 1, int(t / seg))
  local_t = (t % seg) / seg
  zoom = 1.0 + 0.15 * local_t
  base = covers[idx]
  nw, nh = int(BW * zoom), int(BH * zoom)
  im2 = base.resize((nw, nh), Image.LANCZOS)
  px = int(20 * math.sin(t * 2.0))
  py = int(15 * math.cos(t * 1.7))
  x0 = max(0, min(nw - BW, (nw - BW) // 2 + px))
  y0 = max(0, min(nh - BH, (nh - BH) // 2 + py))
  crop = im2.crop((x0, y0, x0 + BW, y0 + BH))
  if local_t > 0.88 and idx < n_img - 1:
   a = (local_t - 0.88) / 0.12
   crop = Image.blend(crop, covers[idx + 1], a)
  if t < 0.2:
   crop = ImageEnhance.Brightness(crop).enhance(0.35)
  elif t < 0.5:
   crop = ImageEnhance.Brightness(crop).enhance(1.5)
  if t > DUR - 0.5:
   k = (DUR - t) / 0.5
   crop = Image.blend(covers[0], crop, k)
  crop.save(os.path.join(tmp, "f%04d.png" % i))
 cap_tmp = "output/viral" + vid + "_caps"
 os.makedirs(cap_tmp, exist_ok=True)
 dts = []
 for k, (a, b) in enumerate(segs):
  fp = cap_tmp + "/" + ("c%d.txt" % k)
  words = parts[k].split()
  lines = []
  cur = ""
  for w in words:
   if len(cur) + len(w) + 1 > 20:
    lines.append(cur)
    cur = w
   else:
    cur = (cur + " " + w).strip()
  if cur:
   lines.append(cur)
  open(fp, "w", encoding="utf-8").write(chr(10).join(lines))
  en = "between(t," + str(round(a, 2)) + "," + str(round(b + 0.1, 2)) + ")"
  qt = chr(39)
  s = "drawtext=fontfile=" + FONT + ":textfile=" + fp + ":enable=" + qt + en + qt
  s += ":fontsize=56:fontcolor=0xFFFFFF:borderw=6:bordercolor=0xFF1493:shadowx=4:shadowy=4:shadowcolor=0x000000@0.9:line_spacing=12"
  s += ":x=(w-text_w)/2:y=h-380"
  dts.append(s)
 vf = ",".join(dts)
 pat = os.path.join(tmp, "f%04d.png")
 silent = "output/viral" + vid + "_silent.mp4"
 cmd1 = [FFMPEG, "-y", "-framerate", str(fps), "-i", pat, "-vf", vf, "-t", str(DUR), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "21", silent]
 r1 = subprocess.run(cmd1, capture_output=True, text=True)
 print("cap rc:", r1.returncode)
 if r1.returncode != 0:
  print(r1.stderr[-400:])
  return None
 music = os.path.abspath("assets/music_clips/" + music_file)
 cmd2 = [FFMPEG, "-y", "-i", silent, "-i", vo, "-i", music, "-filter_complex", "[1:a]volume=1.6[a1];[2:a]volume=0.2[a2];[a1][a2]amix=inputs=2:duration=first[aout]", "-map", "0:v", "-map", "[aout]", "-t", str(DUR), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out]
 r2 = subprocess.run(cmd2, capture_output=True, text=True)
 print("mux rc:", r2.returncode)
 if r2.returncode != 0:
  print(r2.stderr[-400:])
  return None
 print("final:", os.path.getsize(out))
 return out

if __name__ == "__main__":
 vid = sys.argv[1] if len(sys.argv) > 1 else "bully"
 result = build(vid)
 print("RESULT:", result)