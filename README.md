# gen-code-from-requirements-doc

## Purpose of this repo
This repo is meant to help me get a feel for how challenging it is to generate a useful codebase using GPT-4. I'm less concerned here with actually generating functional code and more focused on figuring out to what degree this is possible.

## Design
Ideally I'd directly map from a requirements document to a functional codebase. Initial testing showed that was only going to work for very small projects (say, a single file or two containing a couple functions). Inspired by chain-of-thought prompting and how typical software development works, I tried introducing a middle step of a design document. Really the purpose of the design document is to:
1. Provides all the context that GPT-4 needs to generate one file at a time (due to context limitations).
1. Serve as an intermediate step between the requirements document and the codebase that is easier to debug and iterate on.

## Usage
I've only tested this on Ubuntu 20.04 with Python 3.10.4.

High-level workflow:
- Human writes a requirements document and places it in `requirements_documents/<human_project_name>`.
- Human adds a configuration to `src/config.py` for the project.
- GPT-4 writes a design document based on the requirements document and places it in `generated_projects/<project_name_from_config_file>`:
    ```
    python src/generate_design_document_from_requirements.py --project_name <project_name>
    ```
- Use GPT-4 to populate the content of the codebase: 
    ```
    python src/generate_code_from_design_document.py --project_name <project_name>
    ```
- Runs the tests then runs the code and uses GPT-4 fix errors (note this script calls `chmod +x` on the main bash script): 
    ```
    python src/run_code_with_self_healing.py --project_name <project_name>
    ```

Note:
- During file generation, multiple requests are sent (an initial generation and then "improve file" requests).
- When running the code, it will take some iterations of "self healing" before it will work correctly (but this happens automatically).

## Experiments

To see more detail on each experiment, check out their requirements documents in `requirements_documents/`. Everything in `generated_projects/` was generated by GPT-4 without any manual edits (granted, I did a good amount of iterating on the requirements docs and prompts but never directly edited any of the generated files).

### Local Discord Character Counter Bot
As a first silly test - a discord bot that runs locally counts characters of messages sent by "subscribers" to it. See the requirements docs for usage.

While it's super simple, it's amazing it actually works!

### GitHub Issues to PR Bot
As a second test - a bot which monitors a github repo for issues and automatically creates a PR linked to it and closes the issue when the PR is closed.

This code will actually be used in my next attempt at this (see the "Ideas for the next iteration" section).

***************************************** TODO FINISH THIS ONCE CODE WORKS !!!! *****************************************

## Existing problems
- Generally passing around what folder is where is very fragile and needs some love.
- File generation (sometimes) generates a `.venv` folder, it does not "understand" this will be generated automatically during setup.
- How it returns the contents of files and how that context is parsed a bit fragile.

## Takeaways
- Generally this seems super promising. Check out the generated design documents and code! Not bad. Definitely did better than I thought but we are _not_ quite there yet, at least going about it as this repo is structured.
- Specifying what I want in a requirements file and then using a design document as an intermediate step was great. It seems like for the forseeable future a middle step (or two!) between "me writing what I want" and "generate code" that GPT-4 generates seems extremely helpful (both for human-interpretable debugging and producing higher quality code). For example, the "Ensure that you have set `intents.message_content = True`" in the requirements document is just a bug that neither improve code or fix code finds so I just .. had to add it to the requirements but that doesn't seem like the right place for it.
- There's definitely some being mindful about what the LLM needs to generate functional code and explicitly stating that should appear in the design document (e.g., environment variables, logging).
- Having the LLM iteratively reflect on its response and improve the response seemed to be super helpful. So helpful that I just built it into how I send messages to GPT-4 (see `utils/llm.py`).
- Generating code from one-forward-pass is far too hard. Getting the requirements doc + prompts right definitely took a couple dozen iterations. I think this needs to be an iterative process (with a human in the loop). And "iterating" by editing requirements and/or prompts and re-running makes it too hard to capture the changes.
- Remember the LLM is trained on all the data from the internet: beginner, intermediate, advanced, trash, power users, puzzles, etc. So if you want it be an expert, tell it to be an expert! The same thing goes for package versions, it can sometimes use out-dated packages (even though it knows about newer versions) so tell it to use update-to-date packages.
- I like the mindset of viewing the LLM like it's a really book-smart intern. It has some unintuitive (to me) priors that skews interpretations of vague instructions. When you feel the odd prior happening, just be more specific. At some point "more specific" means "examples".
- Who it assigned the copyright to in the LICENSE file is pretty fantastic.
- It's unclear how much also generating/running tests helped (but could be a lot).

## Ideas for the next iteration
- Rather than this one-forward-pass-style, I think development may need to look a lot more like a standard software dev process (think: GitHub issues, branch the code, put in a PR, reviews, merge the PR). I think this style of iterating will be much easier for me to give GPT-4 the specificity of feedback needed to build a codebase containing, say, a dozen files. This may also help limit what needs to be in GPT-4's context and allow me to build bigger codebases without having to put full requirements and/or design documents in the context.
- Ideally in this new mode, I'd only have to write issues and review PRs. It's mostly the same mindset as interacting with a junior engineer.
- This also may help surface to what degree tests help (since we'd see their results and the bot trying to fix them in the PR).

## Related projects
These projects were extremely inspiring and I borrowed many ideas from them:
- [smol developer](https://github.com/smol-ai/developer)
- [Wolverine](https://github.com/biobootloader/wolverine)
- [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)
- [BabyAGI](https://github.com/yoheinakajima/babyagi)
