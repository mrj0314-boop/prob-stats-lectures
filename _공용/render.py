"""주차 폴더의 manim 장면을 렌더링해 <주차>/애니메이션/에 GIF로 저장.

manim 기본 GIF는 색 수가 부족해 글자 테두리가 얼룩지므로
MP4로 렌더링한 뒤 프레임마다 팔레트를 따로 잡아 GIF로 변환.

사용법: python _공용/render.py 02주차_원순열과중복순열              (그 주차 전체 장면)
        python _공용/render.py 02주차_원순열과중복순열 PolygonTable  (일부 장면)
"""
import os
import subprocess
import sys
from pathlib import Path

import av
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FPS = 15


def mp4_to_gif(src, dst):
    with av.open(str(src)) as c:
        frames = [f.to_image().quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
                  for f in c.decode(video=0)]
    frames[0].save(dst, save_all=True, append_images=frames[1:], duration=1000 // FPS, loop=0, optimize=True)
    # 애니메이션 첫 장면은 빈 화면이므로 PDF 배포본·썸네일용 마지막 장면 PNG도 저장
    frames[-1].convert("RGB").save(dst.with_name(dst.stem + "_final.png"))


week = ROOT / sys.argv[1]
names = sys.argv[2:]
scenes = week / "_제작" / "scenes.py"
media = HERE / "_캐시" / week.name
out = week / "애니메이션"
out.mkdir(exist_ok=True)

env = {**os.environ, "PYTHONPATH": str(HERE), "PYTHONDONTWRITEBYTECODE": "1"}  # scenes.py의 `from common import *`용
subprocess.run([sys.executable, "-m", "manim", "-v", "WARNING", "--progress_bar", "none",
                "--media_dir", str(media), str(scenes), *(names or ["-a"])], check=True, env=env)
for mp4 in media.glob("videos/scenes/*/*.mp4"):
    if not names or mp4.stem in names:
        mp4_to_gif(mp4, out / f"{mp4.stem}.gif")
        print("->", out / f"{mp4.stem}.gif")
