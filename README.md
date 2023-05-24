# gen-code-from-requirements-doc

## Purpose of this repo
This repo is meant to help me get a feel for how challenging it is to generate a useful codebase using GPT-4. I'm less concerned here with actually generating functional code and more focused on figuring out to what degree this is possible.

## Design
Ideally this would directly map from a requirements document to a functional codebase. Initial testing showed that was only going to work for very small projects (say, a single file or two containing a couple functions). Inspired by chain-of-thought prompting and how typical software development works, I tried introducing a middle step of a design document. Really the purpose of the design document is to:
1. Provides all the context that GPT-4 needs to generates code.
1. Serve as an intermediate step between the requirements document and the codebase that is easier to debug and iterate on.

A secondary decision I made was to generate each file independently. This was mostly so I didn't have to worry (as much) about filling up GPT-4's context window. 

## Usage
I've only tested this on Ubuntu 20.04 with Python 3.10.4.

High-level workflow:
- Human writes a requirements document and places it in `generated_projects/<human_project_name>`.
- GPT-4 writes a design document based on the requirements document and places it in `generated_projects/<human_project_name>`:
    ```
    python src/generate_design_document_from_requirements.py --project_path generated_projects/<human_project_name>
    ```
- GPT-4 writes a script to populate the file structure and places it in `generated_projects/<human_project_name>`: 
    ```
    python src/generate_file_structure_from_design_document.py --project_path generated_projects/<human_project_name>
    ```
- Human runs the file structure creation script (this is easy to automate just .. makes me nervous at the moment):
    ```
    python /src/generated_projects/<human_project_name>/generate_file_structure.py
    ```
- Use GPT-4 to populate the content of the files: 
    ```
    python src/generate_code_from_file_structure.py --project_path generated_projects/<human_project_name>
    ```
- Use GPT-4 improve the code TODO REMOVE?: 
    ```
    python src/improve_code.py --project_path generated_projects/<human_project_name>
    ```
- Use GPT-4 fix errors that occur when the project is run (note this script calls `chmod +x` on the bash script): 
    ```
    python src/fix_code.py --project_path generated_projects/<human_project_name> --bash_script <set_up_and_run_bash_script>
    ```

## Experiments

### Local Discord Character Counter Bot
This is a first silly test - a discord bot that runs locally counts characters of messages sent by "subscribers" to it (see `sgenerated_projects/local_discord_bot/local_discord_bot/project_requirements_document.md` for the full requirements). Note the folders are named `generated_projects/<human_project_name>/<gpt4_project_name>`. Inside `generated_projects/local_discord_bot/`, `project_requirements_document.md` is the only file I manually created.

The code improvement and code fix steps definitely helped. Fix code was only helpful when it wouldn't run. Improve code was helpful to catch errors that only appeared during interaction.

It works though!

### GitHub Issues to PR Bot





## Existing problems
- Generally passing around what folder is where is very fragile and needs some love.
- File generation (sometimes) generates a `.venv` folder, it does not "understand" this will be generated automatically during setup.
- Some of what I think of "usage instructions" in the readme are listed under setup (e.g., running it).

## Takeaways
- Generally this seems super promising. Check out the generated design documents! Not bad. Definitely did better than I thought but we are _not_ there yet, at least going about it this way.
- Specifying what I want in a requirements file and then using a design document as an intermediate step was great. It seems like for the forseeable future a middle step (or two!) between "me writing what I want" and "generate code" that GPT-4 generates seems extremely helpful (both for human-interpretable debugging and producing higher quality code). For example, the "Ensure that you have set `intents.message_content = True`" in the requirements document is just a bug that neither improve code or fix code finds so I just .. had to add it to the requirements but that doesn't seem like the right place for it.
- There's definitely some being mindful about what the LLM needs to generate functional code and explicitly stating that should appear in the design document (e.g., environment variables, logging).
- Having the LLM iteratively reflect on its response and improve the response seemed to be super helpful.
- Generating in a one-forward-pass mode is far too hard. Getting the requirements doc + prompts right definitely took a couple dozen iterations. I think this needs to be an iterative (with a human in the loop) process. And "iterating" by editing prompts and re-running makes it too hard to capture the changes.
- Context size is going to make this impossible for anything but tiny projects (ideally, we'd have the requirements and design doc in context while writing code but that'll easily fill half the context of GPT-4 by itself).
- Remember the LLM is trained on all the data from the internet: beginner, intermediate, advanced, trash, power users, puzzles, etc. So if you want it be an expert, tell it to be an expert! The same thing goes for package versions, it can sometimes use out-dated packages (even though it knows about newer versions) so tell it to use update-to-date packages.
- I like the mindset of viewing the LLM like it's a really book-smart intern. It has some unintuitive (to me) priors that skews interpretations of vague instructions. When you feel the odd prior happening, just be more specific. At some point "more specific" means "examples".
- Who it assigned the copyright to in the LICENSE file is pretty fantastic.

## Ideas for the next iteration
- Rather than this one-forward-pass, I think development may need to look a lot more like a standard software dev process (think: GitHub issues, branch the code, put in a PR, reviews, merge the PR). I think this style of iterating will be much easier for me to give GPT-4 the specificity of feedback needed to build a codebase containing, say, a dozen files. This may also help limit what needs to be in GPT-4's context and allow me to build bigger codebases without having to put full requirements and/or design documents in the context.
- Ideally in this new mode, I'd only have to write issues and review PRs. It's mostly the same mindset of interacting with a junior engineer.
- Rather than hoping "improve code" catches all the interaction errors, have it also generate tests and "fix code" should fix errors from the tests. Maybe even have it generate tests before it generates the actual code files (i.e., just from the design doc)?

## Related projects
These projects were extremely inspiring and I borrowed many ideas from them:
- [smol developer](https://github.com/smol-ai/developer)
- [Wolverine](https://github.com/biobootloader/wolverine)
- [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)
- [BabyAGI](https://github.com/yoheinakajima/babyagi)
