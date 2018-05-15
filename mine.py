#coding:utf-8

__author__ = 'Gkyou'

import pyglet
import random, time

WIN_WIDTH = 800
WIN_HEIGHT = 450

BACKGROUND_COLOR = (255 ,250 ,240, 250)
COLOR_BLACK = (0, 0, 0, 255)
BLOCK_COLOR = (238 ,232 ,170, 255)
COLOR_RED = (255, 0, 0, 250)
RANK_NUM = 12
MINE_NUMBER = 9
STATR_BITWISE = 10
BLOCK_LEN = (WIN_HEIGHT - STATR_BITWISE * 2)/RANK_NUM

class Mine(pyglet.window.Window):
	"""docstring for Mine"""
	def __init__(self):
		super().__init__(WIN_WIDTH, WIN_HEIGHT)
		self.data = []
		self.game_init()
		self.be_dig_out = []
		self.start_time = 0
		self.is_game_over = False

	def game_init(self):
		self.data = []
		self.be_dig_out = []
		self.start_time = 0
		self.is_game_over = False

		frame_img = pyglet.image.SolidColorImagePattern(color = BACKGROUND_COLOR)
		self.frame = pyglet.sprite.Sprite(frame_img.create_image(WIN_WIDTH, WIN_HEIGHT), 0, 0)

		self.main_batch = pyglet.graphics.Batch()

		self.time = pyglet.text.Label(text='0:0', color = COLOR_BLACK, x = WIN_WIDTH - 100, \
			y = WIN_HEIGHT - 100, bold = True, anchor_x = 'center', anchor_y = 'center', font_size = 40, batch = self.main_batch)

		self.restart = pyglet.text.Label(text = 'resume', color = COLOR_BLACK, x = WIN_WIDTH - 100, \
			y = 100, anchor_x = 'center', anchor_y = 'center', font_size = 40, batch = self.main_batch)

		#initialize data
		self.data_init()
		
	#pyglet on_draw函数重写，事件触发
	def on_draw(self):
		self.clear()
		self.frame.draw()
		self.draw_grid()
		self.compute_time()
		self.main_batch.draw()

	#restart button 
	def restart_button(self):
		# pyglet.graphics.draw(
		# 	4, pyglet.gl.GL_QUADS,
		# 	('v2f',(WIN_WIDTH - 100, 10,
		# 			WIN_WIDTH - 10, 10 ,
		# 			WIN_WIDTH - 10, 10 + 50,
		# 			WIN_WIDTH - 100, 10 + 50)),
		# 	('c4B', (255 ,228 ,196, 255) * 4)
		# 	)
		pass

	#the event which need update automatic
	def update_interval(self, dt):
		self.compute_time()
		self.time.draw()
		print('%f  %f' % (dt, pyglet.clock.get_fps()))

	def compute_time(self):
		if self.is_game_over:
			return

		if 0 == self.start_time:
			total_seconds = 0
		else:
			total_seconds = time.time() - self.start_time
		
		time_seconds = total_seconds % 60
		time_mins = int(total_seconds / 60)
		#update time
		self.time.text = '%2d:%2d' % (time_mins, time_seconds)

	#pyglet on_mouse_press re-write
	def on_mouse_press(self, x, y, button, modifiers):
		block_x = int((x - STATR_BITWISE) / BLOCK_LEN)
		block_y = int((y - STATR_BITWISE) / BLOCK_LEN)

		if [block_x, block_y] in self.be_dig_out:
			return

		if button & pyglet.window.mouse.LEFT:
			block_x_len = (x - STATR_BITWISE) % BLOCK_LEN
			block_y_len = (y - STATR_BITWISE) % BLOCK_LEN
			if block_x_len > 3 and block_x_len < (BLOCK_LEN - 3) and block_y_len > 3 and block_y_len < (BLOCK_LEN - 3) \
			and STATR_BITWISE < x < STATR_BITWISE + BLOCK_LEN * RANK_NUM:
				position_x = block_x * BLOCK_LEN + STATR_BITWISE + BLOCK_LEN / 2
				position_y = block_y * BLOCK_LEN + STATR_BITWISE + BLOCK_LEN / 2
				print(block_x,block_y)
				if block_x > RANK_NUM -1 or block_y > RANK_NUM -1:
					return
				self.be_dig_out.append([block_x, block_y])

				if self.data[block_x][block_y] == 0:
					#check the 4 sides of this point
					#up
					if block_y + 1 < RANK_NUM:
						self.on_mouse_press(x, y + BLOCK_LEN, pyglet.window.mouse.LEFT, None)
					#down
					if block_y - 1 >= 0:
						self.on_mouse_press(x, y - BLOCK_LEN, pyglet.window.mouse.LEFT, None)
					#left
					if block_x - 1 >= 0:
						self.on_mouse_press(x - BLOCK_LEN, y, pyglet.window.mouse.LEFT, None)
					#left
					if block_x + 1 < RANK_NUM:
						self.on_mouse_press(x + BLOCK_LEN, y, pyglet.window.mouse.LEFT, None)
				#mine number
				elif self.data[block_x][block_y] >= 9:
					pyglet.text.Label(text = 'MINE', bold=True, x = position_x, y = position_y, \
					anchor_x = 'center', anchor_y = 'center', color = COLOR_BLACK, batch = self.main_batch)
					pyglet.text.Label(text = 'GAME OVER', bold = True, x = WIN_WIDTH/2, y = WIN_HEIGHT/2, anchor_x = 'center', \
					anchor_y = 'center', color = COLOR_BLACK, batch = self.main_batch, font_size = 100)
					self.is_game_over = True
				else:
					pyglet.text.Label(text = '%d' % self.data[block_x][block_y], bold=True, x = position_x, y = position_y, \
					anchor_x = 'center', anchor_y = 'center', color = COLOR_BLACK, batch = self.main_batch)
			#resume
			elif x > WIN_WIDTH - 200 and x < WIN_WIDTH and y > 80 and y < 110:
				self.restart.bold = True
				self.game_init()
				return
		elif button & pyglet.window.mouse.RIGHT:
			# pyglet.text.Label(text = 'mouse right press,x = %d,y = %d' % (x,y), x = x, y = y, anchor_x = 'center', \
			# 	anchor_y = 'center', color = COLOR_BLACK, batch = self.main_batch)
			position_x = block_x * BLOCK_LEN + STATR_BITWISE
			position_y = block_y * BLOCK_LEN + STATR_BITWISE
			self.main_batch.add(4, pyglet.gl.GL_LINES, None,
				('v2f',(position_x + 10, position_y + 10,
						position_x + BLOCK_LEN -10, position_y +BLOCK_LEN -10,
						position_x + BLOCK_LEN -10, position_y + 10,
						position_x + 10,position_y +BLOCK_LEN -10)),
				('c4B', COLOR_RED * 4))

		#start timer
		if 0 == self.start_time:
			self.start_time = time.time()

	def on_mouse_release(self, x, y, button, modifiers):
		if button and pyglet.window.mouse.LEFT:
			if x > WIN_WIDTH - 200 and x < WIN_WIDTH and y > 90 and y < 110:
				self.restart.bold = False


	#initialize the data
	def data_init(self):
		self.data = [[0 for x in range(RANK_NUM)] for y in range(RANK_NUM)]

		#bury mines, 9
		for each in range(int(RANK_NUM/2.5)**2):
			x = random.randint(0, RANK_NUM -1)
			y = random.randint(0, RANK_NUM -1)
			while self.data[x][y] >= MINE_NUMBER:
				x = random.randint(0, RANK_NUM -1)
				y = random.randint(0, RANK_NUM -1)
			self.data[x][y] = MINE_NUMBER

			#count number
			if x -1 >= 0:
				if y - 1 >= 0:
					self.data[x-1][y-1] += 1

				self.data[x-1][y] += 1

				if y + 1 <= RANK_NUM -1:
					self.data[x-1][y+1] += 1

			if x + 1 <= RANK_NUM -1:
				if y - 1 >= 0:
					self.data[x +1][y-1] += 1

				self.data[x + 1][y] += 1

				if y +1 <= RANK_NUM -1:
					self.data[x+1][y+1] += 1

			if y -1 >= 0:
				self.data[x][y-1] += 1

			if y + 1 <= RANK_NUM -1:
				self.data[x][y + 1] += 1

	def draw_grid(self):
		for x in range(RANK_NUM):
			for y in range(RANK_NUM):
				if [x, y] in self.be_dig_out:
					continue
				self.painting(x, y, BLOCK_COLOR)

	def painting(self, x, y, painting_color):
		start_x = STATR_BITWISE
		start_y = STATR_BITWISE
		pyglet.graphics.draw(
					4, pyglet.gl.GL_QUADS,
					('v2f',
						(
							start_x + BLOCK_LEN * x + 3, start_y + BLOCK_LEN * y + 3,
							start_x + BLOCK_LEN * (x + 1) - 3, start_y + BLOCK_LEN * y + 3,
							start_x + BLOCK_LEN * (x + 1) - 3, start_y + BLOCK_LEN * (y + 1) - 3,
							start_x + BLOCK_LEN * x + 3, start_y + BLOCK_LEN * (y + 1) - 3
						)
					),
					('c4B', painting_color *4)	
					)

def main():
	mine = Mine()
	pyglet.clock.schedule_interval(mine.update_interval, .5)
	pyglet.app.run()

if __name__ == '__main__':
	main()