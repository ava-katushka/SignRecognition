__author__ = 'ava-katushka'
from ChineseCharacterApplication import *
import sys

def main():
    app = QtGui.QApplication(sys.argv)
    ex = ChineseCharacterApplication()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()