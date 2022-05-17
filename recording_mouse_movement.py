# -*- coding: utf-8 -*-
# import logging.config
# from settings import logger_config
#
# logging.config.dictConfig(logger_config)
# logger = logging.getLogger('app_logger')

from pynput.mouse import Listener
import logging,os

# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    if os.path.isfile('mouse_log.txt'): os.remove('mouse_log.txt')  # log файл
    logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

    def on_move(x, y):
        pass
        # logging.info("Mouse moved to ({0}, {1})".format(x, y))

    def on_click(x, y, button, pressed):
        if pressed:
            logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

    def on_scroll(x, y, dx, dy):
        logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
