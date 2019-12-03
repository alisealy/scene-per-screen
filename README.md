# scene-per-screen
This project aims to allow blender 2.8x to emulate the behaviour of blender 2.7x whereby scenes were stored as a property of a specific "screen". 

The current implementation makes use of a custom property that is added to blender's "Screen" data-block, which stores a string representing the name of a scene. 
There are currently a pair of python scripts which allow a pre-made scene/screen setup to be exported from a .blend file made in blender 2.79, and subsequently imported and saved in a blender 2.80-compatible .blend file. 

The planned development is for an add-on that would read this data and automatically switch the scene accordingly. 

This project started from a discussion on blenderartists forum:
https://blenderartists.org/t/how-execute-script-with-global-shortcut/1192329/8

# Background:
blender 2.80 introduced a new UI design with many changes from the previous 2.79 release. One of the changes was that the project scene was now global instead of per-"screen", another change was the addition of tabs in a top-bar to switch between workspaces, where previously there was a drop-down list to switch between "screens". 
While for most users and most cases these changes represent an improvement in useability, there remain some cases where this design is impractical. 
For example, a highly customised blender set-up with many custom screens or workspaces, with workspace-specific data stored in custom scenes attached to these workspaces. For this case the design of blender 2.80 presents some problems, illustrated in this thread on blenderartists:
https://blenderartists.org/t/free-animation-kit-needs-your-help/1189275

The goal of this project is to allow blender 2.8x to emulate the way these cases were handled in 2.7x, but in a way that can be easily enabled or disabled depending on user preference. 
