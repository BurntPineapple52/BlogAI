# notes
- goals 
    - learn the basics of Diffy
    - make my smol blogger in diffy
    - compare experience implementing on both platforms 
- I remembered to set up my python venv right away.  good job me. 
- Followed the instructions from here https://docs.dify.ai/en/getting-started/install-self-hosted/docker-compose
- I honestly have a very, very loose understanding of docker.  I get why it's helpful, but I don't have a grasp on the commands and really wtf is all running, but hey, I'm not an engineer.  
- it's *so fucking nice* to use modern tools that people who care are working on.  setup is a breeze, docs (when updated) aren't just full of lies. nice way to start the day.
- ok ok ok of course I run into a problem the second I finish typing that, during the upgrade steps the quickstart recommend I install.  Pain. ego death and p ain. 
- Deleted and uninstalled all the diffy stuff, reinstalled and we're up and running.  Shit is clean.
- SHIT IS NOT CLEAN! I'm trying to get the open router free models going and no dice.  There are only a very limited number of models from openrouter.
- ah it's an old version I got. of course.  those god damn docs are fucking me! Why would I even tempt them with my arrogance! 
- ok no, I no like.  I'm already too much of a fan of how smolagent can leverage the natural ability of LLMs to write stuff in python. I'm getting he impression that *by skipping the human abstraction layer during the creation process* everything in the stack benefits.  I don't have to worry about learning a tool that's getting in my way, the LLM doesn't need even MORE context to get a change in place, and the computer can happily run the python code instead of a whole docker whojiggy like you have to do with Dify. 
- There's probably a reason why you'd want to use something like Dify, but it's way outta my use-case alley right now.  

## this is now a post about how I'm going to make a little blogger in just python
- LLMs are good at python
- python is good at doing stuff at a low enough level.  Obviously nothing close to anything C related, but much better than worrying about somebody elses abstractions and instructions for my simple use case.

**Yeah this kicks ass** 
- it's fast, it does only the stuff I want, and it's been very easy to make changes.  
- I'm using flash 2.5 so not even that strong of a model.  I'm pretty sure I have thinking on.

**I was able to implement everything I wanted in only a few calls back and forth** 
- this is leagues better than going through additional abstraction. I'm done with workflow changes and now I'm doing fun stuff like making the loading animations pretty.

**I'm excited to see this turn into a tool I can use every day**
- I like blogging in a very note like chain of thought pattern, which is fine when I read it back, but can be a little fragmented to the outside reader.  
- If the LLM can come in, clean things up, and keep the existing tone and style, i'll be very happy.  I'm not looking for any additional content as much as I'd like it to be more cohesive, and I'd like context added where it makes sense.