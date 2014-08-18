#/usr/bin/python
#coding:utf-8

f = open('mail_list.txt')
all = f.readlines()
f.close()

f = open('new.txt', 'w')
while True:
    for i in range(5):
        if all:
            f.write('%s ' % all.pop().strip())
    f.write('\n')
    if not all:
        break


