#!/usr/bin/env python
"""glshowenv.py: Show the current OpenGL connection strings.

Usage:
  glshowenv.py [GLUT_OPTIONS]
"""

import sys
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT

def main():
    """Show the current OpenGL connection strings."""

    GLUT.glutInit(sys.argv)
    GLUT.glutInitContextVersion(3, 3)
    GLUT.glutInitContextProfile(GLUT.GLUT_CORE_PROFILE)
    GLUT.glutInitDisplayMode(
        GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH)
    win = GLUT.glutCreateWindow(b'NO TITLE')

    aspects = {'Vendor':GL.GL_VENDOR,
               'Renderer':GL.GL_RENDERER,
               'Version':GL.GL_VERSION,}
    if GL.glCreateShader:
        aspects['GLSL'] = GL.GL_SHADING_LANGUAGE_VERSION

    print('\n'.join('{}: {}'.format(key, GL.glGetString(val).decode())
                    for key, val in aspects.items()))

    GLUT.glutDestroyWindow(win)

if __name__ == '__main__':
    main()
