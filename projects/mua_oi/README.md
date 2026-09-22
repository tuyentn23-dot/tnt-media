# Project: Mua Oi Dung Roi Mai (rain music video)

Goal

Loop a rain-themed video with the full song as audio, publish to YouTube.

Source

Video: cham_mua_final_title.mp4 (from Desktop) - h264 1344x768, 15.12s, 30fps. Visual only (audio dropped).

Music: Mua oi dung roi mai (from Desktop) - actually WebM/Opus 48kHz stereo, 3:40 (220s). Full track used.

Build

ffmpeg: -stream_loop -1 on video + music audio, -map 0:v:0 -map 1:a:0, -shortest,
h264 crf20 + aac 192k. Output loops the 15s video to cover the whole 3:40 song.

Output: mua_oi_loop.mp4 (88.8 MB, 3:42, 1344x768, h264 + AAC 48kHz stereo)

Local copies: video_src.mp4, music_src.webm (media gitignored)

Publish

YouTube video id: hsUywXmt0N4

URL: https://www.youtube.com/watch?v=hsUywXmt0N4

Title: Mua Oi Dung Roi Mai - Nhac Chill Mua Buon Thu Gian Ngu Ngon

Category: Music, privacy public, published via ops/os_publish.publish(..., force=True)

Notes

Media files (*.mp4, *.webm) are gitignored; only this README is committed.
