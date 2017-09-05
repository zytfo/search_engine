# -*- coding: utf-8 -*-
'''
    Splitting LISA arhchives into the bunch of documents
'''

counter = 1
for i in range(1, 15):
    with open('/Users/Artur/Desktop/lisa/Archives/LISA' + str(i)) as file:
        for line in file:
            file = open('/Users/Artur/Desktop/lisa/Documents/' + str(counter) + '.txt', 'a')
            if line.find("********************************************") == -1:
                if 'Document' not in line:
                    file.write(line)
            else:
                file.close()
                counter += 1