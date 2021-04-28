from OpenGL.GL import *
import cv2
import math

def ps(deg,length,lp):# pixel size
    return 2 * length * math.tan(math.pi*deg/360)/lp

def makeline(length,lp):
    vtx2 = [0, ps(0.5,length,lp), 0, -ps(0.5,length,lp)]
    glVertexPointer(2, GL_FLOAT, 0, vtx2)
    glLineWidth(5)
    glColor4f(0, 0, 0, 1.0)

    glEnableClientState(GL_VERTEX_ARRAY)
    glDrawArrays(GL_LINES, 0, 2)
    glDisableClientState(GL_VERTEX_ARRAY)

def render(g_texID, angle,om,widthp,hightp,length,imsize,lp):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glTranslatef(widthp/2, hightp/2, 0.0)
    makeline(length,lp)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(widthp/2, hightp/2, 0.0)
    glRotatef(90, 0.0, 0.0, 1.0)
    makeline(length,lp)
    glPopMatrix()

    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glTranslatef(widthp/2, hightp/2, 0.0)
    glTranslatef(-ps(12,length,lp), 0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)
    imageplot(g_texID,om,imsize,length,lp)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def oerender(g_texID,widthp,hightp):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    oeplot(g_texID,widthp,hightp)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def wrender(widthp,hightp,length,lp):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glTranslatef(widthp/2, hightp/2, 0.0)
    makeline(length,lp)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(widthp/2, hightp/2, 0.0)
    glRotatef(90, 0.0, 0.0, 1.0)
    makeline(length,lp)
    glPopMatrix()

def imageplot(g_texID,om,imsize,length,lp):

    hssw=ps(imsize,length,lp)/2 #half stimli size width
    hssh=ps(imsize,length,lp)/2 #half stimli size hight

    vtx = [-hssw, -hssh,\
           -hssw,  hssh,\
            hssw,  hssh,\
            hssw, -hssh]
    glVertexPointer(2, GL_FLOAT, 0, vtx)

    #Step5.テクスチャの領域指定
    if int(om)==0:
        texuv = [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0] # original
    elif int(om)==1:
        texuv = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0] # mirror
    glTexCoordPointer(2, GL_FLOAT, 0, texuv)
    glColor4f(1, 1, 1, 0)

    #Step6.テクスチャの画像指定
    glBindTexture(GL_TEXTURE_2D,g_texID)

    #Step7.テクスチャの描画
    glDrawArrays(GL_QUADS, 0, 4)

def oeplot(g_texID,widthp,hightp):
    w=hightp/widthp
    h=1
    vtx = [widthp/2-hightp/2,      0,\
           widthp/2-hightp/2, hightp,\
           widthp/2+hightp/2, hightp,\
           widthp/2+hightp/2,      0]
    glVertexPointer(2, GL_FLOAT, 0, vtx)

    #Step5.テクスチャの領域指定
    texuv = [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0]
    glTexCoordPointer(2, GL_FLOAT, 0, texuv)
    glColor4f(1,1,1, 0)

    #Step6.テクスチャの画像指定
    glBindTexture(GL_TEXTURE_2D,g_texID)

    #Step7.テクスチャの描画
    glDrawArrays(GL_QUADS, 0, 4)

def setupTexture(texID, imagepath):
    #Sload a image
    image = cv2.imread(imagepath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #Connect image data and texture iD
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.shape[0], image.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, image)

    #Various texture settings
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
