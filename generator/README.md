# CV generator (public edition)

`build_cvs.py` builds the Word CVs from the published `cv_data.json`. It is run by the monthly
GitHub Action in `.github/workflows/monthly-cv.yml`. It holds no private data.

Local run: `CV_JSON=cv_data.json CV_PUBLIC=1 python3 generator/build_cvs.py out`
