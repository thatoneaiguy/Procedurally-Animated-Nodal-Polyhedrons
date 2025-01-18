# Procedurally Animated Nodal Polyhedrons
- [Procedurally Animated Nodal Polyhedrons](#procedurally-animated-nodal-polyhedrons)
  * [Intro](#intro)
  * [How to use](#how-to-use)
    + [However, this can be more than just scrolling](#however--this-can-be-more-than-scrolling)
  * [Patterns](#patterns)
  * [Setup](#setup)
## Intro
Heya! I'm Everest, and I made this node simulator to prove that libarys such as pygame can be used for more than their intended purpose
## How to use
I don't like complex design, so this is really easy to use at a base level, but also in more "advanced" ways.

At a base level, there are two main controls you need to know, and they're both very logical.
- To add nodes, scroll up
- To remove nodes, scroll down

### However, this can be more than just scrolling
If you want to push this simulation to its limits ( really just pygame's limits combined with your pc ), you can spawn in a specific amount of nodes.
On line [] there is a variable called `node_count`. This defaults to `10`, because i think it looks nice when you start the program, but it can be used to spawn in a specific amount of nodes on startup.

Based on the default `radius` value of `350`

- At 90 nodes, the polygon will start to look like a filled in circle, with a few minor spots.
- Infuriatingly, at 100 nodes, the circle will only have one dot that is unfilled, meaning 102 makes a solid circle

## Patterns
This simulation has a lot of patterns, but there is specific settings to help you notice those!
I'd reccoment the following settings. To change these, go to where these variables are defined in the code and replace them with the following

```py
# Colors
BACKGROUND_COLOR = (0, 0, 0)
NODE_COLOR = (0, 0, 255)
LINE_COLOR = (255, 0, 0)
DOT_COLOR = (0, 0, 0)
```

This makes the lines very disticnt to everything else on screen.

## Setup
1. Make sure you have [python]() installed
2. Paste in the code in [main.py]() into your dev window of choice. This can just be a text document renamed after putting the code in to end in .py, however for that you must have show file extensions turned on.
3. Run the program

Alternatly
1. Go to the [releases]() tab
2. Download the latest `.exe`
3. Run the program
However with this method, you cannot edit the code
