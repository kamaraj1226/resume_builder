# Goal

- For the given reusme template and job description. Check the description and create a new resume (pdf) file matching to that JD

## Steps to run

1. Sync packag

```bash
uv sync
```

2. Build image

```bash
uv run poe img-build
```

3. Run image once

```bash
uv run pop img-run-once
```

## TODO fix required

- After tool approval there is unnecessary print statements if tool step info is turned off

## Reference

[latex-essentials](https://2.mirrors.in.sahilister.net/ctan/info/latex-essential/ess2e.pdf) - `pdf_to_latex_agent` use this pdf as reference to check the latex it created. Pdf credict goes to this document creator.
