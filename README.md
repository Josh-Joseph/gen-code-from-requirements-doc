# gen-code-from-requirements-doc

## Purpose of this repo
This repo is meant to get a feel for how challenging it is to generate a useful codebase using GPT-4. I'm less concerned here with actually generating functional code and figuring out to what degree this is possible.

## Design
Ideally this would directly map from a requirements document to a functional codebase. Initial testing showed that was only going to work for very small projects (say, a single file or two containing a couple functions). Inspired by chain-of-thought prompting and how typical software development works, I tried introducing a middle step of a design document.

## Usage
I've only tested this on Ubuntu 20.04 with Python 3.10.4.

High-level workflow:
- Human writes a requirements document and places it in `generated_projects/<project_name>`.
- GPT-4 writes a design document based on the requirements document and places it in `generated_projects/<project_name>`: `python src/generate_design_document_from_requirements.py`
- GPT-4 writes a script to populate the file structure and places it in `generated_projects/<project_name>`: `python src/generate_file_structure_from_design_document.py`
- Human runs the file structure creation script (this is easy to automate just .. makes me nervous at the moment): `python /src/generated_projects/<project_name>/generate_file_structure.py`
- Use GPT-4 to populate the content of the files: `python src/generated_projects/<project_name>/generate_code_from_file_structure.py`

## Experiments

### Discord Character Counter
So far, I've only tested this to create a silly discord bot that counts characters of messages sent by "subscribers" to it and is deployed to GCE (see `src/generated_projects/discord_bot/project_requirements_document.md` for the full requirements). I haven't even tried to run the code yet to see if it actually runs. I imagine it won't since `discord.py` has had some significant changes since GPT-4's knowledge cut-off. I'm going to wait to go farther down actually running the code until I get web-browsing hooked up.

Inside `src/generated_projects/discord_bot/`, `project_requirements_document.md` is the only thing I manually created.

## Existing problems
- Generally passing around what folder is where is very fragile and needs rethinking. For example, I've hardcoded in the directory in `generate_code_from_file_structure.py`.
- File generation generates a `.venv` folder, it does not "understand" this will be generated automatically during setup.
- Some of what I think of "usage instructions" in the readme are listed under setup (e.g., running it).

## Takeaways
- Generally this seems super promising. Definitely did better than I thought but we are _not_ there yet, at least going about it this way.
- Specifying what I want in a requirements file and then using a design document as an intermediate step was great. It seems like for the forseeable future a middle step (or two!) between "me writing what I want" and "generate code" that GPT-4 generates seems extremely helpful (both for human-interpretable debugging and producing higher quality code).
- Generating in a one-forward-pass mode is far too hard. It needs to be an iterative (with a human in the loop) process. And "iterating" by editing prompts and re-running makes it too hard to capture the changes.
- Context size is going to make this impossible for anything but tiny projects (ideally, we'd have the requirements and design doc in context while writing code but that'll easily fill half the context of GPT-4 by itself).
- Who it assigned the copyright to in the LICENSE file is pretty fantastic.

# Ideas for the next iteration
- Rather than this one-forward-pass, I think development may need to look a lot more like a standard software dev process (think: GitHub issues, branch the code, put in a PR, reviews, merge the PR). I think this style of iterating will be much easier for me to give GPT-4 the specificity of feedback needed to build a codebase containing, say, a dozen files. This may also help limit what needs to be in GPT-4's context and allow me to build bigger codebases without having to put full requirements and/or design documents in the context.
- Ideally in this new mode, I'd only have to write issues and review PRs. It's mostly the same mindset of interacting with a junior engineer.

# Related projects
These projects were extremely inspiring and I borrowed many ideas from them:
- [smol developer](https://github.com/smol-ai/developer)
- [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)
- [BabyAGI](https://github.com/yoheinakajima/babyagi)