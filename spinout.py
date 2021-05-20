
import sys
from time import sleep

import pygame
from pygame.locals import *
import os
import argparse


# https://www.pygame.org/docs/tut/ChimpLineByLine.html
# https://rgbcolorcode.com/
# https://riptutorial.com/pygame/example/23786/drawing-with-the-draw-module
# https://www.remove.bg/upload

GREEN = pygame.Color(144, 238, 144)
LIGHT_GREY = pygame.Color(211, 211, 211)
DARK_GREY = pygame.Color(169, 169, 169)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

SCREEN_SIZE = (900, 400)


class Spinout:
    def __init__(self):
        self.gray_code = [1, 1, 1, 1, 1, 1, 1, None, None, None, None, None, None, None]
        # self.gray_code_length = sum(1 for element in self.gray_code if element == 1)
        self.gray_code_length = 7
        self.move_history = []
        self.left_stop_position = 0
        self.working_position = self.gray_code_length - 1  # 6
        self.right_stop_position = self.working_position + 1
        self.decimal_value = self.convert_graycode_to_decimal(self.gray_code)
        self.binary_value = self.convert_graycode_to_binary(self.gray_code)
        self.shift_right_move = 'R>'
        self.shift_left_move = '<L'
        self.flip_bit_move_zero = '0'
        self.flip_bit_move_one = '1'
        return

    def update_values(self):
        if self.gray_code[0] is not None:
            self.decimal_value = self.convert_graycode_to_decimal(self.gray_code)
            self.binary_value = self.convert_graycode_to_binary(self.gray_code)
        return

    def flip_bit(self):
        if self.gray_code[self.right_stop_position] == 1 or self.gray_code[self.right_stop_position] is None:
            if self.gray_code[self.working_position] == 1:
                self.gray_code[self.working_position] = 0
                self.move_history.append(self.flip_bit_move_zero)
            else:
                self.gray_code[self.working_position] = 1
                self.move_history.append(self.flip_bit_move_one)
            return True
        else:
            return False

    def shift_right(self):
        if self.gray_code[self.right_stop_position] == 0 or self.gray_code[self.right_stop_position] is None:
            self.gray_code.insert(0, None)
            self.gray_code = self.gray_code[:self.gray_code_length * 2]
            self.move_history.append(self.shift_right_move)
            return True
        else:
            return False

    def shift_right_multi(self, positions_to_shift):
        for i in range(positions_to_shift):
            if not self.shift_right():
                print('Cannot shift RIGHT ({}/{})'.format(i, positions_to_shift))
                break
        return

    def shift_left(self):
        if self.gray_code[0] is None:
            self.gray_code.pop(0)
            if len(self.gray_code) < self.gray_code_length * 2:
                self.gray_code.append(None)
            self.move_history.append(self.shift_left_move)
            return True
        else:
            return False

    def shift_left_multi(self, positions_to_shift):
        for i in range(positions_to_shift):
            if not self.shift_left():
                print('Cannot shift LEFT ({}/{})'.format(i, positions_to_shift))
                break
        return

    def convert_graycode_to_decimal(self, gray_code):
        binary_value = self.convert_graycode_to_binary(gray_code)
        bin_str = ''.join(str(bit) for bit in binary_value)
        decimal_value = int(bin_str, 2)
        return decimal_value

    def convert_graycode_to_binary(self, gray_code):
        binary_value = []
        if gray_code[0] is not None:
            binary_value = [gray_code[0]]
            for i in range(0, self.gray_code_length - 1):
                binary_value.append(binary_value[i] ^ gray_code[i + 1])
        return binary_value

    def print_graycode(self):
        if self.gray_code[0] is not None:
            self.update_values()
            print('{}:{} = {}'.format(self.gray_code[:self.right_stop_position], self.gray_code[self.right_stop_position:],
                                      self.decimal_value))
        else:
            print('{}:{}'.format(self.gray_code[:self.right_stop_position], self.gray_code[self.right_stop_position:]))
        return


def update_message(screen, message):
    msg_surface = pygame.Surface((int(screen.get_width() * .5), 50))
    msg_surface.fill(WHITE)
    msg_surface.convert()
    msgfont = pygame.font.SysFont('', 24)
    msgtext = msgfont.render(message, True, (0, 0, 0))
    msg_surface.blit(msgtext, (msgtext.get_rect(center=(msg_surface.get_width() / 2, msg_surface.get_height() / 2))))
    # screen.blit(msg_surface, (0, screen.get_height() - 100))
    screen.blit(msg_surface, (msg_surface.get_rect(center=(screen.get_width() / 2,  screen.get_height() - 100))))
    return


def update_info_boxes(screen, binary_value, decimal_value):
    # TODO
    msg_surface = pygame.Surface((400, 50))
    msg_surface.fill(WHITE)
    msg_surface.convert()
    msgfont = pygame.font.SysFont('', 24)
    message = 'Binary: {}  Decimal: {}'.format(binary_value, decimal_value)
    msgtext = msgfont.render(message, True, (0, 0, 0))
    msg_surface.blit(msgtext, (msgtext.get_rect(center=(msg_surface.get_width() / 2, msg_surface.get_height() / 2))))
    #screen.blit(msg_surface, (0, screen.get_height() - 200))
    screen.blit(msg_surface, (msg_surface.get_rect(center=(screen.get_width() / 2,  screen.get_height() - 200))))
    return

def wait_for_quit(screen):

    update_message(screen, 'Click to Quit')
    print('Click to Close')

    # show updated screen
    pygame.display.flip()

    # Handle Input Events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print('mouse click {}'.format(pos))
                return


def update_screen(spinout, screen, message):

    # calculate cell size and spacing
    cell_spacing = 1
    screen_padding = 10
    cell_width = int((screen.get_width() - screen_padding) / len(spinout.gray_code)) - cell_spacing
    cell_height = int(cell_width * 1.4)
    line_width = 5
    cell_tops = (screen_padding, cell_width)
    cell_bottoms = (screen_padding, cell_width + cell_height)

    # create cells
    for i in range(spinout.gray_code_length * 2):
        # create cell
        cell = pygame.Surface((cell_width, cell_height))

        # if working position, fill cell with green or red depending upon blocked state
        if i == spinout.working_position:
            cell.fill(WHITE)
            # if blocked outline in red
            if spinout.gray_code[i] is not None and spinout.gray_code[i + 1] == 0:
                pygame.draw.rect(cell, RED, cell.get_rect(), line_width)
            else:
                pygame.draw.rect(cell, GREEN, cell.get_rect(), line_width)
        else:
            # else fill with grey
            cell.fill(LIGHT_GREY)

        # draw left border
        if i == spinout.left_stop_position:
            pygame.draw.line(cell, DARK_GREY, (0, 0), (0, cell_height), width=line_width)

        # if right stop cell, draw two lines as blockers
        if i == spinout.right_stop_position:
            # -line_width/2 to adjust for direction line is drawn
            pygame.draw.line(cell, DARK_GREY, (cell_width - int(line_width/2), 0),
                             (cell_width - int(line_width/2), int(cell_height * 0.3)),
                             width=line_width)
            pygame.draw.line(cell, DARK_GREY, (cell_width - int(line_width/2), cell_height),
                             (cell_width - int(line_width/2), cell_height - int(cell_height * 0.3)),
                             width=line_width)

        # add bit widget to cells according to gray code
        if spinout.gray_code[i] is not None:

            if spinout.gray_code[i] == 1:
                msgfont = pygame.font.SysFont('', 100)
                msgtext = msgfont.render('1', True, BLACK)
                cell.blit(msgtext, (msgtext.get_rect(center=(cell.get_width()/2, (cell.get_height()/2) + 3))))

            else:
                msgfont = pygame.font.SysFont('', 100)
                msgtext = msgfont.render('0', True, BLACK)
                msgtext = pygame.transform.rotate(msgtext, 90)
                cell.blit(msgtext, (msgtext.get_rect(center=((cell.get_width()/2)+2, cell.get_height()/2))))

        # display cells
        cell = cell.convert()
        screen.blit(cell, (screen_padding + (i * cell_width) + (i * cell_spacing), cell_width))

    # add rails
    rail_thickness = int(cell_height * 0.2)
    rail_bar = pygame.Surface((((spinout.right_stop_position - 1) * cell_width) +
                               ((spinout.right_stop_position - 2) * cell_spacing),
                               rail_thickness))
    rail_bar.fill(DARK_GREY)
    rail_bar.convert()

    # add rails to screen, top and bottom
    screen.blit(rail_bar, cell_tops)
    screen.blit(rail_bar, (cell_bottoms[0], cell_bottoms[1] - rail_thickness))

    # add rails to stop position, top and bottom
    rail_bar = pygame.Surface((cell_width, rail_thickness))
    rail_bar.fill(DARK_GREY)
    rail_bar.convert()
    screen.blit(rail_bar, (screen_padding + (spinout.right_stop_position * cell_width) +
                           (spinout.right_stop_position * cell_spacing), cell_tops[1]))
    screen.blit(rail_bar, (screen_padding + (spinout.right_stop_position * cell_width) +
                           (spinout.right_stop_position * cell_spacing), cell_bottoms[1] - rail_thickness))

    # TODO - Make Quit button

    # update info boxes
    update_info_boxes(screen, spinout.binary_value, spinout.decimal_value)

    # message
    update_message(screen, message)

    # show updated screen
    pygame.display.flip()
    return


def run(solve_it=False, solve_speed=1, show_gui=True):

    # TODO - implement show_gui argument

    spinout = Spinout()
    spinout.print_graycode()

    # init screen
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("~Spinout~")
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    message = ''
    # create white background and fill game screen
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    background = background.convert()
    screen.blit(background, (0, 0))

    update_screen(spinout, screen, message)

    if solve_it:
        run_solution(spinout, screen, solve_speed)
    else:

        # main loop
        run_main_loop = True
        while run_main_loop:
            clock.tick(40)

            # Handle Input Events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run_main_loop = False

                # press ESCAPE to exit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run_main_loop = False

                # shift right
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if spinout.shift_right():
                        spinout.print_graycode()
                        message = ''
                    else:
                        message = 'Cannot shift RIGHT'
                        print(message)
                    spinout.update_values()

                # shift left
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if spinout.shift_left():
                        spinout.print_graycode()
                        message = ''
                    else:
                        message = 'Cannot shift LEFT'
                        print(message)
                    spinout.update_values()

                # flip bit
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if spinout.flip_bit():
                        spinout.print_graycode()
                        message = ''
                    else:
                        message = 'Cannot flip bit'
                        print(message)
                    spinout.update_values()

                # click in red rectangle to exit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    # if 10 <= pos[0] <= 810 and 20 <= pos[1] <= 220:
                    #     sys.exit()

                update_screen(spinout, screen, message)

    wait_for_quit(screen)
    return


def run_solution(spinout, screen, speed=1):
    """
    List of steps to solve the puzzle.
      0 or 1 indicate a bit flip at the working location
      Rx indicates a shift to the right of x bits
      Lx indicates a shift to the left of x bits
    """
    steps = ['0', 'R2', '0', 'L2', '1', 'R1', '0', 'L1', '0', 'R4', '0', 'L4', '1', 'R1', '1', 'L1', '0', 'R2', '1',
             'L2', '1', 'R1', '0', 'L1', '0', 'R3', '0', 'L3', '1', 'R1', '1', 'L1', '0', 'R2', '0', 'L2', '1', 'R1',
             '0', 'L1', '0', 'R6', '0', 'L6', '1', 'R1', '1', 'L1', '0', 'R2', '1', 'L2', '1', 'R1', '0', 'L1', '0',
             'R3', '1', 'L3', '1', 'R1', '1', 'L1', '0', 'R2', '0', 'L2', '0', 'R1', '0', 'L1', '0', 'R4', '1', 'L4',
             '1', 'R1', '1', 'L1', '0', 'R2', '1', 'L2', '1', 'R1', '0', 'L1', '0', 'R3', '0', 'L3', '1', 'R1', '1',
             'L1', '0', 'R2', '0', 'L2', '1', 'R1', '0', 'L1', '0', 'R5', '0', 'L5', '1', 'R1', '1', 'L1', '0', 'R2',
             '1', 'L2', '1', 'R1', '0', 'L1', '0', 'R3', '1', 'L3', '1', 'R1', '1', 'L1', '0', 'R2', '0', 'L2', '1',
             'R1', '0', 'L1', '0', 'R4', '0', 'L4', '1', 'R1', '1', 'L1', '0', 'R2', '1', 'L2', '1', 'R1', '0', 'L1',
             '0', 'R3', '0', 'L3', '1', 'R1', '1', 'L1', '0', 'R2', '0', 'L2', '1', 'R1', '0', 'L1', '0', 'R7']
    
    for step in steps:
        spinout.print_graycode()
        if step == '0' or step == '1':
            spinout.flip_bit()
        elif step[0] == 'R':
            distance = int(step[1])
            spinout.shift_right_multi(distance)
        elif step[0] == 'L':
            distance = int(step[1])
            spinout.shift_left_multi(distance)

        update_screen(spinout, screen, 'Decimal: {}'.format(spinout.decimal_value))
        sleep(1/speed)

        # Handle Input Events
        for event in pygame.event.get():
            # Close window
            if event.type == pygame.QUIT:
                return
            # press ESCAPE to exit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

    # print('\n'.join(spinout.move_history))
    return


if __name__ == '__main__':

    print('Spinout computer simulation, (C) 2020 MSRoth')
    print('\nUse left (<-) and right (->) arrow keys to slide spinners.  Use space bar to flip')
    print('bit in work cell.')

    #create arg parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=int, default=None, help='Solve with speed [1 (slow)-10 (fast)]')
    parser.add_argument('-x', action='store_false', default=True, help='Show GUI')

    solve_speed = 1
    solve_it = False
    show_gui = True

    args = parser.parse_args()

    if args.s is not None:
        solve_speed = args.s
        solve_it = True
    if not args.x:
        show_gui = False

    run(solve_it, solve_speed, show_gui)
    pygame.quit()
    print('Quit')


# <SDG><
