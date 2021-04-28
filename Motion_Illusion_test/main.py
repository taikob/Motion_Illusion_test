import glfw, time, sys, os, shutil, argparse
from OpenGL.GL import *
import test as move
import make_test_sheet as ts #test sheet
import file as f

switch=0
ans=-1
go=0
wtime=0
startpath='Motion_Illusion_test/start.png'
endpath='Motion_Illusion_test/end.png'

def keyboard(window, key, scancode, action, mods):
    global switch, ans, go
    if action == glfw.PRESS:
        if   switch==0: switch=1
    elif  key == glfw.KEY_Q:
            if (switch==2 or switch==3) and go==0: switch=5
    elif  key == glfw.KEY_A:
            if switch==2 or switch==3: ans=1
    elif  key == glfw.KEY_L:
            if switch==2 or switch==3: ans=0
    elif  key == glfw.KEY_SPACE and (switch==2 or switch==3) and (ans==1 or ans==0):
        go=1

def main(savedpath):
    global go, wtime, switch, ans

    if savedpath=='':
        sys.path.append(os.getcwd())
        import config as p
        folderpath=str(int(time.time()))
        os.mkdir(folderpath)
        shutil.copy('./config.py', folderpath)
        clist = ts.make_sheet(p.nitr, p.max, p.nd)
    else:
        folderpath=str(savedpath)
        sys.path.append(os.getcwd()+'/'+folderpath)
        clist=f.load_list(folderpath+'/clist.txt')
        import config as p


    # GLFW Initialize
    if not glfw.init():
        return

    # make window
    window = glfw.create_window(p.widthp, p.hightp, 'Hello World', glfw.get_primary_monitor(), None)
    if not window:
        glfw.terminate()
        print('Failed to create window')
        return

    # make context
    glfw.make_context_current(window)

    # Specify version
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.set_key_callback(window, keyboard)

    g_texID=glGenTextures(3)
    move.setupTexture(g_texID[0], p.imagepath)
    move.setupTexture(g_texID[1], startpath)
    move.setupTexture(g_texID[2],   endpath)

    #Specifying the drawing range
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, p.widthp, 0.0, p.hightp, -1.0, 1.0)

    angle=0
    last=time.time()
    c=0
    anslist=[]
    while not glfw.window_should_close(window):
        #time
        now = time.time()
        dt= now - last
        last=now

        # Initialize the buffer with the specified color
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if switch==0:# start
            move.oerender(g_texID[1],p.widthp ,p.hightp)
        elif switch==1:# wait
            move.wrender(p.widthp, p.hightp, p.length, p.lp)
            wtime += dt
            if wtime > 3:
                wtime=0
                switch = 2
        elif switch==2:# show stimuli
            cd=clist[c]
            angle+=float(cd[1])*dt
            move.render(g_texID[0], angle,cd[0], p.widthp, p.hightp, p.length, p.imsize, p.lp)
            wtime += dt
            if wtime > 0.5:
                wtime=0
                switch=3
        elif switch==3:# type key
            move.wrender(p.widthp, p.hightp, p.length, p.lp)
            wtime += dt
            if wtime > 1 and go==1:
                clist[c].append(ans)
                anslist.append(clist[c])
                wtime=0
                go=0
                ans=-1
                angle=0
                if c==len(clist)-1: switch = 4
                else:
                    c+=1
                    switch = 2
        elif switch==4:# finish
            move.oerender(g_texID[2], p.widthp, p.hightp)
            wtime += dt
            if wtime > 3:
                break
        elif switch==5:# finish & save
            move.oerender(g_texID[2], p.widthp, p.hightp)
            wtime += dt
            if wtime > 3:
                f.save_list(clist[c:], folderpath + '/clist.txt',md='w')
                break

        # Swap buffers and refresh screen
        glfw.swap_buffers(window)

        # Accept events
        glfw.poll_events()

    # Destroy the window and exit GLFW
    glfw.destroy_window(window)
    glfw.terminate()

    f.save_list(anslist, folderpath+'/'+p.imagepath.split('/')[-1].replace('.png','')+'_ans.txt')
    if args.path!='' and c==len(clist)-1:
        os.remove(folderpath + '/clist.txt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='plot_data')
    parser.add_argument('--path', '-p', default='', type=str, help='config')
    parser.set_defaults(test=False)
    args = parser.parse_args()

    main(args.path)