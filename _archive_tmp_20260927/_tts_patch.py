import ast
U = chr(95)
NL = chr(10)
T = chr(9)
old_lines = [
'def tts(text, out):',
T + '# P1: edge-tts natural voice (fallback gTTS)',
T + 'try:',
T + T + 'from ops import voice' + U + 'synth',
T + T + 'voice' + U + 'synth.synth(text, out, voice="female' + U + 'north