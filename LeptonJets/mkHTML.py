#!/usr/bin/env python

import os
import sys

if __name__ == '__main__':
    
    plotsuf = ['gif', 'jpg', 'png']

    scriptname=sys.argv[0]
    scriptpath=scriptname.split("/mkHTML.py")[0]
    files = os.listdir(scriptpath)
    cwd = os.getcwd()

    ausgabe = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n\
    <html xmlns="http://www.w3.org/1999/xhtml">\n\
    <head>\n\
    <style type="text/css">\n\
    <!--\n\
    body {position: absolute; background: white; margin: 0; padding: 0;}\n\
    div#images {width: 130;}\n\
    div#images a p img {height: 0; width: 0; border-width: 0;}\n\
    div#images a:hover p img {position: fixed; top: 157px; left: 600px; height: 372px; width: 596px;}\n\
    -->\n\
    </style>\n\
    <title>Plots in Directory %s</title>\n\
    </head>\n\
    <body>\n\
    <a href="./.." target="_top">Parent Directory</a>\n\
    <!--h1> <fonts style="position:fixed; top:0%%; left:45%%"> Validation plots </h1-->\n\
    <div id="images">\n\
    <table>\n\
    <tr>\n' % cwd
        
    plots = []
    alreadyexists = 0
    
    for file in files:
        if (file.split('.')[-1]) not in plotsuf:
            continue
        else:
            for file2 in plots:
                if (file.split('.')[0] == file2.split('.')[0]):
                    alreadyexists = 1
                    break
            if (alreadyexists == 0):
                plots.append(file)
            alreadyexists = 0

    
    i = 0
    j = 0
    ausgabe2 = ""
    ausgabe1 = ""

    plotsuf2 = plotsuf
    plotsuf2.append('eps');
    plotsuf2.append('tiff');
    
    for plot in plots:
        ausgabe1 += '        <td><a href="./%s" target="plots"><img src="%s" height=120 width=160></a></td>\n' % (plot,plot)
        ausgabe2 += '<td>'
        for suffix in plotsuf2:
            if (plot.split('.')[0]+"."+suffix) in files:
                ausgabe2 += '        <a href="./%s" target="_top">%s</a>' % (plot.split('.')[0]+"."+suffix,suffix)
        ausgabe2 += '</td>\n'
        i += 1
        j += 1
        if (i % 2) == 0:
            ausgabe += ausgabe2
            ausgabe += '</tr>\n  <tr>'
            ausgabe += ausgabe1
            ausgabe += '</tr>\n  <tr>'
            ausgabe1 = ""
            ausgabe2 = ""
    if (j % 2) == 1:
        ausgabe += ausgabe2
        ausgabe += '</tr>\n  <tr>'
        ausgabe += ausgabe1
        ausgabe += '</tr>\n  <tr>'
        ausgabe1 = ""
        ausgabe2 = ""
            
    ausgabe += '</tr>    </table>\n     </div>\n  </body>\n'
#    ausgabe += "     <iframe src=\"./frames.html\" name=\"fenster\"  style=\"position:fixed; left:400px; top:20%; height: 80%; width:80%; border-width: 0;\" ></iframe>\n"
    ausgabe +='</html>\n'
                
plotsdir = open(scriptpath+'/overview.html', 'w+')
plotsdir.write(ausgabe)
plotsdir.close()

plotsdir = open(scriptpath+'/empty.html', 'w+')
plotsdir.write('<html>\n  <center> <pre> \n \n \n No histogram selected \n </pre>  </center> </html>')
plotsdir.close()

indexausgabe = ""
indexausgabe += '<html>\n'
indexausgabe += '  <head>\n'
indexausgabe += '    <title>Validation plots</title>\n'
indexausgabe += '  </head>\n'
indexausgabe += '  <frameset cols="370,*">\n'
indexausgabe += '    <frame src="overview.html" name="overview">\n'
indexausgabe += '  <frameset rows="180,*">\n'
indexausgabe += '    <frame src="analysis.html" name="analysis">\n'
indexausgabe += '    <frame src="empty.html" name="plots">\n'
indexausgabe += '  <noframes>\n'
indexausgabe += '    Ihr Browser kann keine Frames!\n'
indexausgabe += '  </noframes>\n'
indexausgabe += '  </frameset>\n'
indexausgabe += '</html>\n'

plotsdir = open(scriptpath+'/index.html', 'w+')
plotsdir.write(indexausgabe)
plotsdir.close()

indexausgabe = ""


analysisausgabe = ""
analysisausgabe += '<html>\n'
analysisausgabe += '  <head>\n'
analysisausgabe += '    <title>Process and analysis</title>\n'
analysisausgabe += '  </head>\n'
analysisausgabe += '  <body>\n'
analysisausgabe += '    <h1> <fonts style="position:fixed; top:0%; left:45%"> Validation plots </h1> <br><br>\n'
analysisausgabe += '  For these plots the following setup was used:<br>\n'
#analysisausgabe += '    <a href="./Pythia8Process_top.config" target="plots"> configuration </a> of the process (analysis kind, steering file, etc.) <br>\n'




analysisausgabe += '  </body>\n'
analysisausgabe += '</html>\n'

plotsdir = open(scriptpath+'/analysis.html', 'w+')
plotsdir.write(analysisausgabe)
plotsdir.close()

analysisausgabe = ""
