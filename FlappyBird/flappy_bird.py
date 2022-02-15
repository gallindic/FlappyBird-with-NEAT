import enum
import pygame
import neat

from FlappyBird.Utils.utils import *
from FlappyBird.Display.display import Display
from FlappyBird.Entity.bird import Bird
from FlappyBird.Entity.platform import Platform
from FlappyBird.Entity.pipe import Pipe

class FlappyBird():
    GEN = -1
    def __init__(self):
        pygame.init()
        pygame.font.init() 
        
        self.configurations_file = "config.yaml"
        self.configurations = parse_configurations(self.configurations_file)
        
        self._initialize()
    
    
    def _initialize(self):
        self.display = self._init_display()
        
        self.score = 0
        self.max_score = 0
        self.finished = False
        self.birds = []
        self.pipes = []

        self.clock = pygame.time.Clock()
        self.FPS = self.configurations['fps']
        self.animation_time = self.configurations['animation_time']
        self.pipes_interval = self.configurations['pipes_interval']
        font_size = int(self.configurations['font_size'])

        self.font = pygame.font.SysFont('Arial', font_size)

        self._init_platform()

    
    def _init_display(self):
        window_width = int(self.configurations['window_width'])
        window_height = int(self.configurations['window_height'])
        window_title = str(self.configurations['window_title'])
        background = str(self.configurations['background'])
        icon = str(self.configurations['icon'])

        return Display(window_width, window_height, window_title, background, icon)
    
    
    def _init_bird(self):
        self.birds.append(Bird(50, 100, self.animation_time))

    
    def _init_platform(self):
        self.platform = Platform(self.display.get_height() - 112)

    
    def _create_pipes(self):
        top_pipe = Pipe(self.display.get_width() + 1, 0, True)
        bottom_pipe_height = self.display.get_height() - self.platform.height - Pipe.GAP - top_pipe.height
        bottom_pipe = Pipe(self.display.get_width() + 1, self.display.get_height() - self.platform.height, False, bottom_pipe_height)
        
        self.pipes.append(top_pipe)
        self.pipes.append(bottom_pipe)


    def restart(self):
        if self.score > self.max_score:
            self.max_score = self.score

        self.score = 0
        self.birds = []
        self.pipes = []


    def display_score(self):
        self.display.get_display().blit(self.font.render('Score: ' + str(self.score), True, (255, 255, 255)), (10, 15))
        self.display.get_display().blit(self.font.render('Max score: ' + str(self.max_score), True, (255, 255, 255)), (10, 40))


    def display_neat_stats(self, generation, population_size):
        self.display.get_display().blit(self.font.render('Generation: ' + str(generation), True, (255, 255, 255)), (10, 65))
        self.display.get_display().blit(self.font.render('Population: ' + str(len(self.birds)) + '/' + str(population_size), True, (255, 255, 255)), (10, 90))


    def get_next_pipe_pair(self):
        birds_pos_x = self.birds[0].get_pos()[0]
        birds_width = self.birds[0].width
        pipes_width = self.pipes[0].width

        for i in range(2, len(self.pipes), 2):
            if i + 2 > len(self.pipes):
                breakpoint

            perv_pipe_pair = self.pipes[i-2:i]
            next_pipe_pair = self.pipes[i:i+2]

            if perv_pipe_pair[0].get_pos()[0] + pipes_width < birds_pos_x and next_pipe_pair[0].get_pos()[0] > birds_pos_x + birds_width:
                return next_pipe_pair

        return self.pipes[0:2]


    def run(self, genomes, config):
        frame_clock = None
        self.GEN += 1
        ge = []
        neural_networks = []
        population_size = len(genomes)

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            neural_networks.append(net)
            self._init_bird()
            g.fitness = 0
            ge.append(g)

        while not self.finished:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
            
            self.display.display_background()

            if len(self.birds) <= 0:
                self.restart()
                break

            if frame_clock is None or frames_to_msec(frame_clock, self.FPS) >= self.pipes_interval:
                frame_clock = 0
                self._create_pipes()

            next_pipe_pair = self.get_next_pipe_pair()

            for x, bird in enumerate(self.birds):
                    bird.move()
                    ge[x].fitness += 0.1

                    output = neural_networks[x].activate((bird.y, abs(bird.y - next_pipe_pair[0].height), abs(bird.y - next_pipe_pair[1].y)))
                    
                    if output[0] > 0.5:
                        bird.jump()

                    if bird.has_hit_celling():
                        ge[x].fitness -= 2
            
            for pipe in self.pipes:
                for x, bird in enumerate(self.birds):
                    if bird.has_collided(pipe) or bird.has_collided(self.platform):
                        ge[x].fitness -= 1
                        self.birds.pop(x)
                        ge.pop(x)
                        neural_networks.pop(x)

                    if bird.has_passed(self.pipes[0]) and not self.pipes[0].passed:
                        self.pipes[0].set_passed()
                        self.score += 1

                        for g in ge:
                            g.fitness += 3

                pipe.move()

                if pipe.is_offscreen():
                    self.pipes.remove(pipe)

            self.platform.move()

            for pipe in self.pipes:
                pipe.draw(self.display.get_display())

            for bird in self.birds:
                bird.draw(self.display.get_display())

            self.platform.draw(self.display.get_display())
            
            self.display_score()
            self.display_neat_stats(self.GEN, population_size)
            self.display.update_display()

            frame_clock += 1
            self.clock.tick(self.FPS)
            
            
    def quit(self):
        pygame.quit()