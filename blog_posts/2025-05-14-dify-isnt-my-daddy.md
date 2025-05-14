---
date: '2025-05-14'
layout: post
title: Dify isn't my daddy, Python is <3 <3
---

Lately, I've been kicking around the idea of building a small tool to help me with my blogging workflow. My writing style tends to be a bit stream-of-consciousness – lots of notes, fragmented thoughts, quick jots that make perfect sense to me in the moment but might be a bit incoherent for an external reader. I wanted a tool that could take these raw notes, clean them up, fill in context gaps, and structure them into a more cohesive post, all while preserving my original tone and style. The goal wasn't to generate new content, but to polish what's already there.

As part of exploring how to build this, I had a couple of goals:
1.  Learn the basics of Dify, an open-source LLM application development platform.
2.  Attempt to build my "smol blogger" tool using Dify.
3.  Compare the experience of implementing this idea on a platform like Dify versus a more direct approach, likely just using Python.

### Diving into Dify

My first step was to get Dify up and running locally. I remembered to set up my Python virtual environment right away, which felt like a small win – good job, me!

I followed the official instructions for installing Dify using Docker Compose. Now, I'll be honest: my understanding of Docker is *very* loose. I grasp the *why* – it's great for packaging applications and dependencies – but I don't really have a solid grasp on the commands, the networking, or what exactly is happening under the hood when I run a `docker-compose up`. But hey, I'm not a DevOps engineer, so I figured I could just follow the steps.

Initial impressions? Setting up Dify using Docker Compose was *so fucking nice*. Seriously, it feels great to use modern tools that people who care are actively maintaining. The setup process was a breeze, and the documentation (at least the installation part) wasn't just full of lies, which is a refreshing way to start the day in the world of open-source software.

### Ah, The Pain.

Of course, the second I finished typing that glowing review in my notes, I ran into a problem. The quickstart guide recommended running some upgrade steps right after the initial installation. Following those steps led to an error. Pain. Pure ego death and pain. It's like the universe heard my moment of satisfaction and decided I needed to be humbled immediately.

After a bit of fumbling, I decided the cleanest approach was to just delete and uninstall all the Dify stuff and start over. Reinstalled from scratch, followed the *basic* setup steps without attempting the immediate upgrade, and... we were up and running. Okay, maybe not *completely* clean, but it seemed functional.

### Not So Fast...

My next hurdle was connecting Dify to external LLM providers, specifically trying to use the free models available via OpenRouter. And... no dice. There were only a very limited number of models showing up from OpenRouter, not the variety I expected or needed for experimentation.

Turns out, I had installed an older version of Dify. Of course. Those god damn docs were potentially screwing with me after all! Why would I even tempt them with my earlier arrogance?! Trying to figure out the right version, compatibility, and model availability just added layers of complexity I wasn't prepared for.

### The Pivot: Python is Where It's At

This is where the narrative shifted dramatically for me. The frustration with Dify's setup, versioning issues, and model availability started highlighting something fundamental. I'm already too much of a fan of how powerful it is for LLMs to leverage their natural ability to *write and understand Python code*. It struck me that *by skipping a human-designed abstraction layer like a UI-based workflow builder during the core creation process*, everything in the stack benefits.

I realized I didn't want to spend time learning the intricacies of a specific tool's UI and workflow paradigms (Dify's). The LLM itself wouldn't need extra context on how to operate *within* Dify; it could just focus on the task using its core abilities with language and code. And for running the tool, a simple Python script is infinitely less overhead than managing a whole Docker setup like Dify requires, especially for a single-user, personal project.

There's probably a really good reason why you'd want to use something like Dify – collaborative teams, complex workflows, built-in monitoring, etc. – but it's way outta my use-case alley right now. For my simple blogger tool, it felt like significant overkill and introduced unnecessary friction.

## Building a Blogger Tool in Just Python

So, I pivoted. The goal is still the same: clean up my notes into blog posts. The method is changing: straight-up Python and direct calls to the LLM API.

Here's why this feels right:
*   **LLMs are inherently good at understanding and writing code, especially Python.** This is a core strength, not an add-on feature.
*   **Python is good at doing stuff at a low enough level for this task.** Obviously, it's nothing close to C for system-level tasks, but it's *much* better than worrying about somebody else's UI abstractions, workflow definitions, and installation instructions for my simple use case. I can read a file, send it to an LLM, get text back, and write it to another file with minimal fuss.

**Yeah, this kicks ass.**

Working directly in Python:
*   **It's fast.** I can iterate quickly.
*   **It does *only* the stuff I want.** No extra features or complexities I don't need.
*   **It's been very easy to make changes.** A quick edit to a script or prompt is all it takes.

I'm currently using Flash 2.5 for this, so not even that strong of a model, and it's handling the tasks well. I'm pretty sure I have some level of 'thinking' or chain-of-thought enabled in the prompting, which helps.

**I was able to implement everything I wanted for the core functionality in only a few calls back and forth with the LLM and minor script adjustments.** This is leagues better than trying to translate my needs into a new tool's workflow or wrestling with installation issues. I'm already done with the core workflow changes and am moving on to more fun, less critical stuff like making loading animations pretty or adding little quality-of-life features.

**I'm genuinely excited to see this turn into a tool I can use every day.** My specific need is to transform my note-like, chain-of-thought writing style into something more presentable. While that style works for me reading back, it can be fragmented for others. If the LLM can come in, clean things up, add context where needed (based on the notes themselves), and keep the existing tone and style, I'll be very happy. I'm not looking for the LLM to generate *additional* content, just make the existing content more cohesive and readable.

Ultimately, while my brief attempt with Dify had its moments of hope and frustration, it clarified that for this particular project, the simplest, most direct path using Python and leveraging the LLM's core capabilities is the right one. Sometimes, the most powerful tool is the one that gets out of your way.