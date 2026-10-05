# -- coding: utf-8 --"""Multichannel runner - goi autopublish_runner.

Workflow GitHub goi file nay. Tham so: so bai (mac dinh 4).
"""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def main():
 per = 4
 if len(sys.argv) > 1:
 try:
 per = int(sys.argv[1])
 except Exception:
 per = 4
 results = []
 for i in range(per):
 try:
 from ops import autopublish_runner
 rc = autopublish_runner.main()
 results.append({'run': i+1, 'rc': rc})
 except Exception as e:
 results.append({'run': i+1, 'error': str(e)})
 break
 print('multichannel done:', results)
 return 0


if __name__ == '__main__':
 sys.exit(main())
