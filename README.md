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

## Sample Qeury

1. Enure you have job description copied and saveed in a local directory
2. Provide the below input

```
Read the following files
job_description = '/mnt/d/resume_building/resume_builder/files/job_description.txt'
sample_latex_resume_format = '/mnt/d/resume_building/resume_builder/files/sample_latex.tex'
resume_pdf = '/mnt/d/resume_building/resume_builder/files/sample_resume.pdf'

You must use read_local_file to read job_description and sample_latex_resume_format file
You must use read_local_pdf_file tool to read resume_pdf
After reading all the files can you provide me tailored resume in latex format using 'customize_latax_with_jd' tool
```

## TODO fix required

- After tool approval there is unnecessary print statements if tool step info is turned off

## Reference

[latex-essentials](https://2.mirrors.in.sahilister.net/ctan/info/latex-essential/ess2e.pdf) - `pdf_to_latex_agent` use this pdf as reference to check the latex it created. Pdf credict goes to this document creator.
